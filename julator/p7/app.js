// ปริจเฉทที่ ๗ สมุจจยสังคหะ -- bidirectional cross-reference tool.
//
// data/data.json carries data.p7 = { sangahas[], reverse } (built by
// scripts/build_data.py from data/p7.yaml). Four สังคหะ (อกุศล / มิสสก /
// โพธิปักขิย / สัพพ), 28 dhamma-sets, ~198 named members; each member lists its
// องค์ธรรม as ปรมัตถ์ ids. `reverse` maps ปรมัตถ์ id -> [{sangaha, set, member}].
//
// Left panel  : the dhamma-sets of the active สังคหะ (a tab switcher), each set a
//               header (ชื่อ + count_label) over its member chips.
// Right panel : every ปรมัตถ์ -- จิต ๑๒๑ / เจตสิก ๕๒ / รูป ๒๘ / นิพพาน ๑ -- in the
//               standard groups (จูฬตรี order), always all shown.
// Click/hover either side lights the other; the info panel shows องค์ธรรม detail
// + the set's คาถา. Selecting a ปรมัตถ์ whose sets are not under the active tab
// auto-switches to the first สังคหะ that contains it and badges every tab with
// its match count.
//
// Interaction model (pin on click, preview on hover) mirrors p3/app.js, but the
// two chapters' tools are separate on purpose -- p7 has no per-นัย axis, no
// partition/matrix cardinality, no category rail.

// ----- right-panel ปรมัตถ์ groups (จูฬตรี layout, shared with p3) -----
const CITTA_GROUPS = [
  { id: "lobha-mula", label: "โลภมูลจิต ๘", chunkSize: 4 },
  { id: "dosa-mula", label: "โทสมูลจิต ๒" },
  { id: "moha-mula", label: "โมหมูลจิต ๒" },
  { id: "ahetuka", label: "อเหตุกจิต ๑๘", rows: [7, 8, 3] },
  { id: "mahakusala", label: "มหากุศลจิต ๘", chunkSize: 4 },
  { id: "mahavipaka", label: "มหาวิปากจิต ๘", chunkSize: 4 },
  { id: "mahakiriya", label: "มหากิริยาจิต ๘", chunkSize: 4 },
  { id: "rupa-jhana", label: "รูปาวจรจิต ๑๕ (กุศล/วิบาก/กิริยา × ฌาน ๑-๕)", chunkSize: 5 },
  { id: "arupa-jhana", label: "อรูปาวจรจิต ๑๒ (กุศล/วิบาก/กิริยา × อรูปฌาน ๔)", chunkSize: 4 },
  { id: "lokuttara", label: "โลกุตตรจิต ๔๐ (พิสดาร, มรรค-ผล ๘ × ฌาน ๑-๕)", chunkSize: 5 },
];
const CETASIKA_GROUPS = [
  { id: "sabbacitta-sadharana", label: "สัพพจิตตสาธารณเจตสิก ๗" },
  { id: "pakinnaka", label: "ปกิณณกเจตสิก ๖" },
  { id: "moha-catuka", label: "โมจตุกเจตสิก ๔" },
  { id: "lobha-tika", label: "โลติกเจตสิก ๓" },
  { id: "dosa-catuka", label: "โทจตุกเจตสิก ๔" },
  { id: "thina-duka", label: "ถีทุกเจตสิก ๒" },
  { id: "vicikiccha", label: "วิจิกิจฉาเจตสิก ๑" },
  { id: "sobhana-sadharana", label: "โสภณสาธารณเจตสิก ๑๙" },
  { id: "virati", label: "วิรตีเจตสิก ๓" },
  { id: "appamanna", label: "อัปปมัญญาเจตสิก ๒" },
  { id: "pannindriya", label: "ปัญญินทรีย์เจตสิก ๑" },
];
const RUPA_GROUPS = [
  { id: "mahabhuta", label: "มหาภูตรูป ๔" },
  { id: "pasada", label: "ปสาทรูป ๕" },
  { id: "visaya", label: "วิสยรูป (โคจรรูป) ๔" },
  { id: "bhava", label: "ภาวรูป ๒" },
  { id: "hadaya", label: "หทยรูป ๑" },
  { id: "jivita", label: "ชีวิตรูป ๑" },
  { id: "ahara", label: "อาหารรูป ๑" },
  { id: "pariccheda", label: "ปริจเฉทรูป ๑" },
  { id: "vinnatti", label: "วิญญัตติรูป ๒" },
  { id: "vikara", label: "วิการรูป ๓" },
  { id: "lakkhana", label: "ลักขณรูป ๔" },
];
const NIBBANA_GROUP = [{ id: "nibbana", label: "นิพพาน ๑" }];

const RIGHT_SECTIONS = [
  { kind: "citta", title: "จิต", groups: CITTA_GROUPS },
  { kind: "cetasika", title: "เจตสิก", groups: CETASIKA_GROUPS },
  { kind: "rupa", title: "รูป", groups: RUPA_GROUPS },
  { kind: "nibbana", title: "นิพพาน", groups: NIBBANA_GROUP },
];

const el = {
  sangahaSwitch: document.getElementById("sangaha-switch"),
  setGroups: document.getElementById("set-groups"),
  paraGroups: document.getElementById("paramattha-groups"),
  info: document.getElementById("info-panel"),
  setCount: document.getElementById("set-count"),
  paraCount: document.getElementById("paramattha-count"),
};

const store = {
  sangahas: [], sangahaById: {},
  reverse: {},
  para: { citta: [], cetasika: [], rupa: [], nibbana: [] },
  paraById: {}, paraKind: {},
  memberByKey: {},   // "sg/set/mem" -> { member, set, sangaha }
  setByKey: {},      // "sg/set"     -> { set, sangaha }
  sangaha: null,
  pinned: null, hover: null,
};

fetch("../data/data.json")
  .then((r) => r.json())
  .then((data) => {
    store.sangahas = data.p7.sangahas || [];
    store.reverse = data.p7.reverse || {};
    store.sangahas.forEach((sg) => {
      store.sangahaById[sg.id] = sg;
      (sg.sets || []).forEach((st) => {
        store.setByKey[sg.id + "/" + st.id] = { set: st, sangaha: sg };
        (st.members || []).forEach((m) => {
          store.memberByKey[sg.id + "/" + st.id + "/" + m.id] = { member: m, set: st, sangaha: sg };
        });
      });
    });
    ["citta", "cetasika", "rupa", "nibbana"].forEach((k) => {
      store.para[k] = data.paramattha[k] || [];
      store.para[k].forEach((p) => { store.paraById[p.id] = p; store.paraKind[p.id] = k; });
    });
    store.sangaha = store.sangahas.length ? store.sangahas[0].id : null;

    const nSets = store.sangahas.reduce((n, sg) => n + (sg.sets || []).length, 0);
    const nMembers = Object.keys(store.memberByKey).length;
    const nPara = ["citta", "cetasika", "rupa", "nibbana"].reduce((n, k) => n + store.para[k].length, 0);
    el.setCount.textContent = "(" + nSets + " หมวด · " + nMembers + " องค์)";
    el.paraCount.textContent = "(" + nPara + ")";

    renderSangahaTabs();
    renderRightPanel();
    renderLeftPanel();
    renderInfo();
  })
  .catch((e) => {
    el.info.innerHTML = '<p class="info-placeholder">โหลดข้อมูลไม่สำเร็จ</p>';
    console.error(e);
  });

// ---------- helpers ----------

function sangaha() { return store.sangahaById[store.sangaha]; }
function activeSelection() { return store.pinned || store.hover; }
function memberKey(sgId, setId, memId) { return sgId + "/" + setId + "/" + memId; }
function setKey(sgId, setId) { return sgId + "/" + setId; }

function paraThai(id) {
  const p = store.paraById[id];
  return p ? p.thai : id;
}

// every set key (sg/set) that the given ปรมัตถ์ id appears in
function setsForPara(pid) {
  const out = [];
  (store.reverse[pid] || []).forEach((hit) => {
    const k = setKey(hit.sangaha, hit.set);
    if (!out.includes(k)) out.push(k);
  });
  return out;
}

// { paras:Set, members:Set (member keys), sets:Set (set keys) } implied by a selection
function computeRelated(sel) {
  const res = { paras: new Set(), members: new Set(), sets: new Set() };
  if (!sel) return res;

  if (sel.type === "member") {
    const rec = store.memberByKey[sel.id];
    if (!rec) return res;
    (rec.member.ongkhatham || []).forEach((pid) => res.paras.add(pid));
    res.sets.add(setKey(rec.sangaha.id, rec.set.id));
  } else if (sel.type === "set") {
    const rec = store.setByKey[sel.id];
    if (!rec) return res;
    res.sets.add(sel.id);
    (rec.set.members || []).forEach((m) => {
      res.members.add(memberKey(rec.sangaha.id, rec.set.id, m.id));
      (m.ongkhatham || []).forEach((pid) => res.paras.add(pid));
    });
  } else if (sel.type === "para") {
    res.paras.add(sel.id);
    (store.reverse[sel.id] || []).forEach((hit) => {
      res.members.add(memberKey(hit.sangaha, hit.set, hit.member));
      res.sets.add(setKey(hit.sangaha, hit.set));
    });
  }
  return res;
}

// per-สังคหะ count of members matching the active para selection (for tab badges)
function paraMatchCountsBySangaha(pid) {
  const counts = {};
  (store.reverse[pid] || []).forEach((hit) => {
    counts[hit.sangaha] = (counts[hit.sangaha] || 0) + 1;
  });
  return counts;
}

// ---------- rendering ----------

function renderSangahaTabs() {
  el.sangahaSwitch.innerHTML = "";
  const sel = activeSelection();
  const badges = sel && sel.type === "para" ? paraMatchCountsBySangaha(sel.id) : null;
  store.sangahas.forEach((sg) => {
    const b = document.createElement("button");
    b.className = "mode-btn" + (sg.id === store.sangaha ? " active" : "");
    b.dataset.sangaha = sg.id;
    const n = (sg.sets || []).length;
    let html = sg.thai + '<span class="mode-hint">' + n + " หมวด</span>";
    if (badges) {
      const c = badges[sg.id] || 0;
      html = sg.thai + '<span class="mode-hint">' + (c ? "ตรง " + c + " องค์" : "—") + "</span>";
      if (c) b.classList.add("has-match");
    }
    b.innerHTML = html;
    el.sangahaSwitch.appendChild(b);
  });
}

function renderLeftPanel() {
  const sg = sangaha();
  el.setGroups.innerHTML = "";
  if (!sg) { el.setGroups.innerHTML = '<p class="bucket-empty">ไม่มีข้อมูล</p>'; return; }

  (sg.sets || []).forEach((st) => {
    const block = document.createElement("div");
    block.className = "p7-set";

    const head = document.createElement("button");
    head.className = "p7-set-head";
    head.dataset.setkey = setKey(sg.id, st.id);
    head.innerHTML = "<span>" + st.thai + '</span><span class="p7-set-count">' +
      (st.count_label || (st.members || []).length) + "</span>";
    block.appendChild(head);

    const row = document.createElement("div");
    row.className = "p7-members";
    (st.members || []).forEach((m) => {
      const chip = document.createElement("button");
      chip.className = "p7-member";
      chip.dataset.memberkey = memberKey(sg.id, st.id, m.id);
      chip.dataset.setkey = setKey(sg.id, st.id);
      chip.textContent = m.thai;
      row.appendChild(chip);
    });
    block.appendChild(row);
    el.setGroups.appendChild(block);
  });
}

function nodeKindClass(kind) {
  return kind === "cetasika" ? " cetasika" : kind === "rupa" ? " rupa" : kind === "nibbana" ? " nibbana" : "";
}

function renderRightPanel() {
  el.paraGroups.innerHTML = "";
  RIGHT_SECTIONS.forEach((sec) => {
    const items = store.para[sec.kind];
    if (!items.length) return;
    const secWrap = document.createElement("div");
    secWrap.className = "p7-para-section";
    const secLabel = document.createElement("p");
    secLabel.className = "p7-para-section-label";
    secLabel.textContent = sec.title + " " + items.length;
    secWrap.appendChild(secLabel);

    sec.groups.forEach((g) => {
      const members = items.filter((p) => p.group === g.id);
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
        members.slice(i, i + size).forEach((p) => {
          const n = document.createElement("button");
          n.className = "node" + nodeKindClass(sec.kind);
          n.dataset.kind = "para";
          n.dataset.id = p.id;
          const lab = document.createElement("span");
          lab.className = "node-label";
          lab.textContent = p.thai;
          n.appendChild(lab);
          n.title = (p.pali ? p.pali + " — " : "") + "ปรากฏใน " + setsForPara(p.id).length + " หมวด";
          row.appendChild(n);
        });
        i += size;
        wrap.appendChild(row);
      });
      secWrap.appendChild(wrap);
    });
    el.paraGroups.appendChild(secWrap);
  });
}

function applyHighlight() {
  const sel = activeSelection();
  const rel = computeRelated(sel);

  // left: member chips + set heads
  document.querySelectorAll(".p7-member").forEach((c) => {
    c.classList.remove("is-dim", "is-related", "is-selected");
    if (!sel) return;
    if (sel.type === "member" && sel.id === c.dataset.memberkey) { c.classList.add("is-selected"); return; }
    c.classList.add(rel.members.has(c.dataset.memberkey) ? "is-related" : "is-dim");
  });
  document.querySelectorAll(".p7-set-head").forEach((h) => {
    h.classList.remove("is-dim", "is-related", "is-selected");
    if (!sel) return;
    if (sel.type === "set" && sel.id === h.dataset.setkey) { h.classList.add("is-selected"); return; }
    h.classList.add(rel.sets.has(h.dataset.setkey) ? "is-related" : "is-dim");
  });

  // right: ปรมัตถ์ nodes
  document.querySelectorAll(".node").forEach((n) => {
    n.classList.remove("is-dim", "is-related", "is-selected");
    if (!sel) return;
    if (sel.type === "para" && sel.id === n.dataset.id) { n.classList.add("is-selected"); return; }
    n.classList.add(rel.paras.has(n.dataset.id) ? "is-related" : "is-dim");
  });
}

// ---------- info panel ----------

function chipRow(ids) {
  if (!ids || !ids.length) return "<em>—</em>";
  return '<div class="info-chips">' + ids.map((id) =>
    '<span class="info-chip info-chip-' + (store.paraKind[id] || "citta") + '">' + paraThai(id) + "</span>").join("") + "</div>";
}
function groupLabel(kind, gid) {
  const src = kind === "citta" ? CITTA_GROUPS : kind === "cetasika" ? CETASIKA_GROUPS
    : kind === "rupa" ? RUPA_GROUPS : NIBBANA_GROUP;
  const g = src.find((x) => x.id === gid);
  return g ? g.label : gid;
}
const KIND_THAI = { citta: "จิต", cetasika: "เจตสิก", rupa: "รูป", nibbana: "นิพพาน" };

// Render a prose note as a bulleted list: each sentence (ending "." or "ฯ") is a
// top-level bullet; a spaced em-dash inside a sentence splits the trailing clause
// into a sub-bullet. A single-sentence note stays a plain <p class=cls>.
function noteHtml(text, cls) {
  const raw = (text || "").trim();
  cls = cls || "info-note";
  if (!raw) return "";
  const sentences = raw.replace(/([.ฯ])\s+/g, "$1\x00").split("\x00")
    .map((s) => s.trim()).filter(Boolean);
  if (sentences.length <= 1) return '<p class="' + cls + '">' + raw + "</p>";
  const li = (s) => {
    s = s.replace(/^[—–-]\s+/, "");
    const bits = s.split(/\s+[—–]\s+/);
    const head = bits.shift();
    const sub = bits.map((x) => "<li>" + x + "</li>").join("");
    return "<li>" + head + (sub ? "<ul>" + sub + "</ul>" : "") + "</li>";
  };
  return '<ul class="info-notelist">' + sentences.map(li).join("") + "</ul>";
}

function renderInfo() {
  const sel = activeSelection();
  const pinned = !!store.pinned;

  if (!sel) {
    const sg = sangaha();
    let h = '<h3 class="info-title">' + (sg ? sg.thai : "สมุจจยสังคหะ") + "</h3>";
    if (sg) {
      h += '<p class="info-related-label">' + (sg.sets || []).length + " หมวดธรรม · " +
        (sg.sets || []).reduce((n, s) => n + (s.members || []).length, 0) + " องค์</p>";
      if (sg.gatha) h += '<p class="info-gatha">' + sg.gatha + "</p>";
      h += noteHtml(sg.note);
    }
    h += '<p class="clear-hint">ชี้หรือคลิกที่หมวดธรรมทางซ้าย หรือปรมัตถ์ทางขวา เพื่อดูความสัมพันธ์</p>';
    el.info.innerHTML = h;
    return;
  }

  let h = "";
  if (sel.type === "member") {
    const rec = store.memberByKey[sel.id];
    h += '<h3 class="info-title">' + rec.member.thai + "</h3>";
    h += '<p class="info-related-label">' + rec.sangaha.thai + " › " + rec.set.thai +
      " " + (rec.set.count_label || "") + "</p>";
    if (rec.member.note) h += noteHtml(rec.member.note, "info-meaning");
    h += '<p class="info-related-label">องค์ธรรม (' + (rec.member.ongkhatham || []).length + " ปรมัตถ์)</p>" +
      chipRow(rec.member.ongkhatham);
    if (rec.set.gatha) h += '<p class="info-gatha">' + rec.set.gatha + "</p>";
    if (rec.set.source) h += '<p class="info-note">ที่มา: ' + rec.set.source + "</p>";
  } else if (sel.type === "set") {
    const rec = store.setByKey[sel.id];
    const st = rec.set;
    const ong = new Set();
    (st.members || []).forEach((m) => (m.ongkhatham || []).forEach((p) => ong.add(p)));
    h += '<h3 class="info-title">' + st.thai + " " + (st.count_label || "") + "</h3>";
    h += '<p class="info-related-label">' + rec.sangaha.thai + "</p>";
    if (st.gatha) h += '<p class="info-gatha">' + st.gatha + "</p>";
    h += noteHtml(st.note);
    h += '<p class="info-related-label">สมาชิก ' + (st.members || []).length + " องค์ · รวมองค์ธรรม " +
      ong.size + " ปรมัตถ์</p>";
    h += '<ul class="info-related-list">' +
      (st.members || []).map((m) => "<li>" + m.thai + "</li>").join("") + "</ul>";
    if (st.source) h += '<p class="info-note">ที่มา: ' + st.source + "</p>";
  } else if (sel.type === "para") {
    const p = store.paraById[sel.id];
    const kind = store.paraKind[sel.id];
    const hits = store.reverse[sel.id] || [];
    h += '<h3 class="info-title">' + p.thai + "</h3>";
    if (p.pali) h += '<p class="info-pali">' + p.pali + "</p>";
    if (p.meaning) h += '<p class="info-meaning">' + p.meaning + "</p>";
    h += '<p class="info-related-label">' + KIND_THAI[kind] + " — " + groupLabel(kind, p.group) + "</p>";
    // group hits by สังคหะ › set
    const bySg = {};
    hits.forEach((hit) => {
      (bySg[hit.sangaha] = bySg[hit.sangaha] || []).push(hit);
    });
    const nSets = new Set(hits.map((x) => x.sangaha + "/" + x.set)).size;
    h += '<p class="info-related-label">ปรากฏใน ' + nSets + " หมวด (" + hits.length + " แห่ง)</p>";
    h += '<ul class="info-related-list">';
    store.sangahas.forEach((sg) => {
      const list = bySg[sg.id];
      if (!list) return;
      h += "<li>" + sg.thai + '<ul class="info-related-sublist">' +
        list.map((hit) => {
          const srec = store.setByKey[hit.sangaha + "/" + hit.set];
          const mrec = store.memberByKey[hit.sangaha + "/" + hit.set + "/" + hit.member];
          return "<li>" + (srec ? srec.set.thai : hit.set) + " › " +
            (mrec ? mrec.member.thai : hit.member) + "</li>";
        }).join("") + "</ul></li>";
    });
    h += "</ul>";
  }
  h += '<p class="clear-hint">' +
    (pinned ? "คลิกอีกครั้งหรือคลิกพื้นที่ว่างเพื่อล้าง" : "คลิกเพื่อตรึงไว้") + "</p>";
  el.info.innerHTML = h;
}

function renderAll() {
  renderSangahaTabs();
  renderLeftPanel();
  applyHighlight();
  renderInfo();
}

// if a para selection has no matching member under the active tab, jump to the
// first สังคหะ that does (so the cross-highlight is actually visible)
function ensureSangahaShowsSelection() {
  const sel = activeSelection();
  if (!sel || sel.type !== "para") return;
  const counts = paraMatchCountsBySangaha(sel.id);
  if (counts[store.sangaha]) return;
  const first = store.sangahas.find((sg) => counts[sg.id]);
  if (first) store.sangaha = first.id;
}

// ---------- events ----------

function samesel(a, b) { return !!a && !!b && a.type === b.type && a.id === b.id; }

function pick(target) {
  const memberEl = target.closest(".p7-member");
  if (memberEl) return { type: "member", id: memberEl.dataset.memberkey };
  const headEl = target.closest(".p7-set-head");
  if (headEl) return { type: "set", id: headEl.dataset.setkey };
  const nodeEl = target.closest(".node");
  if (nodeEl) return { type: "para", id: nodeEl.dataset.id };
  return null;
}

document.addEventListener("click", (e) => {
  const tab = e.target.closest(".mode-btn");
  if (tab) {
    store.sangaha = tab.dataset.sangaha;
    store.pinned = store.hover = null;
    renderAll();
    return;
  }
  const cur = pick(e.target);
  if (cur) {
    store.pinned = samesel(store.pinned, cur) ? null : cur;
    store.hover = null;
    const before = store.sangaha;
    ensureSangahaShowsSelection();
    if (store.sangaha !== before) {
      renderAll(); // tab jumped -> left panel rebuilds
    } else {
      renderSangahaTabs(); applyHighlight(); renderInfo();
    }
    return;
  }
  if (!e.target.closest("#info-panel")) {
    store.pinned = null;
    renderSangahaTabs(); applyHighlight(); renderInfo();
  }
});

document.addEventListener("mouseover", (e) => {
  if (store.pinned) return;
  const next = pick(e.target);
  // no change (incl. both null when hovering empty space / the tab bar itself) --
  // bail before re-rendering, or a rebuild lands between mousedown and mouseup on
  // a สังคหะ tab and eats the click.
  if (next === store.hover || samesel(store.hover, next)) return;
  store.hover = next;
  // hover must not yank the tab out from under the pointer; only re-tab on click
  renderSangahaTabs();
  applyHighlight();
  renderInfo();
});

document.addEventListener("mouseout", (e) => {
  if (store.pinned || !store.hover) return;
  const to = e.relatedTarget;
  if (to && to.closest && (to.closest(".p7-member") || to.closest(".p7-set-head") || to.closest(".node"))) return;
  store.hover = null;
  renderSangahaTabs();
  applyHighlight();
  renderInfo();
});
