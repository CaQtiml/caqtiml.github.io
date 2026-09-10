// ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- interactive classification tool.
//
// Scheme-driven. data/data.json carries one entry per นัย (data/p3/<id>.yaml,
// assembled by scripts/build_data.py). A นัย with data renders an active tab;
// the rest render disabled.  Built so far: เวทนาสังคหะ, เหตุสังคหะ, กิจจสังคหะ,
// ทวารสังคหะ, อารัมมณสังคหะ, วัตถุสังคหะ (all 6 นัย).
//
// Layout follows julatri: the จิต and เจตสิก panels are always organised by the
// standard จิต/เจตสิก groups (โลภมูลจิต ๘ ... โลกุตตรจิต ๔๐; สัพพจิตตสาธารณ ๗ ...),
// in the textbook's order and row structure. The active scheme shows as node
// colour / dots + the category rail + cross-highlight -- it never re-buckets
// the panels.
//
// Each scheme's citta / cetasika axis-block declares a `cardinality`:
//   * partition -- each ปรมัตถ์ sits in exactly one category; node is tinted.
//   * matrix    -- each ปรมัตถ์ carries a SET of 0..N categories; node shows
//                  a strip of coloured dots, and `groupings` bucket by set size.
// เวทนา: จิต partition (เวทนา ๕), เจตสิก matrix.  เหตุ / กิจ / ทวาร / อารมณ์ /
// วัตถุ: both axes matrix (เหตุ ๖ / กิจ ๑๔ / ทวาร ๖ / อารมณ์ ๖ / วัตถุ ๖).

const CITTA_GROUPS = [
  { id: "lobha-mula", label: "โลภมูลจิต ๘ (รากเหง้าคือโลภะ)", chunkSize: 4 },
  { id: "dosa-mula", label: "โทสมูลจิต ๒ (รากเหง้าคือโทสะ)" },
  { id: "moha-mula", label: "โมหมูลจิต ๒ (รากเหง้าคือโมหะ)" },
  { id: "ahetuka", label: "อเหตุกจิต ๑๘ (๗ อกุศลวิบาก, ๘ กุศลวิบาก, ๓ กิริยา)", rows: [7, 8, 3] },
  { id: "mahakusala", label: "มหากุศลจิต ๘ (กามาวจรโสภณ)", chunkSize: 4 },
  { id: "mahavipaka", label: "มหาวิปากจิต ๘ (กามาวจรโสภณ)", chunkSize: 4 },
  { id: "mahakiriya", label: "มหากิริยาจิต ๘ (กามาวจรโสภณ)", chunkSize: 4 },
  { id: "rupa-jhana", label: "รูปาวจรจิต ๑๕ (กุศล/วิบาก/กิริยา × ฌาน ๑-๕)", chunkSize: 5 },
  { id: "arupa-jhana", label: "อรูปาวจรจิต ๑๒ (กุศล/วิบาก/กิริยา × อรูปฌาน ๔)", chunkSize: 4 },
  { id: "lokuttara", label: "โลกุตตรจิต ๔๐ (พิสดาร, มรรค-ผล ๘ × ฌาน ๑-๕)", chunkSize: 5 },
];

const CETASIKA_GROUPS = [
  { id: "sabbacitta-sadharana", label: "สัพพจิตตสาธารณเจตสิก ๗ — ประกอบกับจิตทุกดวง" },
  { id: "pakinnaka", label: "ปกิณณกเจตสิก ๖ — ประกอบเป็นบางครั้ง" },
  { id: "moha-catuka", label: "โมจตุกเจตสิก ๔ — อกุศลจิตทุกดวง" },
  { id: "lobha-tika", label: "โลติกเจตสิก ๓ — เฉพาะโลภมูลจิต" },
  { id: "dosa-catuka", label: "โทจตุกเจตสิก ๔ — เฉพาะโทสมูลจิต" },
  { id: "thina-duka", label: "ถีทุกเจตสิก ๒ — เฉพาะสสังขาริก" },
  { id: "vicikiccha", label: "วิจิกิจฉาเจตสิก ๑ — เฉพาะโมหมูลจิตดวงที่ ๑" },
  { id: "sobhana-sadharana", label: "โสภณสาธารณเจตสิก ๑๙ — จิตดีงามทุกดวง" },
  { id: "virati", label: "วิรตีเจตสิก ๓ — งดเว้นจากทุจริต" },
  { id: "appamanna", label: "อัปปมัญญาเจตสิก ๒ — กรุณา มุทิตา" },
  { id: "pannindriya", label: "ปัญญินทรีย์เจตสิก ๑ — ปัญญา" },
];

// category id -> CSS custom property, per scheme. shell.css owns the tokens
// (light + dark). Unknown ids fall back to a neutral grey.
const SCHEME_PALETTE = {
  vedana: {
    sukha: "--v-sukha", dukkha: "--v-dukkha", somanassa: "--v-somanassa",
    domanassa: "--v-domanassa", upekkha: "--v-upekkha",
  },
  hetu: {
    lobha: "--h-lobha", dosa: "--h-dosa", moha: "--h-moha",
    alobha: "--h-alobha", adosa: "--h-adosa", amoha: "--h-amoha",
  },
  kicca: {
    patisandhi: "--k-patisandhi", bhavanga: "--k-bhavanga", avajjana: "--k-avajjana",
    dassana: "--k-dassana", savana: "--k-savana", ghayana: "--k-ghayana",
    sayana: "--k-sayana", phusana: "--k-phusana", sampaticchana: "--k-sampaticchana",
    santirana: "--k-santirana", votthapana: "--k-votthapana", javana: "--k-javana",
    tadarammana: "--k-tadarammana", cuti: "--k-cuti",
  },
  dvara: {
    cakkhu: "--d-cakkhu", sota: "--d-sota", ghana: "--d-ghana",
    jivha: "--d-jivha", kaya: "--d-kaya", mano: "--d-mano",
  },
  arammana: {
    rupa: "--am-rupa", satta: "--am-satta", gandha: "--am-gandha",
    rasa: "--am-rasa", photthabba: "--am-photthabba", dhamma: "--am-dhamma",
  },
  vatthu: {
    cakkhu: "--vt-cakkhu", sota: "--vt-sota", ghana: "--vt-ghana",
    jivha: "--vt-jivha", kaya: "--vt-kaya", hadaya: "--vt-hadaya",
  },
};
const FALLBACK_VAR = "--cat-neutral";

const el = {
  schemeSwitch: document.getElementById("scheme-switch"),
  subaxisSwitch: document.getElementById("subaxis-switch"),
  cittaGroups: document.getElementById("citta-groups"),
  cetasikaGroups: document.getElementById("cetasika-groups"),
  catRail: document.getElementById("cat-rail"),
  info: document.getElementById("info-panel"),
  cittaCount: document.getElementById("citta-count"),
  cetasikaCount: document.getElementById("cetasika-count"),
};

const store = {
  schemes: [], schemeById: {},
  cittas: [], cetasikas: [], cittaById: {}, cetasikaById: {},
  scheme: "vedana", view: null,
  pinned: null, hover: null,
};

fetch("../data/data.json")
  .then((r) => r.json())
  .then((data) => {
    store.schemes = data.p3.schemes;
    store.schemes.forEach((s) => (store.schemeById[s.id] = s));
    store.cittas = data.paramattha.citta;
    store.cetasikas = data.paramattha.cetasika;
    store.cittas.forEach((c) => (store.cittaById[c.id] = c));
    store.cetasikas.forEach((c) => (store.cetasikaById[c.id] = c));
    el.cittaCount.textContent = "(" + store.cittas.length + ")";
    el.cetasikaCount.textContent = "(" + store.cetasikas.length + ")";
    const first = store.schemes.find((s) => s.citta || s.cetasika);
    store.scheme = first ? first.id : store.schemes[0].id;
    resetView();
    renderSchemeTabs();
    renderAll();
  })
  .catch((e) => {
    el.info.innerHTML = '<p class="info-placeholder">โหลดข้อมูลไม่สำเร็จ</p>';
    console.error(e);
  });

// ---------- scheme / category helpers ----------

function scheme() { return store.schemeById[store.scheme]; }
function activeView() {
  return (scheme().views || []).find((v) => v.id === store.view) || null;
}
function collapseMap() {
  const v = activeView();
  return (v && v.collapse) || {};
}
function effCat(c) { return collapseMap()[c] || c; }

// every category the active scheme uses, citta block first, de-duplicated,
// in declared order (this is the order feelings/roots are listed in).
function schemeCats() {
  const out = [];
  [scheme().citta, scheme().cetasika].forEach((b) => {
    if (!b) return;
    (b.categories || []).forEach((c) => { if (!out.find((x) => x.id === c.id)) out.push(c); });
  });
  return out;
}
function catOrder() { return schemeCats().map((c) => c.id); }
function catThaiAny(id) {
  const hit = schemeCats().find((c) => c.id === id);
  return hit ? hit.thai : id;
}
function catVar(id) {
  return (SCHEME_PALETTE[store.scheme] || {})[id] || FALLBACK_VAR;
}

// collapse-map applied, de-duped, ordered
function effSet(cats) {
  const ord = catOrder();
  const out = [];
  (cats || []).map(effCat).forEach((c) => { if (!out.includes(c)) out.push(c); });
  return out.sort((a, b) => ord.indexOf(a) - ord.indexOf(b));
}
// visible categories for the rail (collapse-map applied)
function displayCats() {
  const seen = [];
  schemeCats().forEach((c) => {
    const e = effCat(c.id);
    if (!seen.find((x) => x.id === e)) seen.push({ id: e, thai: catThaiAny(e) });
  });
  return seen;
}

function rawCats(block, ref) {
  const a = block && (block.assignments || []).find((x) => x.ref === ref);
  return a ? a.cats : null;
}
// the effective category set of one ปรมัตถ์ under `block` (partition -> 1 entry)
function catsOf(block, ref) {
  const raw = rawCats(block, ref);
  if (raw == null) return [];
  return block.cardinality === "partition"
    ? [effCat(raw[0])].filter(Boolean)
    : effSet(raw);
}
function cittaCatsOf(ref) { return catsOf(scheme().citta, ref); }
function cetasikaCatsOf(ref) { return catsOf(scheme().cetasika, ref); }
function bucketOf(block, size) {
  return (block && (block.groupings || []).find((g) => g.size === size)) || null;
}

function resetView() {
  const vs = scheme().views || [];
  store.view = vs.length ? vs[0].id : null;
}

// ---------- rendering ----------

function renderSchemeTabs() {
  el.schemeSwitch.innerHTML = "";
  store.schemes.forEach((s) => {
    const b = document.createElement("button");
    b.className = "mode-btn" + (s.id === store.scheme ? " active" : "");
    b.dataset.scheme = s.id;
    const ready = !!(s.citta || s.cetasika);
    b.disabled = !ready;
    b.innerHTML = s.thai + (ready ? "" : '<span class="mode-hint">เร็วๆ นี้</span>');
    el.schemeSwitch.appendChild(b);
  });
}

function renderSubaxis() {
  const vs = scheme().views || [];
  el.subaxisSwitch.innerHTML = "";
  el.subaxisSwitch.hidden = vs.length < 2;
  vs.forEach((v) => {
    const b = document.createElement("button");
    b.className = "subaxis-btn" + (v.id === store.view ? " active" : "");
    b.dataset.view = v.id;
    b.textContent = v.thai;
    el.subaxisSwitch.appendChild(b);
  });
}

function dotStrip(cats) {
  const strip = document.createElement("span");
  strip.className = "tagstrip";
  if (cats.length) {
    cats.forEach((c) => {
      const d = document.createElement("span");
      d.className = "tagdot";
      d.style.setProperty("--dot", "var(" + catVar(c) + ")");
      strip.appendChild(d);
    });
  } else {
    strip.classList.add("tagstrip-none");
  }
  return strip;
}

function makeNode(kind, id) {
  const rec = kind === "citta" ? store.cittaById[id] : store.cetasikaById[id];
  const block = scheme()[kind];
  const n = document.createElement("button");
  n.className = "node" + (kind === "cetasika" ? " cetasika" : "");
  n.dataset.kind = kind;
  n.dataset.id = id;

  const label = document.createElement("span");
  label.className = "node-label";
  label.textContent = rec ? rec.thai : id;
  n.appendChild(label);

  if (!block) return n;
  const cats = catsOf(block, id);

  if (block.cardinality === "partition") {
    const cat = cats[0];
    if (cat) {
      n.dataset.cat = cat;
      const cv = catVar(cat);
      n.style.setProperty("--node-color", "var(" + cv + ")");
      n.style.setProperty("--node-soft", "var(" + cv + "-soft)");
      n.title = (rec && rec.pali ? rec.pali + " — " : "") + block.axis + ": " + catThaiAny(cat);
    }
  } else {
    n.dataset.nset = String(cats.length);
    n.appendChild(dotStrip(cats));
    const bkt = bucketOf(block, cats.length);
    n.title = cats.length
      ? (bkt ? bkt.thai + " — " : "") + cats.map(catThaiAny).join(", ")
      : (bkt ? bkt.thai : "ไม่จัดเข้าหมวดใด");
  }
  return n;
}

function renderGroupedPanel(container, groups, allItems, kind) {
  container.innerHTML = "";
  if (!scheme()[kind]) {
    container.innerHTML = '<p class="bucket-empty">ยังไม่มีข้อมูลสำหรับนัยนี้</p>';
    return;
  }
  groups.forEach((g) => {
    const members = allItems.filter((c) => c.group === g.id);
    if (!members.length) return;
    const wrap = document.createElement("div");
    wrap.className = "natgroup";
    const label = document.createElement("p");
    label.className = "group-label";
    label.textContent = g.label;
    wrap.appendChild(label);

    const rowSizes = g.rows
      || (g.chunkSize ? Array(Math.ceil(members.length / g.chunkSize)).fill(g.chunkSize) : [members.length]);
    let i = 0;
    rowSizes.forEach((size) => {
      const row = document.createElement("div");
      row.className = "circle-row";
      members.slice(i, i + size).forEach((m) => row.appendChild(makeNode(kind, m.id)));
      i += size;
      wrap.appendChild(row);
    });
    container.appendChild(wrap);
  });
}

function renderCittaPanel() {
  renderGroupedPanel(el.cittaGroups, CITTA_GROUPS, store.cittas, "citta");
}
function renderCetasikaPanel() {
  renderGroupedPanel(el.cetasikaGroups, CETASIKA_GROUPS, store.cetasikas, "cetasika");
}

function countWith(block, catId) {
  if (!block) return 0;
  return (block.assignments || []).filter((a) => catsOf(block, a.ref).includes(catId)).length;
}

function renderRail() {
  const s = scheme();
  el.catRail.innerHTML = "";
  displayCats().forEach((cat) => {
    const nCitta = countWith(s.citta, cat.id);
    const nCeta = countWith(s.cetasika, cat.id);
    const b = document.createElement("button");
    b.className = "cat-chip";
    b.dataset.cat = cat.id;
    b.style.setProperty("--chip", "var(" + catVar(cat.id) + ")");
    b.innerHTML = "<span>" + cat.thai + '</span><span class="chip-count">จิต ' +
      nCitta + " · เจต " + nCeta + "</span>";
    el.catRail.appendChild(b);
  });
}

function renderAll() {
  renderSubaxis();
  renderCittaPanel();
  renderCetasikaPanel();
  renderRail();
  applyHighlight();
  renderInfo();
}

// ---------- highlighting ----------

function activeSelection() { return store.pinned || store.hover; }

function computeRelated(sel) {
  const s = scheme();
  const res = { cittas: new Set(), cetasikas: new Set(), cats: new Set() };
  if (!sel) return res;

  let targetCats = [];
  if (sel.type === "cat") targetCats = [sel.id];
  else if (sel.type === "citta") targetCats = cittaCatsOf(sel.id);
  else if (sel.type === "cetasika") targetCats = cetasikaCatsOf(sel.id);
  targetCats.forEach((c) => res.cats.add(c));

  if (s.citta) {
    s.citta.assignments.forEach((a) => {
      if (catsOf(s.citta, a.ref).some((c) => targetCats.includes(c))) res.cittas.add(a.ref);
    });
  }
  if (s.cetasika) {
    s.cetasika.assignments.forEach((a) => {
      if (catsOf(s.cetasika, a.ref).some((c) => targetCats.includes(c))) res.cetasikas.add(a.ref);
    });
  }
  return res;
}

function applyHighlight() {
  const sel = activeSelection();
  const rel = computeRelated(sel);
  document.querySelectorAll(".node").forEach((n) => {
    n.classList.remove("is-dim", "is-related", "is-selected");
    if (!sel) return;
    if (sel.type === n.dataset.kind && sel.id === n.dataset.id) {
      n.classList.add("is-selected");
      return;
    }
    const inSet = n.dataset.kind === "citta" ? rel.cittas.has(n.dataset.id) : rel.cetasikas.has(n.dataset.id);
    n.classList.add(inSet ? "is-related" : "is-dim");
  });
  document.querySelectorAll(".cat-chip").forEach((c) => {
    c.classList.remove("is-dim", "is-selected");
    if (!sel) return;
    if (sel.type === "cat" && sel.id === c.dataset.cat) c.classList.add("is-selected");
    else if (!rel.cats.has(c.dataset.cat)) c.classList.add("is-dim");
  });
}

// ---------- info panel ----------

function chip(catId, label) {
  return '<span class="info-chip" style="--chip:var(' + catVar(catId) + ')">' +
    (label || catId) + "</span>";
}
function groupLabelOf(groups, id) {
  const g = groups.find((x) => x.id === id);
  return g ? g.label : id;
}
function cardHint(block) {
  if (!block) return "";
  return block.cardinality === "partition"
    ? " (แต่ละดวงมีประเภทเดียว)"
    : " (นับได้หลายประเภทต่อดวง)";
}

// scheme.notes: a list of bullet items. Each item is either a plain string, or
// { t: <text>, sub: [<text>...] } for a bullet with sub-bullets. Rendered as a
// nested <ul>. Falls back to the legacy flat scheme.note string.
function notesHtml(s) {
  if (Array.isArray(s.notes) && s.notes.length) {
    const li = (item) => {
      if (typeof item === "string") return "<li>" + item + "</li>";
      const sub = (item.sub || []).map((x) => "<li>" + x + "</li>").join("");
      return "<li>" + (item.t || "") + (sub ? "<ul>" + sub + "</ul>" : "") + "</li>";
    };
    return '<ul class="info-notelist">' + s.notes.map(li).join("") + "</ul>";
  }
  return s.note ? '<p class="info-note">' + s.note + "</p>" : "";
}

function renderInfo() {
  const s = scheme();
  const sel = activeSelection();
  const pinned = !!store.pinned;

  if (!sel) {
    let h = '<h3 class="info-title">' + s.thai + "</h3>";
    if (s.citta) h += '<p class="info-related-label">จิต — ' + s.citta.axis + cardHint(s.citta) + "</p>";
    if (s.cetasika) h += '<p class="info-related-label">เจตสิก — ' + s.cetasika.axis + cardHint(s.cetasika) + "</p>";
    if (s.gatha) h += '<p class="info-gatha">' + s.gatha + "</p>";
    h += notesHtml(s);
    h += '<p class="clear-hint">ชี้หรือคลิกที่วงกลม / หมวดทางกลาง เพื่อดูความสัมพันธ์</p>';
    el.info.innerHTML = h;
    return;
  }

  let h = "";
  if (sel.type === "citta") {
    const rec = store.cittaById[sel.id];
    const cats = cittaCatsOf(sel.id);
    const bkt = bucketOf(s.citta, cats.length);
    h += '<h3 class="info-title">' + rec.thai + "</h3>";
    if (rec.pali) h += '<p class="info-pali">' + rec.pali + "</p>";
    h += '<p class="info-related-label">' + groupLabelOf(CITTA_GROUPS, rec.group) + "</p>";
    if (bkt) h += '<p class="info-related-label">' + bkt.thai + "</p>";
    h += '<p class="info-related-label">' + s.citta.axis + "</p><div class=\"info-chips\">" +
      (cats.length ? cats.map((c) => chip(c, catThaiAny(c))).join("") : "<em>—</em>") + "</div>";
    h += '<p class="info-note">เจตสิกที่เกิดร่วมได้ ' +
      computeRelated(sel).cetasikas.size + " ดวง (เน้นไว้ทางขวา)</p>";
  } else if (sel.type === "cetasika") {
    const rec = store.cetasikaById[sel.id];
    const cats = cetasikaCatsOf(sel.id);
    const bkt = bucketOf(s.cetasika, cats.length);
    h += '<h3 class="info-title">' + rec.thai + "</h3>";
    if (rec.meaning) h += '<p class="info-meaning">' + rec.meaning + "</p>";
    h += '<p class="info-related-label">' + groupLabelOf(CETASIKA_GROUPS, rec.group) + "</p>";
    if (bkt) h += '<p class="info-related-label">' + bkt.thai + "</p>";
    if (cats.length) {
      h += '<p class="info-related-label">' + s.cetasika.axis + " (" + cats.length + ")</p>" +
        '<div class="info-chips">' + cats.map((c) => chip(c, catThaiAny(c))).join("") + "</div>";
      h += '<p class="info-note">จิตที่เกิดร่วมได้ ' + computeRelated(sel).cittas.size + " ดวง</p>";
    } else {
      h += '<p class="info-note">ไม่จัดเข้าหมวดใด</p>';
    }
  } else if (sel.type === "cat") {
    const rel = computeRelated(sel);
    h += '<h3 class="info-title">' + catThaiAny(sel.id) + "</h3>";
    h += '<div class="info-chips">' + chip(sel.id, catThaiAny(sel.id)) + "</div>";
    const og = (s.ongkhatham || {})[sel.id];
    if (og && store.cetasikaById[og]) {
      h += '<p class="info-note">องค์ธรรม: ' + store.cetasikaById[og].thai + "เจตสิก</p>";
    }
    h += '<p class="info-note">จิต ' + rel.cittas.size + " ดวง · เจตสิกที่เกิดร่วมได้ " +
      rel.cetasikas.size + " ดวง</p>";
  }
  h += '<p class="clear-hint">' +
    (pinned ? "คลิกอีกครั้งหรือคลิกพื้นที่ว่างเพื่อล้าง" : "คลิกเพื่อตรึงไว้") + "</p>";
  el.info.innerHTML = h;
}

// ---------- events ----------

function samesel(a, b) { return !!a && !!b && a.type === b.type && a.id === b.id; }

document.addEventListener("click", (e) => {
  const schemeBtn = e.target.closest(".mode-btn");
  if (schemeBtn && !schemeBtn.disabled) {
    store.scheme = schemeBtn.dataset.scheme;
    store.pinned = store.hover = null;
    resetView();
    renderSchemeTabs();
    renderAll();
    return;
  }
  const viewBtn = e.target.closest(".subaxis-btn");
  if (viewBtn) {
    store.view = viewBtn.dataset.view;
    store.pinned = store.hover = null;
    renderAll();
    return;
  }
  const n = e.target.closest(".node");
  if (n) {
    const cur = { type: n.dataset.kind, id: n.dataset.id };
    store.pinned = samesel(store.pinned, cur) ? null : cur;
    store.hover = null;
    applyHighlight(); renderInfo();
    return;
  }
  const chipEl = e.target.closest(".cat-chip");
  if (chipEl) {
    const cur = { type: "cat", id: chipEl.dataset.cat };
    store.pinned = samesel(store.pinned, cur) ? null : cur;
    store.hover = null;
    applyHighlight(); renderInfo();
    return;
  }
  if (!e.target.closest("#info-panel")) {
    store.pinned = null;
    applyHighlight(); renderInfo();
  }
});

document.addEventListener("mouseover", (e) => {
  if (store.pinned) return;
  const n = e.target.closest(".node");
  const chipEl = e.target.closest(".cat-chip");
  const next = n ? { type: n.dataset.kind, id: n.dataset.id }
    : chipEl ? { type: "cat", id: chipEl.dataset.cat } : null;
  if (samesel(store.hover, next)) return;
  store.hover = next;
  applyHighlight(); renderInfo();
});

document.addEventListener("mouseout", (e) => {
  if (store.pinned || !store.hover) return;
  const to = e.relatedTarget;
  if (to && to.closest && (to.closest(".node") || to.closest(".cat-chip"))) return;
  store.hover = null;
  applyHighlight(); renderInfo();
});
