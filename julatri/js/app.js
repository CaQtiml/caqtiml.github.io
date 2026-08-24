const CITTA_GROUPS = [
  { id: "lobha-mula", label: "โลภมูลจิต ๘ (รากเหง้าคือโลภะ)", shortLabel: "โลภมูลจิต ๘", prefix: "ล", chunkSize: 4 },
  { id: "dosa-mula", label: "โทสมูลจิต ๒ (รากเหง้าคือโทสะ)", shortLabel: "โทสมูลจิต ๒", prefix: "ท" },
  { id: "moha-mula", label: "โมหมูลจิต ๒ (รากเหง้าคือโมหะ)", shortLabel: "โมหมูลจิต ๒", prefix: "ม" },
  { id: "ahetuka", label: "อเหตุกจิต ๑๘ (ไม่มีเหตุ: ๗ อกุศลวิบาก, ๘ กุศลวิบาก, ๓ กิริยา)", shortLabel: "อเหตุกจิต ๑๘", prefix: "อห", rows: [7, 8, 3] },
  { id: "mahakusala", label: "มหากุศลจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหากุศลจิต ๘", prefix: "กศ", chunkSize: 4 },
  { id: "mahavipaka", label: "มหาวิปากจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหาวิปากจิต ๘", prefix: "วบ", chunkSize: 4 },
  { id: "mahakiriya", label: "มหากิริยาจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหากิริยาจิต ๘", prefix: "กร", chunkSize: 4 },
  { id: "rupa-jhana", label: "รูปาวจรจิต ๑๕ (แถวละ กุศล/วิบาก/กิริยา × ฌาน ๑-๕)", shortLabel: "รูปาวจรจิต ๑๕", prefix: "รป", chunkSize: 5,
    etymology: "รูปสฺส ภโว = รูปํ (ภูมิที่เกิดแห่งวัตถุรูป/กิเลสรูป ชื่อว่ารูป) + รูเป อวจรตีติ = รูปาวจรํ (จิตที่ท่องเที่ยวเกิดในภูมินั้น)" },
  { id: "arupa-jhana", label: "อรูปาวจรจิต ๑๒ (แถวละ กุศล/วิบาก/กิริยา × อรูปฌาน ๔)", shortLabel: "อรูปาวจรจิต ๑๒", prefix: "อร", chunkSize: 4,
    etymology: "อรูปสฺส ภโว = อรูปํ (ภูมิที่เกิดแห่งวัตถุอรูป/กิเลสอรูป ชื่อว่าอรูป) + อรูเป อวจรตีติ = อรูปาวจรํ (จิตที่ท่องเที่ยวเกิดในภูมินั้น)" },
  { id: "lokuttara", label: "โลกุตตรจิต ๔๐ (พิสดาร, มรรค-ผล ๘ × ฌาน ๑-๕)", shortLabel: "โลกุตตรจิต ๔๐", prefix: "ลก", chunkSize: 5 },
];

const CETASIKA_GROUPS = [
  { id: "sabbacitta-sadharana", label: "สัพพจิตตสาธารณเจตสิก ๗ — ประกอบกับจิตทุกดวง", shortLabel: "สัพพจิตตสาธารณเจตสิก ๗",
    etymology: "สพฺพ (ทั้งหมด) + จิตฺต (จิต) + สาธารณ (ทั่วไป) = ทั่วไปแก่จิตทั้งหมด" },
  { id: "pakinnaka", label: "ปกิณณกเจตสิก ๖ — ประกอบเป็นบางครั้ง", shortLabel: "ปกิณณกเจตสิก ๖",
    etymology: "ป (โดยทั่วๆ ไป) + กิณฺณ (เรี่ยราย) + ก (ไม่มีเนื้อความเฉพาะ) = เรี่ยรายโดยทั่วๆ ไป (ประกอบทั่วไปแต่ไม่ใช่ทั้งหมด ต่างจากสัพพจิตตสาธารณะ)" },
  { id: "moha-catuka", label: "โมจตุกเจตสิก ๔ — ประกอบกับอกุศลจิตทุกดวง", shortLabel: "โมจตุกเจตสิก ๔",
    etymology: "โมห (ความหลง) + จตุก (หมวด ๔) = หมวด ๔ ที่ยกโมหเจตสิกเป็นประธาน" },
  { id: "lobha-tika", label: "โลติกเจตสิก ๓ — เฉพาะโลภมูลจิต", shortLabel: "โลติกเจตสิก ๓",
    etymology: "โลภ (ความติดใจ) + ติก (หมวด ๓) = หมวด ๓ ที่ยกโลภเจตสิกเป็นประธาน" },
  { id: "dosa-catuka", label: "โทจตุกเจตสิก ๔ — เฉพาะโทสมูลจิต", shortLabel: "โทจตุกเจตสิก ๔",
    etymology: "โทส (ความประทุษร้าย) + จตุก (หมวด ๔) = หมวด ๔ ที่ยกโทสเจตสิกเป็นประธาน" },
  { id: "thina-duka", label: "ถีทุกเจตสิก ๒ — เฉพาะจิตที่เป็นสสังขาริก", shortLabel: "ถีทุกเจตสิก ๒",
    etymology: "ถีน (ความหดหู่) + ทุก (หมวด ๒) = หมวด ๒ ของถีนะ-มิทธะ (ต้นฉบับไม่ได้แยกบทวจนัตถะไว้)" },
  { id: "vicikiccha", label: "วิจิกิจฉาเจตสิก ๑ — เฉพาะโมหมูลจิตดวงที่ ๑", shortLabel: "วิจิกิจฉาเจตสิก ๑",
    etymology: "มีเจตสิกดวงเดียวคือวิจิกิจฉา ชื่อกลุ่มตรงกับชื่อเจตสิกโดยตรง ไม่มีการแยกบทเพิ่มเติมในต้นฉบับ" },
  { id: "sobhana-sadharana", label: "โสภณสาธารณเจตสิก ๑๙ — ประกอบกับจิตที่ดีงามทุกดวง", shortLabel: "โสภณสาธารณเจตสิก ๑๙",
    etymology: "โสภณ (จิตที่มีความสวยงามอันไม่มีโทษ) + สาธารณ (ทั่วไป) = ทั่วไปในจิตที่มีความสวยงามอันไม่มีโทษ" },
  { id: "virati", label: "วิรตีเจตสิก ๓ — งดเว้นจากทุจริต (กุศล/กิริยาบางดวง)", shortLabel: "วิรตีเจตสิก ๓",
    etymology: "ชื่อว่าวิรตีเจตสิก เพราะมีเจตนาเว้นจากทุจริตเป็นประธาน" },
  { id: "appamanna", label: "อัปปมัญญาเจตสิก ๒ — แผ่ไปในสัตว์ไม่มีประมาณ", shortLabel: "อัปปมัญญาเจตสิก ๒",
    etymology: "ชื่อว่าอัปปมัญญาเจตสิก เพราะเกิดขึ้นโดยอาศัยทุกขิตสัตว์หรือสุขิตสัตว์ทั่วไป ไม่จำกัด (ไม่มีประมาณ)" },
  { id: "pannindriya", label: "ปัญญินทรีย์เจตสิก ๑ — ปัญญา", shortLabel: "ปัญญินทรีย์เจตสิก ๑",
    etymology: "ชื่อว่าปัญญินทรีย์ เพราะมีหน้าที่ปกครองในการรู้ต่างๆ โดยทั่วไปตามความเป็นจริง" },
];

let DATA = null;
let mode = "sangaha"; // 'sangaha' | 'sampayoga' | 'tadubhaya'
let pinned = null; // { type: 'citta'|'cetasika', id: string } | null

const cittaGroupsEl = document.getElementById("citta-groups");
const cetasikaGroupsEl = document.getElementById("cetasika-groups");
const infoPanel = document.getElementById("info-panel");
const cittaPanel = document.getElementById("citta-panel");
const cetasikaPanel = document.getElementById("cetasika-panel");

function activeSourceType() {
  return mode === "sangaha" ? "citta" : "cetasika";
}

function byId(list, id) {
  return list.find((x) => x.id === id);
}

// The number shown on a เจตสิก circle depends on the active mode: the
// สัมปโยคนัย count (how many จิต it occurs in) normally, but the
// ตทุภยมิสสกนัย count (how many OTHER เจตสิก it co-occurs with) in that mode,
// since that's the relation ตทุภยมิสสกนัย actually measures.
function cetasikaCircleLabel(id) {
  const list = mode === "tadubhaya" ? DATA.cooccurrence[id] : DATA.cetasikaToCittas[id];
  return String((list || []).length);
}

// ตทุภยมิสสกนัย is a เจตสิก<->เจตสิก relation - จิต isn't part of what it
// measures, so its circles show no number in that mode (they're only ever
// dimmed context there, never a value-bearing target).
function cittaCircleLabel(citta) {
  return mode === "tadubhaya" ? "" : String(citta.count);
}

function updateCittaLabels() {
  document.querySelectorAll('.node[data-type="citta"]').forEach((el) => {
    el.textContent = cittaCircleLabel(byId(DATA.cittas, el.dataset.id));
  });
}

function updateCetasikaLabels() {
  document.querySelectorAll('.node[data-type="cetasika"]').forEach((el) => {
    el.textContent = cetasikaCircleLabel(el.dataset.id);
  });
}

function render() {
  document.getElementById("citta-count").textContent = `(${DATA.cittas.length})`;
  document.getElementById("cetasika-count").textContent = `(${DATA.cetasikas.length})`;

  cittaGroupsEl.innerHTML = "";
  CITTA_GROUPS.forEach((g) => {
    const members = DATA.cittas.filter((c) => c.group === g.id);
    if (!members.length) return;
    const wrap = document.createElement("div");
    wrap.className = "citta-group";
    const label = document.createElement("p");
    label.className = "group-label";
    label.textContent = g.label;
    if (g.etymology) label.title = g.etymology;
    // `rows` gives explicit, possibly-uneven row sizes (e.g. [7, 8, 3]); falls
    // back to uniform `chunkSize` rows, then to one single row.
    const rowSizes = g.rows || (g.chunkSize ? Array(Math.ceil(members.length / g.chunkSize)).fill(g.chunkSize) : [members.length]);
    wrap.appendChild(label);
    let i = 0;
    rowSizes.forEach((size) => {
      const row = document.createElement("div");
      row.className = "circle-row";
      members.slice(i, i + size).forEach((c, j) => {
        row.appendChild(makeNode("citta", c.id, cittaCircleLabel(c), c.thai));
      });
      i += size;
      wrap.appendChild(row);
    });
    cittaGroupsEl.appendChild(wrap);
  });

  cetasikaGroupsEl.innerHTML = "";
  CETASIKA_GROUPS.forEach((g) => {
    const members = DATA.cetasikas.filter((c) => c.group === g.id);
    if (!members.length) return;
    const wrap = document.createElement("div");
    wrap.className = "cetasika-group";
    const label = document.createElement("p");
    label.className = "group-label";
    label.textContent = g.label;
    if (g.etymology) label.title = g.etymology;
    const row = document.createElement("div");
    row.className = "circle-row";
    members.forEach((c) => {
      row.appendChild(makeNode("cetasika", c.id, cetasikaCircleLabel(c.id), c.thai));
    });
    wrap.appendChild(label);
    wrap.appendChild(row);
    cetasikaGroupsEl.appendChild(wrap);
  });

  updateActivePanelStyling();
  applyHighlight(pinned);
}

function makeNode(type, id, shortLabel, title) {
  const el = document.createElement("div");
  el.className = "node" + (type === "cetasika" ? " cetasika" : "");
  el.dataset.type = type;
  el.dataset.id = id;
  el.title = title;
  el.textContent = shortLabel;
  el.addEventListener("mouseenter", () => {
    if (type === activeSourceType()) applyHighlight({ type, id });
  });
  el.addEventListener("mouseleave", () => {
    applyHighlight(pinned);
  });
  el.addEventListener("click", () => {
    if (type !== activeSourceType()) return;
    if (pinned && pinned.type === type && pinned.id === id) {
      pinned = null;
    } else {
      pinned = { type, id };
    }
    applyHighlight(pinned);
  });
  return el;
}

function updateActivePanelStyling() {
  const sourceType = activeSourceType();
  cittaPanel.classList.toggle("inactive-panel", sourceType !== "citta");
  cetasikaPanel.classList.toggle("inactive-panel", sourceType !== "cetasika" && mode !== "sampayoga" && mode !== "sangaha");
  // cetasika panel is always a valid *target*; only its clickability changes
  document.querySelectorAll('.node[data-type="citta"]').forEach((el) => {
    el.style.cursor = sourceType === "citta" ? "pointer" : "default";
  });
  document.querySelectorAll('.node[data-type="cetasika"]').forEach((el) => {
    el.style.cursor = sourceType === "cetasika" ? "pointer" : "default";
  });
}

function clearHighlight() {
  document.querySelectorAll(".node").forEach((el) => {
    el.classList.remove("is-dim", "is-related", "is-selected");
  });
}

function applyHighlight(selection) {
  clearHighlight();
  if (!selection) {
    showInfoPlaceholder();
    return;
  }
  const { type, id } = selection;

  if (mode === "sangaha" && type === "citta") {
    const citta = byId(DATA.cittas, id);
    highlightSet("citta", [id], true);
    highlightSet("cetasika", citta.cetasikas, false);
    dimUnrelated("cetasika", citta.cetasikas);
    dimUnrelated("citta", [id]);
    showCittaInfo(citta);
  } else if (mode === "sampayoga" && type === "cetasika") {
    const relatedCittas = DATA.cetasikaToCittas[id] || [];
    highlightSet("cetasika", [id], true);
    highlightSet("citta", relatedCittas, false);
    dimUnrelated("citta", relatedCittas);
    dimUnrelated("cetasika", [id]);
    showCetasikaInfo(id, relatedCittas);
  } else if (mode === "tadubhaya" && type === "cetasika") {
    const relatedCetasikas = DATA.cooccurrence[id] || [];
    const relatedCittas = DATA.cetasikaToCittas[id] || [];
    highlightSet("cetasika", [id], true);
    highlightSet("cetasika", relatedCetasikas, false);
    dimUnrelated("cetasika", [id, ...relatedCetasikas]);
    highlightSet("citta", relatedCittas, false);
    dimUnrelated("citta", relatedCittas);
    showTadubhayaInfo(id, relatedCittas, relatedCetasikas);
  }
}

function highlightSet(type, ids, isSelected) {
  ids.forEach((id) => {
    const el = document.querySelector(`.node[data-type="${type}"][data-id="${id}"]`);
    if (el) el.classList.add(isSelected ? "is-selected" : "is-related");
  });
}

function dimUnrelated(type, keepIds) {
  document.querySelectorAll(`.node[data-type="${type}"]`).forEach((el) => {
    if (!keepIds.includes(el.dataset.id)) el.classList.add("is-dim");
  });
}

function dimAll(type) {
  document.querySelectorAll(`.node[data-type="${type}"]`).forEach((el) => {
    el.classList.add("is-dim");
  });
}

function showInfoPlaceholder() {
  infoPanel.innerHTML = '<p class="info-placeholder">ชี้หรือคลิกที่วงกลมจิตหรือเจตสิก เพื่อดูความสัมพันธ์</p>';
}

// Summarizes a list of related ids by their CITTA_GROUPS/CETASIKA_GROUPS
// membership, so a full group collapses to one bullet ("สัพพจิตตสาธารณเจตสิก ๗
// (ครบทั้งหมด)") instead of listing all 7 names -- a partial group instead
// gets a nested sub-list naming exactly which members are included.
function summarizeByGroup(ids, groupDefs, allItems) {
  const idSet = new Set(ids);
  const groups = [];
  groupDefs.forEach((g) => {
    const groupMembers = allItems.filter((x) => x.group === g.id);
    const present = groupMembers.filter((x) => idSet.has(x.id));
    if (!present.length) return;
    const isFull = present.length === groupMembers.length;
    groups.push({
      label: isFull ? `${g.shortLabel} (ครบทั้งหมด)` : `${g.shortLabel} (${present.length}/${groupMembers.length} ดวง)`,
      members: isFull ? null : present.map((x) => x.thai),
    });
  });
  return groups;
}

// Renders summarizeByGroup's output as a <ul>, with a nested <ul> sub-list of
// member names under any group that isn't fully included.
function renderGroupList(groups) {
  return `<ul class="info-related-list">${groups
    .map(
      (g) => `<li>${g.label}${
        g.members ? `<ul class="info-related-sublist">${g.members.map((n) => `<li>${n}</li>`).join("")}</ul>` : ""
      }</li>`
    )
    .join("")}</ul>`;
}

function showCittaInfo(citta) {
  const groups = summarizeByGroup(citta.cetasikas, CETASIKA_GROUPS, DATA.cetasikas);
  infoPanel.innerHTML = `
    <h3 class="info-title">${citta.thai}</h3>
    <p class="info-pali">${citta.pali}</p>
    <p class="info-meaning">มีเจตสิกประกอบ ${citta.cetasikas.length} ดวง (สังคหนัย)</p>
    <p class="info-related-label">เจตสิกที่ประกอบ (ตามหมวด):</p>
    ${renderGroupList(groups)}
  `;
}

// นิยตโยคี/อนิยตโยคี: renders an extra explanatory line for the 11 cetasikas
// that don't accompany their citta unconditionally -- see CONTEXT.md and the
// "เน้นตาม (เจตสิก)" overlay in สัมปโยคนัย mode, which is where this is browsable now.

// อธิบายพิเศษ/เกจิวาทะ: collapsed-by-default asides for the handful of cetasikas
// that have one, via native <details> (no extra toggle wiring needed).
function footnotesHtml(ceta) {
  if (!ceta.footnotes || !ceta.footnotes.length) return "";
  return ceta.footnotes
    .map(
      (fn) => `
    <details class="info-footnote">
      <summary>อธิบายเพิ่มเติม: ${fn.title}</summary>
      <p>${fn.body}</p>
    </details>`
    )
    .join("");
}

function showCetasikaInfo(id, relatedCittaIds) {
  const ceta = byId(DATA.cetasikas, id);
  const groups = summarizeByGroup(relatedCittaIds, CITTA_GROUPS, DATA.cittas);
  infoPanel.innerHTML = `
    <h3 class="info-title">${ceta.thai}</h3>
    <p class="info-meaning">${ceta.meaning}</p>
    <p class="info-related-label">ประกอบได้ในจิต ${relatedCittaIds.length} ดวง (สัมปโยคนัย, ตามหมวด):</p>
    ${renderGroupList(groups)}
    ${footnotesHtml(ceta)}
  `;
}

function showTadubhayaInfo(id, relatedCittaIds, relatedCetasikaIds) {
  const ceta = byId(DATA.cetasikas, id);
  const cittaGroups = summarizeByGroup(relatedCittaIds, CITTA_GROUPS, DATA.cittas);
  const cetaGroups = summarizeByGroup(relatedCetasikaIds, CETASIKA_GROUPS, DATA.cetasikas);
  infoPanel.innerHTML = `
    <h3 class="info-title">${ceta.thai}</h3>
    <p class="info-meaning">${ceta.meaning}</p>
    <p class="info-related-label">เจตสิกที่ประกอบร่วมกันได้ ${relatedCetasikaIds.length} ดวง (ตทุภยมิสสกนัย, ตามหมวด):</p>
    ${renderGroupList(cetaGroups)}
    <p class="info-related-label">ประกอบได้ในจิต ${relatedCittaIds.length} ดวง (สัมปโยคนัย, ตามหมวด):</p>
    ${renderGroupList(cittaGroups)}
    ${footnotesHtml(ceta)}
  `;
}

document.querySelectorAll(".mode-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    mode = btn.dataset.mode;
    pinned = null;
    updateActivePanelStyling();
    updateCetasikaLabels();
    updateCittaLabels();
    applyHighlight(null);
    updateLensAvailability();
    updateComboAvailability();
  });
});

// จำแนกนัย overlay: available in สังคหนัย mode only -- a lens filter's meaning
// is "which cittas fall in this category," and highlighting their สังคหนัย
// cetasikas alongside them is what makes the filter legible; that citta->cetasika
// direction doesn't hold the same way in the other 2 modes, so the control is
// hidden there (see updateLensAvailability below).
const LENS_LABELS = {
  jati: "ชาติเภทนัย (อกุศล/กุศล/วิบาก/กริยา)",
  bhumi: "ภูมิเภทนัย (กาม/รูป/อรูป/โลกุตตร)",
  sobhana: "โสภณเภทนัย (อโสภณ/โสภณ)",
  loka: "โลกเภทนัย (โลกีย/โลกุตตร)",
  hetu: "เหตุเภทนัย (อเหตุก/สเหตุก)",
  jhana: "ฌานเภทนัย (อฌาน/ฌาน)",
  vedana: "เวทนาเภทนัย (สุข/ทุกข์/โสมนัส/โทมนัส/อุเบกขา)",
  sankhara: "สังขารเภทนัย (อสังขาริก/สสังขาริก)",
};

const lensOverlayEl = document.getElementById("lens-overlay");
const lensSelect = document.getElementById("lens-select");
const lensCategorySelect = document.getElementById("lens-category-select");
const lensClearBtn = document.getElementById("lens-clear");

function updateLensAvailability() {
  const available = mode === "sangaha";
  lensOverlayEl.hidden = !available;
  if (!available) {
    lensSelect.value = "";
    populateLensCategories("");
    applyLensOverlay();
  }
}

Object.keys(LENS_LABELS).forEach((key) => {
  const opt = document.createElement("option");
  opt.value = key;
  opt.textContent = LENS_LABELS[key];
  lensSelect.appendChild(opt);
});

function populateLensCategories(lens) {
  lensCategorySelect.innerHTML = "";
  if (!lens || !DATA) {
    lensCategorySelect.disabled = true;
    lensClearBtn.disabled = true;
    return;
  }
  const values = new Set(Object.values(DATA.cittaLenses).map((v) => v[lens]));
  [...values].sort().forEach((v) => {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    lensCategorySelect.appendChild(opt);
  });
  lensCategorySelect.disabled = false;
  lensClearBtn.disabled = false;
}

function applyLensOverlay() {
  const lens = lensSelect.value;
  const category = lensCategorySelect.value;
  const active = mode === "sangaha" && lens && category && DATA;

  // Every เจตสิก that appears (สังคหนัย) in at least one matched จิต -- this is
  // what makes the filter answer "which เจตสิก does this category actually
  // involve," not just "which circles are highlighted."
  const matchedCetasikaIds = new Set();

  document.querySelectorAll('.node[data-type="citta"]').forEach((el) => {
    el.classList.remove("lens-match", "lens-nomatch");
    if (!active) return;
    const lensValues = DATA.cittaLenses[el.dataset.id];
    const isMatch = lensValues && lensValues[lens] === category;
    el.classList.add(isMatch ? "lens-match" : "lens-nomatch");
    if (isMatch) {
      byId(DATA.cittas, el.dataset.id).cetasikas.forEach((cid) => matchedCetasikaIds.add(cid));
    }
  });

  document.querySelectorAll('.node[data-type="cetasika"]').forEach((el) => {
    el.classList.remove("lens-match", "lens-nomatch");
    if (!active) return;
    el.classList.add(matchedCetasikaIds.has(el.dataset.id) ? "lens-match" : "lens-nomatch");
  });
}

lensSelect.addEventListener("change", () => {
  populateLensCategories(lensSelect.value);
  applyLensOverlay();
});
lensCategorySelect.addEventListener("change", applyLensOverlay);
lensClearBtn.addEventListener("click", () => {
  lensSelect.value = "";
  populateLensCategories("");
  applyLensOverlay();
});

updateLensAvailability();

// นิยตโยคี/อนิยตโยคี overlay: available in สัมปโยคนัย mode only -- เจตสิก is
// the source type there (see activeSourceType()), so highlighting เจตสิก
// circles by an intrinsic property is consistent with what that mode is
// already for; สังคหนัย/ตทุภยมิสสกนัย treat เจตสิก as a target or a
// cetasika<->cetasika relation instead, so the control is hidden there.
const comboOverlayEl = document.getElementById("combo-overlay");

function updateComboAvailability() {
  const available = mode === "sampayoga";
  comboOverlayEl.hidden = !available;
  if (!available) {
    comboSelect.value = "";
    applyComboOverlay();
  }
}

const COMBINATION_LABELS = {
  niyata: "นิยตโยคี (ประกอบแน่นอน)",
  kadaci: "กทาจิ (ประกอบไม่แน่นอน, ตามลำพัง)",
  "nana-kadaci": "นานากทาจิ (ประกอบไม่แน่นอน, ไม่พร้อมกับพี่น้อง)",
  "saha-kadaci": "สหกทาจิ (ประกอบไม่แน่นอน, แต่พร้อมกันเป็นคู่)",
};

const comboSelect = document.getElementById("combo-select");
const comboClearBtn = document.getElementById("combo-clear");

Object.keys(COMBINATION_LABELS).forEach((key) => {
  const opt = document.createElement("option");
  opt.value = key;
  opt.textContent = COMBINATION_LABELS[key];
  comboSelect.appendChild(opt);
});

function cetasikaComboCategory(ceta) {
  return ceta.combination_type || "niyata";
}

function applyComboOverlay() {
  const category = comboSelect.value;
  comboClearBtn.disabled = !category;

  // Every จิต that appears (สัมปโยคนัย) in at least one matched เจตสิก -- mirrors
  // the จิต lens overlay's matched-cetasika logic, just in the other direction.
  const matchedCittaIds = new Set();

  document.querySelectorAll('.node[data-type="cetasika"]').forEach((el) => {
    el.classList.remove("combo-match", "combo-nomatch");
    if (!category || !DATA) return;
    const ceta = byId(DATA.cetasikas, el.dataset.id);
    const isMatch = cetasikaComboCategory(ceta) === category;
    el.classList.add(isMatch ? "combo-match" : "combo-nomatch");
    if (isMatch) {
      (DATA.cetasikaToCittas[el.dataset.id] || []).forEach((cid) => matchedCittaIds.add(cid));
    }
  });

  document.querySelectorAll('.node[data-type="citta"]').forEach((el) => {
    el.classList.remove("combo-match", "combo-nomatch");
    if (!category || !DATA) return;
    el.classList.add(matchedCittaIds.has(el.dataset.id) ? "combo-match" : "combo-nomatch");
  });
}

comboSelect.addEventListener("change", applyComboOverlay);
comboClearBtn.addEventListener("click", () => {
  comboSelect.value = "";
  applyComboOverlay();
});

updateComboAvailability();

fetch("data/data.json")
  .then((r) => r.json())
  .then((data) => {
    DATA = data;
    render();
  })
  .catch((err) => {
    infoPanel.innerHTML = `<p class="info-placeholder">โหลดข้อมูลไม่สำเร็จ: ${err.message}</p>`;
  });
