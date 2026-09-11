---
title: "Integrating Dynamic Region-Based Ownership into CPython and NumPy"
excerpt: "My master's thesis on retrofitting a concurrency-safety ownership model into CPython and NumPy, done within Uppsala's Pyrona project."
collection: portfolio
---

{% include toc %}

## About this Project

This is my MSc degree project at Uppsala University, done within the
**Pyrona project** (a collaboration between Uppsala's UPLANG group and
[Microsoft Research](https://microsoft.github.io/verona/pyrona.html)), supervised by Fridtjof Peer Stoldt and Tobias Wrigstad. The Pyrona project as a whole consists of 3 master theses and 2 bachelor theses in VT2026, of which mine is one.

Read the full thesis on Uppsala University's publication database (DiVA):
[urn:nbn:se:uu:diva-597391](http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-597391).

This blog explains the project informally; the presentation slides give a
more visual walkthrough and are embedded below.

### Presentation Slides

<iframe src="https://mozilla.github.io/pdf.js/web/viewer.html?file=https://sivakornl.com/files/master/msc_presentation_resource.pdf" width="100%" height="800px" style="border:none;"></iframe>

[Open presentation directly](/files/master/msc_presentation_resource.pdf) — [Shared Pyrona project presentation](/files/master/shared_presentation_pyrona.pdf) (introduces the project background across all 5 theses).

My presentation deck above includes more slides than the version I actually used live, since I wanted it to be more understandable on its own for an audience not already familiar with the topic.

## The Problem I'm Working On

Python's Global Interpreter Lock (GIL) blocks true parallelism. Python
3.12+'s sub-interpreters (PEP 554/684/734) sidestep this by giving each
interpreter its own GIL — but at the cost of being "shared-nothing":
objects have to be copied across interpreters rather than shared.

The Pyrona project proposes **Dynamic Region-based Ownership (DRO)** as a
way to let mutable objects be shared safely across interpreters via
runtime-checked **write barriers**, building on the foundational paper by
Stoldt et al. (["Dynamic Region Ownership for Concurrency Safety,"](https://dl.acm.org/doi/10.1145/3729313) PLDI
2025). Going into my thesis, the DRO prototype only covered a very limited
set of data structures. My job was to extend it — into three more CPython
built-in types, and into NumPy, a major external C-extension library — and
to build a methodology for actually verifying the migrations were correct.

## Key Ideas

Every Python object carries a reference count (`ob_refcnt`) managed through
macros like `Py_INCREF`/`Py_DECREF`. DRO groups objects into **regions**,
distinguishes **mortal** objects from **immortal** ones (like small cached
integers or `True`/`False`), and replaces raw refcount manipulation at
region boundaries with explicit **write barriers** — functions like
`PyRegion_AddRef`, `PyRegion_RemoveRef`, `PyRegion_TakeRef`, and
`PyRegion_CLEAR` — that keep a region's **Local Reference Count (LRC)**
consistent. Correctly placing these barriers depends on `tp_traverse`, the
existing CPython mechanism for walking an object's outgoing references.

## What I Built: CPython Migrations

I migrated three built-in types, working out and cataloging the rules for
where write barriers need to go — the barrier has to go in *before* any
refcount modification, integer-returning barriers need error handling where
void-returning ones don't, and only mortal, mutable objects with the right
object-header shape can be passed to a barrier at all.

- **`range`**: added 67 write barriers (1282 → 1474 lines). Atomic
  multi-field updates need barriers that act atomically too, migration can
  be skipped when arguments are immortal, and slicing a range silently
  constructs a `slice` object that itself needs partial migration.
- **`set`**: added 128 write barriers (2592 → 3208 lines) — the largest of
  the three. The same method reachable from multiple call sites sometimes
  needs conditional barrier logic gated on a boolean flag, and
  `set_swap_bodies` needs migration even though it uses raw pointer
  manipulation with no recognizable refcount pattern at all.
- **`enumerate`**: added 32 write barriers (544 → 653 lines). `enum_next`'s
  tuple-recycling optimization breaks under ownership — you can't recycle a
  tuple that's already been moved into a region — and a reference the
  Python-level user can never independently release still has to be
  explicitly removed by the runtime at the end of iteration.

## What I Built: NumPy Migration

NumPy was a genuinely different kind of challenge, since it's a large
external C-extension library rather than a CPython built-in. I added 52
write barriers across 9 files, solving three problems that didn't exist in
the CPython built-ins:

1. **NumPy arrays had no `tp_traverse` at all** — I implemented it from
   scratch, guarding it with the `NPY_ARRAY_OWNDATA` flag so a view and its
   base array don't get double-traversed.
2. **Views don't own their data** — ownership constraints have to be
   enforced against the *base* array a view points into, not the view
   itself.
3. **`OBJECT_setitem`/`OBJECT_getitem` disguise semantic assignment as
   `memcpy` and indirect refcount calls** — I had to choose the correct
   barrier (`AddRef` vs. `AddLocalRef`) based on what the code was actually
   doing semantically, not what it looked like syntactically.

I scoped the NumPy work to object-dtype 1-D arrays and four indexing modes
(slice, ellipsis, scalar integer, boolean) in `array_subscript` and
`array_assign_subscript`, and treated `mem_handler`/`descr` as immutable via
a `freeze` mechanism from a related deep-immutability paper.

## How I Verified Correctness

Beyond re-running CPython's and NumPy's existing unit test suites for
regressions, I designed a **five-scenario conformance testing
methodology** covering the ways an object's ownership can legitimately (or
illegitimately) change: same-location no-ops, moving a local reference into
a region, removing a regional reference back to local, moving a regional
reference to an ephemeral local one, and cross-region references (which
must raise a `RuntimeError`). A key methodological insight was that the
Local Reference Count must be tracked as a **relative delta**, not an
absolute value, for the conformance tests to be meaningful.

Results: `test_set.py` passed 72 of 76 cases (4 ignored, tied to a known
in-place-operation bug); `test_enum.py` passed all 27 of 27; my NumPy test
suite (`test_basic_refactor.py`) passed all 172 of 172. `range` doesn't yet
have a formal conformance suite — my supervisor advised holding off pending
a planned redesign of the integer-barrier approach — so I verified it with
manual test scripts instead.

Note that none of this testing is concurrent. I rely on the theoretical
guarantee already established in the foundational DRO paper: the base
model proves that if ownership constraints are strictly maintained, the
system is free from data races. So the goal of my conformance testing
isn't to re-prove data-race freedom — it's to verify that write barriers
are correctly inserted to enforce the model's rules. If the barriers are
placed correctly, the migrated data structures inherit the model's
data-race-free property by construction, which is why sequential testing
is sufficient here.

## Development Practice

I built and rebuilt CPython from source throughout the project, working in
a Linux environment. When a barrier was placed incorrectly, the symptom
was usually a corrupted region state or an off reference count much later
in execution, so I leaned on GDB heavily — tracing call stacks back to the
offending site and setting watchpoints on internal region/refcount fields
to catch the exact moment they went wrong. The codebase is developed
collaboratively against the Pyrona project's prototype on GitHub; my own
work lives [here](https://github.com/CaQtiml/cpython/tree/regions-main-mil-updated).

## Contribution, Limitations, and What's Next

The concrete contribution here is threefold: a catalog of the CPython
write-barrier patterns and edge cases I found, a documented case study of
what it takes to migrate a major *external* C-extension library (NumPy)
rather than just CPython's own built-ins, and a reusable five-scenario
conformance-testing methodology. The current scope is sequential-only (no
concurrent or multi-interpreter testing yet), the NumPy work covers only a
narrow slice of its indexing/dtype surface, and the immutability assumption
on `mem_handler`/`descr` is something I flagged as needing revisiting. If
this work continues, the natural next steps are finishing the CPython
migration, widening the NumPy scope (higher dimensions, fancy indexing,
structured arrays), applying the same approach to other external libraries,
and adding concurrent tests or formal verification.

## Why This Matters Beyond the Thesis Itself

This is hands-on, first-authored systems research at the boundary of
language-runtime design and the C-extension ecosystem that libraries like
NumPy (and, by extension, most of the Python ML/AI stack) actually depend
on. It's directly relevant to any role or program concerned with the
low-level performance, memory-safety, or concurrency behavior of ML
infrastructure.

The reusable research-taste lesson: the hard part of retrofitting a safety
abstraction onto an existing codebase is rarely the well-behaved cases, but
the optimized, low-level operations whose need for migration cannot be
read off the surface of the code and only reveals itself by reasoning about
what the operation actually does to memory. NumPy's `memcpy`-based
assignments are the worked example — syntactically a byte copy,
semantically a reference replacement. The same shape of problem shows up
wherever performance optimizations hide operations from a higher-level
view (GPU memory coalescing and shared-memory tiling are the analogues I'd
expect on the accelerator side).
