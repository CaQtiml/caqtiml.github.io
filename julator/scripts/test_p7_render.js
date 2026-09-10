// Headless DOM/fetch shim to execute p7/app.js and assert the bidirectional
// set <-> ปรมัตถ์ render + cross-highlight.  Run: node scripts/test_p7_render.js
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "data/data.json"), "utf8"));

class El {
  constructor(tag) {
    this.tag = tag; this.children = []; this.parent = null;
    this.dataset = {}; this.hidden = false; this._text = ""; this._html = ""; this.disabled = false;
    this.style = { setProperty(k, v) { (this._m = this._m || {})[k] = v; } };
    this.classList = {
      _s: new Set(),
      add: (...c) => c.forEach((x) => this.classList._s.add(x)),
      remove: (...c) => c.forEach((x) => this.classList._s.delete(x)),
      toggle: (c, on) => { on ? this.classList._s.add(c) : this.classList._s.delete(c); },
      contains: (c) => this.classList._s.has(c),
    };
  }
  set className(v) { this.classList._s = new Set(String(v).split(/\s+/).filter(Boolean)); }
  get className() { return [...this.classList._s].join(" "); }
  appendChild(c) { c.parent = this; this.children.push(c); return c; }
  set innerHTML(v) { this._html = v; if (v === "") this.children = []; }
  get innerHTML() { return this._html; }
  set textContent(v) { this._text = v; }
  get textContent() { return this._text; }
  _all(pred, acc) { for (const c of this.children) { if (pred(c)) acc.push(c); c._all(pred, acc); } return acc; }
  querySelectorAll(sel) { return this._all((c) => matchOne(c, sel), []); }
  closest(sel) { let n = this; while (n) { if (matchOne(n, sel)) return n; n = n.parent; } return null; }
}
function matchOne(el, sel) {
  if (!el || !el.tag) return false;
  if (sel.startsWith("#")) return el._domId === sel.slice(1);
  const m = sel.match(/^\.([\w-]+)(?:\[([\w-]+)\])?$/);
  if (m) return el.classList.contains(m[1]) && (!m[2] || m[2] in el.dataset);
  return false;
}
const byId = {};
global.document = {
  _listeners: {},
  getElementById: (id) => byId[id],
  createElement: (t) => new El(t),
  addEventListener: (ev, fn) => { (global.document._listeners[ev] = global.document._listeners[ev] || []).push(fn); },
  querySelectorAll: (sel) => {
    const out = [];
    Object.values(byId).forEach((r) => { if (matchOne(r, sel)) out.push(r); r._all((c) => matchOne(c, sel), out); });
    return out;
  },
};
for (const id of ["sangaha-switch", "set-groups", "paramattha-groups", "info-panel", "set-count", "paramattha-count"]) {
  const e = new El("div"); e._domId = id; byId[id] = e;
}
global.fetch = () => Promise.resolve({ json: () => Promise.resolve(data) });

require(path.join(ROOT, "p7/app.js"));

let failed = 0;
const ok = (c, m) => { if (!c) { console.error("FAIL:", m); failed++; } else console.log("ok:", m); };
const all = (root, sel) => root._all((c) => matchOne(c, sel), []);
const fire = (ev, target) => (global.document._listeners[ev] || []).forEach((fn) =>
  fn({ target: { closest: (s) => (target ? target.closest(s) : null) } }));
const rel = (root, sel) => all(root, sel).filter((n) => n.classList.contains("is-related"));
const tab = (sg) => byId["sangaha-switch"].children.find((t) => t.dataset.sangaha === sg);

setTimeout(() => {
  ok(byId["sangaha-switch"].children.length === 4, "4 สังคหะ tabs");
  ok(byId["sangaha-switch"].children.map((t) => t.dataset.sangaha).join(",") === "akusala,missaka,bodhipakkhiya,sabba",
    "tab order = อกุศล มิสสก โพธิปักขิย สัพพ");
  ok(byId["sangaha-switch"].children.filter((t) => t.disabled).length === 0, "no tab disabled");

  // ---------- right panel: every ปรมัตถ์ ----------
  const nodes = all(byId["paramattha-groups"], ".node");
  ok(nodes.length === 202, "202 ปรมัตถ์ nodes (" + nodes.length + ")");
  ok(nodes.filter((n) => !n.classList.contains("cetasika") && !n.classList.contains("rupa") && !n.classList.contains("nibbana")).length === 121, "121 จิต nodes");
  ok(nodes.filter((n) => n.classList.contains("cetasika")).length === 52, "52 เจตสิก nodes");
  ok(nodes.filter((n) => n.classList.contains("rupa")).length === 28, "28 รูป nodes");
  ok(nodes.filter((n) => n.classList.contains("nibbana")).length === 1, "1 นิพพาน node");
  ok(all(byId["paramattha-groups"], ".p7-para-section").length === 4, "4 ปรมัตถ์ sections");

  // ---------- left panel: อกุศลสังคหะ active ----------
  let sets = all(byId["set-groups"], ".p7-set");
  ok(sets.length === 9, "อกุศล: 9 dhamma-set blocks (" + sets.length + ")");
  const heads = all(byId["set-groups"], ".p7-set-head");
  ok(heads.map((h) => h.dataset.setkey).includes("akusala/asava"), "อกุศล: asava set head present");
  const asavaBlock = sets.find((s) => all(s, ".p7-set-head")[0].dataset.setkey === "akusala/asava");
  ok(all(asavaBlock, ".p7-member").length === 4, "อกุศล: อาสวะ has 4 member chips");
  ok(all(byId["set-groups"], ".p7-member").length === 53,
    "อกุศล: 53 member chips total (4+4+4+4+4+6+7+10+10) (" + all(byId["set-groups"], ".p7-member").length + ")");

  // ---------- click a member -> right lights its องค์ธรรม ----------
  {
    const kamasava = all(byId["set-groups"], ".p7-member").find((c) => c.dataset.memberkey === "akusala/asava/kamasava");
    fire("click", kamasava);
    ok(kamasava.classList.contains("is-selected"), "member: กามาสวะ is-selected");
    const lobhaNode = nodes.find((n) => n.dataset.id === "lobha");
    ok(lobhaNode.classList.contains("is-related"), "member: โลภเจตสิก node lit (กามาสวะ องค์ธรรม)");
    ok(rel(byId["paramattha-groups"], ".node").length === 1, "member: exactly 1 ปรมัตถ์ lit for กามาสวะ");
    ok(/กามาสวะ/.test(byId["info-panel"].innerHTML) && /อกุศลสังคหะ/.test(byId["info-panel"].innerHTML),
      "member: info shows name + parent สังคหะ");
    fire("click", kamasava); // unpin
  }

  // ---------- click a set head -> union of member องค์ธรรม ----------
  {
    const asavaHead = heads.find((h) => h.dataset.setkey === "akusala/asava");
    fire("click", asavaHead);
    ok(asavaHead.classList.contains("is-selected"), "set: อาสวะ head is-selected");
    ok(rel(byId["set-groups"], ".p7-member").length === 4, "set: all 4 อาสวะ members lit");
    const litIds = rel(byId["paramattha-groups"], ".node").map((n) => n.dataset.id).sort();
    ok(litIds.join(",") === "ditthi,lobha,moha", "set: อาสวะ union องค์ธรรม = โลภ ทิฏฐิ โมห (" + litIds.join(",") + ")");
    ok(/รวมองค์ธรรม 3 ปรมัตถ์/.test(byId["info-panel"].innerHTML), "set: info reports 3 distinct องค์ธรรม");
    fire("click", asavaHead);
  }

  // ---------- click a ปรมัตถ์ -> reverse: light every set/member it is in ----------
  {
    const lobhaNode = nodes.find((n) => n.dataset.id === "lobha");
    fire("click", lobhaNode);
    ok(lobhaNode.classList.contains("is-selected"), "para: โลภเจตสิก is-selected");
    ok(tab("akusala").classList.contains("has-match"), "para: อกุศล tab badged has-match");
    ok(/ตรง \d+ องค์/.test(tab("akusala").innerHTML), "para: อกุศล tab shows a match count");
    ok(rel(byId["set-groups"], ".p7-member").length >= 8,
      "para: โลภเจตสิก lights many อกุศล members (" + rel(byId["set-groups"], ".p7-member").length + ")");
    ok(/ปรากฏใน \d+ หมวด/.test(byId["info-panel"].innerHTML), "para: info lists the sets it appears in");
    fire("click", lobhaNode);
  }

  // ---------- tab switch ----------
  {
    fire("click", tab("sabba"));
    sets = all(byId["set-groups"], ".p7-set");
    ok(sets.length === 5, "สัพพ: 5 dhamma-set blocks");
    const khandhaBlock = sets.find((s) => all(s, ".p7-set-head")[0].dataset.setkey === "sabba/khandha");
    ok(all(khandhaBlock, ".p7-member").length === 5, "สัพพ: ขันธ์ has 5 members");
  }

  // ---------- para selection auto-switches สังคหะ when active tab has no match ----------
  {
    fire("click", tab("akusala")); // akusala has no นิพพาน
    const nibNode = all(byId["paramattha-groups"], ".node").find((n) => n.dataset.id === "nibbana");
    fire("click", nibNode);
    ok(tab("sabba").classList.contains("active"),
      "para นิพพาน: auto-switched to สัพพสังคหะ (only สังคหะ that contains it)");
    ok(rel(byId["set-groups"], ".p7-member").length === 3,
      "para นิพพาน: 3 สัพพ members lit (นิโรธสัจจ + ธัมมายตนะ + ธัมมธาตุ) (" + rel(byId["set-groups"], ".p7-member").length + ")");
    ok(/นิพพาน/.test(byId["info-panel"].innerHTML), "para นิพพาน: info title");
    fire("click", nibNode);
  }

  // ---------- click empty space clears the pin ----------
  {
    const head = all(byId["set-groups"], ".p7-set-head")[0];
    fire("click", head);
    fire("click", null); // nothing -> closest() returns null everywhere
    ok(rel(byId["paramattha-groups"], ".node").length === 0 &&
       all(byId["set-groups"], ".p7-set-head").filter((h) => h.classList.contains("is-selected")).length === 0,
      "click-away clears selection");
  }

  console.log(failed ? "\n" + failed + " CHECK(S) FAILED" : "\nALL CHECKS PASSED");
  process.exitCode = failed ? 1 : 0;
}, 50);
