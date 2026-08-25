// RUPA_GROUPS: 11 fine-grained subgroups, in source order. Groups 1-7 are the
// นิปผันนรูป bucket (18 total), groups 8-11 are the อนิปผันนรูป bucket (10
// total) -- the boundary falls cleanly between group 7 and group 8, so the two
// always-visible bounding boxes below are just nested containers around that
// split, no highlight-overlay state needed (see CONTEXT.md).
const RUPA_GROUPS = [
  { id: "mahabhuta", label: "มหาภูตรูป ๔", shortLabel: "มหาภูตรูป ๔", bucket: "nipphanna",
    etymology: "มหนฺตานิ หุตฺวา ภูตานิ ปาตุภูตานีติ = มหาภูตานิ — รูปที่เป็นใหญ่และปรากฏชัด" },
  { id: "pasada", label: "ปสาทรูป ๕", shortLabel: "ปสาทรูป ๕", bucket: "nipphanna",
    etymology: "ปสีทตีติ = ปสาโท — รูปที่มีความใส สามารถรับอารมณ์ของตนๆ ได้" },
  { id: "visaya", label: "วิสยรูป ๔", shortLabel: "วิสยรูป ๔", bucket: "nipphanna",
    etymology: "หมายเหตุ: แหล่งข้อมูลนับ \"๗ หรือ ๔\" — โผฏฐัพพารมณ์ ๓ เป็นสารัตถะเดียวกับปถวี/เตโช/วาโย (มหาภูตรูป) จึงไม่นับซ้ำเป็นวงกลมใหม่ที่นี่" },
  { id: "bhava", label: "ภาวรูป ๒", shortLabel: "ภาวรูป ๒", bucket: "nipphanna" },
  { id: "hadaya", label: "หทยรูป ๑", shortLabel: "หทยรูป ๑", bucket: "nipphanna" },
  { id: "jivita", label: "ชีวิตรูป ๑", shortLabel: "ชีวิตรูป ๑", bucket: "nipphanna" },
  { id: "ahara", label: "อาหารรูป ๑", shortLabel: "อาหารรูป ๑", bucket: "nipphanna" },
  { id: "pariccheda", label: "ปริจเฉทรูป ๑", shortLabel: "ปริจเฉทรูป ๑", bucket: "anipphanna" },
  { id: "vinnatti", label: "วิญญัติรูป ๒", shortLabel: "วิญญัติรูป ๒", bucket: "anipphanna" },
  { id: "vikara", label: "วิการรูป ๓", shortLabel: "วิการรูป ๓", bucket: "anipphanna",
    etymology: "หมายเหตุ: แหล่งข้อมูลนับ \"๕ หรือ ๓\" — อีกนัยหนึ่งนับกายวิญญัติ/วจีวิญญัติ (วิญญัติรูป ๒) ซ้ำเข้าในวิการรูปด้วย" },
  { id: "lakkhana", label: "ลักขณรูป ๔", shortLabel: "ลักขณรูป ๔", bucket: "anipphanna" },
];

// 5 synonym names for the 18 นิปผันนรูป (line 132-138) and the opposite 5 for
// the 10 อนิปผันนรูป (line 140-146) -- derived from which bucket a รูป is in,
// not stored per-item.
const BUCKET_ALT_NAMES = {
  nipphanna: [
    ["สภาวรูป", "รูปที่มีสภาวะของตนๆ"],
    ["สลักขณรูป", "รูปที่มีลักษณะ คือ อนิจจะ ทุกขะ อนัตตะ"],
    ["นิปผันนรูป", "รูปที่เกิดขึ้นจาก กรรม จิต อุตุ อาหาร"],
    ["รูปรูป", "รูปที่มีการเสื่อมสิ้นสลายไป"],
    ["สัมมสนรูป", "รูปที่พระโยคีบุคคลพิจารณาโดยความเป็นอนิจจัง ทุกขัง อนัตตาได้"],
  ],
  anipphanna: [
    ["อสภาวรูป", "รูปที่ไม่มีสภาวะของตนๆ"],
    ["อสลักขณรูป", "รูปที่ไม่มีลักษณะ อนิจจะ ทุกขะ อนัตตะ"],
    ["อนิปผันนรูป", "รูปที่ไม่ได้เกิดขึ้นจาก กรรม จิต อุตุ อาหาร"],
    ["อรูปรูป", "รูปที่ไม่มีการเสื่อมสิ้นสลายไป"],
    ["อสัมมสนรูป", "รูปที่พระโยคีบุคคลพิจารณาโดยความเป็นอนิจจัง ทุกขัง อนัตตาไม่ได้"],
  ],
};

const BUCKET_LABEL = { nipphanna: "นิปผันนรูป ๑๘", anipphanna: "อนิปผันนรูป ๑๐" };

// รูปวิภาคนัย: 11 คู่ (ch.6 lines 561-703) -- an intrinsic per-รูป categorical
// attribute, same shape as จำแนกนัย ๙ for จิต, so it's a lens-overlay filter
// on the existing grid rather than a new panel (see CONTEXT.md).
const RUPA_VIBHAGA_LABELS = {
  ajjhattika: "๑. อัชฌัตติกรูป / พาหิรรูป (รูปภายใน-ภายนอก)",
  vatthu: "๒. วัตถุรูป / อวัตถุรูป (ที่อาศัยเกิดของจิตเจตสิก)",
  dvara: "๓. ทวารรูป / อทวารรูป (เหตุเกิดวิถีจิต/กายกรรมวจีกรรม)",
  indriya: "๔. อินทริยรูป / อนินทริยรูป (เป็นใหญ่เป็นผู้ปกครอง)",
  olarika: "๕. โอฬาริกรูป / สุขุมรูป (หยาบ-ละเอียด)",
  santike: "๖. สันติเกรูป / ทูเรรูป (ใกล้-ไกล)",
  sappatigha: "๗. สัปปฏิฆรูป / อัปปฏิฆรูป (กระทบกันได้-ไม่ได้)",
  upadinna: "๘. อุปาทินนรูป / อนุปาทินนรูป (เกิดจากกรรมหรือไม่)",
  sanidassana: "๙. สนิทัสสนรูป / อนิทัสสนรูป (เห็นด้วยตาได้-ไม่ได้)",
  gocaraggahaka: "๑๐. โคจรัคคาหกรูป / อโคจรัคคาหกรูป (รับปัญจารมณ์ได้-ไม่ได้)",
  avinibbhoga: "๑๑. อวินิพโภครูป / วินิพโภครูป (แยกกันไม่ได้-ได้)",
};

// CITTA_GROUPS: duplicated from js/app.js (not shared via a module system) --
// only needed here to lay out the 121 จิต circles in จิตตชรูปนัย mode the
// same way index.html does. Keep in sync if that constant changes there.
const CITTA_GROUPS = [
  { id: "lobha-mula", label: "โลภมูลจิต ๘ (รากเหง้าคือโลภะ)", shortLabel: "โลภมูลจิต ๘", prefix: "ล", chunkSize: 4 },
  { id: "dosa-mula", label: "โทสมูลจิต ๒ (รากเหง้าคือโทสะ)", shortLabel: "โทสมูลจิต ๒", prefix: "ท" },
  { id: "moha-mula", label: "โมหมูลจิต ๒ (รากเหง้าคือโมหะ)", shortLabel: "โมหมูลจิต ๒", prefix: "ม" },
  { id: "ahetuka", label: "อเหตุกจิต ๑๘ (ไม่มีเหตุ: ๗ อกุศลวิบาก, ๘ กุศลวิบาก, ๓ กิริยา)", shortLabel: "อเหตุกจิต ๑๘", prefix: "อห", rows: [7, 8, 3] },
  { id: "mahakusala", label: "มหากุศลจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหากุศลจิต ๘", prefix: "กศ", chunkSize: 4 },
  { id: "mahavipaka", label: "มหาวิปากจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหาวิปากจิต ๘", prefix: "วบ", chunkSize: 4 },
  { id: "mahakiriya", label: "มหากิริยาจิต ๘ (กามาวจรโสภณ)", shortLabel: "มหากิริยาจิต ๘", prefix: "กร", chunkSize: 4 },
  { id: "rupa-jhana", label: "รูปาวจรจิต ๑๕ (แถวละ กุศล/วิบาก/กิริยา × ฌาน ๑-๕)", shortLabel: "รูปาวจรจิต ๑๕", prefix: "รป", chunkSize: 5 },
  { id: "arupa-jhana", label: "อรูปาวจรจิต ๑๒ (แถวละ กุศล/วิบาก/กิริยา × อรูปฌาน ๔)", shortLabel: "อรูปาวจรจิต ๑๒", prefix: "อร", chunkSize: 4 },
  { id: "lokuttara", label: "โลกุตตรจิต ๔๐ (พิสดาร, มรรค-ผล ๘ × ฌาน ๑-๕)", shortLabel: "โลกุตตรจิต ๔๐", prefix: "ลก", chunkSize: 5 },
];

let DATA = null;
let selectedId = null;
let rupaMode = "summary"; // 'summary' | 'samutthana' | 'cittaja'
let pinned = null; // { type: 'rupa'|'cause'|'activity'|'citta', id: string } | null

const rupaGroupsEl = document.getElementById("rupa-groups");
const infoPanel = document.getElementById("info-panel");
const rupaPanel = document.getElementById("rupa-panel");
const samutthanaPanel = document.getElementById("samutthana-panel");
const samutthanaGroupsEl = document.getElementById("samutthana-groups");
const samutthanaLegend = document.getElementById("samutthana-legend");
const cittajaActivityPanel = document.getElementById("cittaja-activity-panel");
const cittajaActivityGroupsEl = document.getElementById("cittaja-activity-groups");
const cittajaCittaPanel = document.getElementById("cittaja-citta-panel");
const cittajaCittaGroupsEl = document.getElementById("cittaja-citta-groups");

function byId(id) {
  return DATA.rupas.find((r) => r.id === id);
}

function groupDef(id) {
  return RUPA_GROUPS.find((g) => g.id === id);
}

function cittaById(id) {
  return DATA.cittas.find((c) => c.id === id);
}

function render() {
  document.getElementById("rupa-count").textContent = `(${DATA.rupas.length})`;

  rupaGroupsEl.innerHTML = "";
  let currentBucket = null;
  let bucketWrap = null;

  RUPA_GROUPS.forEach((g) => {
    const members = DATA.rupas.filter((r) => r.group === g.id).sort((a, b) => a.order - b.order);
    if (!members.length) return;

    if (g.bucket !== currentBucket) {
      currentBucket = g.bucket;
      bucketWrap = document.createElement("div");
      bucketWrap.className = "rupa-bucket";
      const bucketLabel = document.createElement("p");
      bucketLabel.className = "bucket-label";
      bucketLabel.textContent = BUCKET_LABEL[currentBucket];
      bucketWrap.appendChild(bucketLabel);
      rupaGroupsEl.appendChild(bucketWrap);
    }

    const wrap = document.createElement("div");
    wrap.className = "rupa-group";
    const label = document.createElement("p");
    label.className = "group-label";
    label.textContent = g.label;
    if (g.etymology) label.title = g.etymology;
    wrap.appendChild(label);

    const row = document.createElement("div");
    row.className = "circle-row";
    members.forEach((r) => {
      row.appendChild(makeNode(r));
    });
    wrap.appendChild(row);
    bucketWrap.appendChild(wrap);
  });

  applySelection();
}

function makeNode(rupa) {
  const el = document.createElement("div");
  el.className = "node rupa-node";
  el.dataset.id = rupa.id;
  el.title = rupa.thai;
  el.textContent = rupa.thai;
  el.addEventListener("click", () => {
    if (rupaMode === "summary") {
      selectedId = selectedId === rupa.id ? null : rupa.id;
      applySelection();
    } else if (rupaMode === "samutthana") {
      togglePinned("rupa", rupa.id);
    }
  });
  return el;
}

function applySelection() {
  if (rupaMode !== "summary") return;
  document.querySelectorAll(".rupa-node").forEach((el) => {
    el.classList.toggle("is-selected", el.dataset.id === selectedId);
  });
  if (!selectedId) {
    showInfoPlaceholder();
  } else {
    showRupaInfo(byId(selectedId));
  }
}

function showInfoPlaceholder() {
  infoPanel.innerHTML = '<p class="info-placeholder">คลิกที่วงกลมรูป เพื่อดูรายละเอียด</p>';
}

function altNamesHtml(bucket) {
  const names = BUCKET_ALT_NAMES[bucket];
  return `
    <p class="info-related-label">ชื่ออื่นของ${BUCKET_LABEL[bucket]}:</p>
    <ul class="info-related-list">
      ${names.map(([name, gloss]) => `<li><strong>${name}</strong> — ${gloss}</li>`).join("")}
    </ul>
  `;
}

function showRupaInfo(rupa) {
  const g = groupDef(rupa.group);
  infoPanel.innerHTML = `
    <h3 class="info-title">${rupa.thai}</h3>
    <p class="info-pali">${g.label}</p>
    <p class="info-related-label">องค์ธรรม:</p>
    <p class="info-meaning">${rupa.ongkhatham}</p>
    <p class="info-related-label">ที่เกิด:</p>
    <p class="info-meaning">${rupa.thiKoet}</p>
    ${rupa.kicha ? `<p class="info-related-label">กิจ:</p><p class="info-meaning">${rupa.kicha}</p>` : ""}
    <p class="info-related-label">วจนัตถะ:</p>
    <p class="info-meaning">${rupa.etymology}</p>
    <p class="info-related-label">อธิบายสภาวลักษณะ:</p>
    <p class="info-meaning">${rupa.description}</p>
    ${altNamesHtml(g.bucket)}
  `;
}

// --- shared highlight helpers (used by samutthana + cittaja modes) ---

function clearNodeStates(selector) {
  document.querySelectorAll(selector).forEach((el) => {
    el.classList.remove("is-dim", "is-related", "is-selected");
  });
}

function highlightSet(selector, ids, isSelected) {
  ids.forEach((id) => {
    const el = document.querySelector(`${selector}[data-id="${id}"]`);
    if (el) el.classList.add(isSelected ? "is-selected" : "is-related");
  });
}

function dimUnrelated(selector, keepIds) {
  document.querySelectorAll(selector).forEach((el) => {
    if (!keepIds.includes(el.dataset.id)) el.classList.add("is-dim");
  });
}

function togglePinned(type, id) {
  pinned = pinned && pinned.type === type && pinned.id === id ? null : { type, id };
  if (rupaMode === "samutthana") applySamutthanaHighlight();
  else if (rupaMode === "cittaja") applyCittajaHighlight();
}

// --- รูปสมุฏฐานนัย (causal origin, bidirectional) ---

function renderSamutthanaPanel() {
  samutthanaGroupsEl.innerHTML = "";
  DATA.rupaSamutthanaCauses.forEach((cause) => {
    const el = document.createElement("div");
    el.className = "node cause-node";
    el.dataset.id = cause.key;
    el.title = cause.label;
    el.textContent = cause.label;
    el.addEventListener("click", () => togglePinned("cause", cause.key));
    samutthanaGroupsEl.appendChild(el);
  });
}

// Always-on 3-way border coding, independent of click state (see CONTEXT.md).
function applySamutthanaBorders(active) {
  document.querySelectorAll(".rupa-node").forEach((el) => {
    el.classList.remove("samutthana-ekanta", "samutthana-anekanta", "samutthana-nakutoci");
    if (!active) return;
    const cls = DATA.rupaSamutthana[el.dataset.id].class;
    if (cls === "เอกันตะ") el.classList.add("samutthana-ekanta");
    else if (cls === "อเนกันตะ") el.classList.add("samutthana-anekanta");
    else el.classList.add("samutthana-nakutoci");
  });
}

function applySamutthanaHighlight() {
  clearNodeStates(".rupa-node");
  clearNodeStates(".cause-node");
  if (!pinned) {
    showInfoPlaceholder();
    return;
  }
  const { type, id } = pinned;
  if (type === "rupa") {
    const causes = DATA.rupaSamutthana[id].causes;
    highlightSet(".rupa-node", [id], true);
    highlightSet(".cause-node", causes, false);
    dimUnrelated(".cause-node", causes);
    dimUnrelated(".rupa-node", [id]);
    showSamutthanaRupaInfo(id, causes);
  } else if (type === "cause") {
    const rupaIds = DATA.rupas.filter((r) => DATA.rupaSamutthana[r.id].causes.includes(id)).map((r) => r.id);
    if (id === "nakutoci") {
      DATA.rupas.forEach((r) => {
        if (DATA.rupaSamutthana[r.id].class === "นกุโตจิ") rupaIds.push(r.id);
      });
    }
    highlightSet(".cause-node", [id], true);
    highlightSet(".rupa-node", rupaIds, false);
    dimUnrelated(".rupa-node", rupaIds);
    dimUnrelated(".cause-node", [id]);
    showSamutthanaCauseInfo(id, rupaIds);
  }
}

function showSamutthanaRupaInfo(rupaId, causeKeys) {
  const rupa = byId(rupaId);
  const causeLabels = causeKeys.map((k) => DATA.rupaSamutthanaCauses.find((c) => c.key === k).label);
  const cls = DATA.rupaSamutthana[rupaId].class;
  infoPanel.innerHTML = `
    <h3 class="info-title">${rupa.thai}</h3>
    <p class="info-meaning">จำแนก: ${cls}</p>
    <p class="info-related-label">เกิดจากสมุฏฐาน:</p>
    <ul class="info-related-list">${
      causeLabels.length ? causeLabels.map((l) => `<li>${l}</li>`).join("") : "<li>ไม่มีสมุฏฐาน (นกุโตจิสมุฏฐานิกรูป)</li>"
    }</ul>
  `;
}

function showSamutthanaCauseInfo(causeKey, rupaIds) {
  const cause = DATA.rupaSamutthanaCauses.find((c) => c.key === causeKey);
  const groups = summarizeByGroup(rupaIds, RUPA_GROUPS, DATA.rupas);
  infoPanel.innerHTML = `
    <h3 class="info-title">${cause.label}</h3>
    <p class="info-related-label">ทำให้รูปเกิด ${rupaIds.length} รูป (ตามหมวด):</p>
    ${renderGroupList(groups)}
  `;
}

// Summarizes a list of ids by group membership (mirrors js/app.js's
// summarizeByGroup/renderGroupList -- duplicated here for the same
// no-shared-module reason as CITTA_GROUPS above).
function summarizeByGroup(ids, groupDefs, allItems) {
  const idSet = new Set(ids);
  const groups = [];
  groupDefs.forEach((g) => {
    const groupMembers = allItems.filter((x) => x.group === g.id);
    const present = groupMembers.filter((x) => idSet.has(x.id));
    if (!present.length) return;
    const isFull = present.length === groupMembers.length;
    groups.push({
      label: isFull ? `${g.shortLabel} (ครบทั้งหมด)` : `${g.shortLabel} (${present.length}/${groupMembers.length})`,
      members: isFull ? null : present.map((x) => x.thai),
    });
  });
  return groups;
}

function renderGroupList(groups) {
  return `<ul class="info-related-list">${groups
    .map(
      (g) => `<li>${g.label}${
        g.members ? `<ul class="info-related-sublist">${g.members.map((n) => `<li>${n}</li>`).join("")}</ul>` : ""
      }</li>`
    )
    .join("")}</ul>`;
}

// --- จิตตชรูปนัย (coarse: จิต <-> 7 activity labels, bidirectional) ---

function renderCittajaPanels() {
  cittajaActivityGroupsEl.innerHTML = "";
  DATA.cittajaActivities.forEach((activity) => {
    const el = document.createElement("div");
    el.className = "node activity-node";
    el.dataset.id = activity.key;
    el.title = activity.label;
    el.textContent = activity.label;
    el.addEventListener("click", () => togglePinned("activity", activity.key));
    cittajaActivityGroupsEl.appendChild(el);
  });

  document.getElementById("cittaja-citta-count").textContent = `(${DATA.cittas.length})`;
  cittajaCittaGroupsEl.innerHTML = "";
  CITTA_GROUPS.forEach((g) => {
    const members = DATA.cittas.filter((c) => c.group === g.id);
    if (!members.length) return;
    const wrap = document.createElement("div");
    wrap.className = "citta-group";
    const label = document.createElement("p");
    label.className = "group-label";
    label.textContent = g.label;
    wrap.appendChild(label);
    const rowSizes = g.rows || (g.chunkSize ? Array(Math.ceil(members.length / g.chunkSize)).fill(g.chunkSize) : [members.length]);
    let i = 0;
    rowSizes.forEach((size) => {
      const row = document.createElement("div");
      row.className = "circle-row";
      members.slice(i, i + size).forEach((c) => {
        const el = document.createElement("div");
        el.className = "node citta-node";
        el.dataset.id = c.id;
        el.title = c.thai;
        el.textContent = c.thai;
        const eligible = DATA.cittaEligibility[c.id];
        if (!eligible) {
          el.classList.add("is-ineligible");
        } else {
          el.addEventListener("click", () => togglePinned("citta", c.id));
        }
        row.appendChild(el);
      });
      i += size;
      wrap.appendChild(row);
    });
    cittajaCittaGroupsEl.appendChild(wrap);
  });
}

function applyCittajaHighlight() {
  clearNodeStates(".activity-node");
  clearNodeStates(".citta-node");
  if (!pinned) {
    showInfoPlaceholder();
    return;
  }
  const { type, id } = pinned;
  if (type === "activity") {
    const activity = DATA.cittajaActivities.find((a) => a.key === id);
    highlightSet(".activity-node", [id], true);
    highlightSet(".citta-node", activity.cittaIds, false);
    dimUnrelated(".citta-node", activity.cittaIds);
    dimUnrelated(".activity-node", [id]);
    showCittajaActivityInfo(activity);
  } else if (type === "citta") {
    const activityKeys = DATA.cittajaActivities.filter((a) => a.cittaIds.includes(id)).map((a) => a.key);
    highlightSet(".citta-node", [id], true);
    highlightSet(".activity-node", activityKeys, false);
    dimUnrelated(".activity-node", activityKeys);
    dimUnrelated(".citta-node", [id]);
    showCittajaCittaInfo(id, activityKeys);
  }
}

function showCittajaActivityInfo(activity) {
  const groups = summarizeByGroup(activity.cittaIds, CITTA_GROUPS, DATA.cittas);
  infoPanel.innerHTML = `
    <h3 class="info-title">${activity.label}</h3>
    <p class="info-related-label">เกิดจากจิต ${activity.cittaIds.length} ดวง (ตามหมวด):</p>
    ${renderGroupList(groups)}
  `;
}

function showCittajaCittaInfo(cittaId, activityKeys) {
  const citta = cittaById(cittaId);
  const labels = activityKeys.map((k) => DATA.cittajaActivities.find((a) => a.key === k).label);
  infoPanel.innerHTML = `
    <h3 class="info-title">${citta.thai}</h3>
    <p class="info-pali">${citta.pali}</p>
    <p class="info-related-label">ทำให้จิตตชรูปเกิด (กิจ):</p>
    <ul class="info-related-list">${labels.map((l) => `<li>${l}</li>`).join("")}</ul>
  `;
}

// --- mode switching ---

function updateModeVisibility() {
  rupaPanel.hidden = rupaMode === "cittaja";
  samutthanaPanel.hidden = rupaMode !== "samutthana";
  cittajaActivityPanel.hidden = rupaMode !== "cittaja";
  cittajaCittaPanel.hidden = rupaMode !== "cittaja";
  document.getElementById("rupa-lens-overlay").hidden = rupaMode !== "summary";
  samutthanaLegend.hidden = rupaMode !== "samutthana";
  document.querySelector("main.rupa-main").classList.toggle("mode-cittaja", rupaMode === "cittaja");
}

document.querySelectorAll(".mode-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    rupaMode = btn.dataset.mode;
    selectedId = null;
    pinned = null;
    updateModeVisibility();
    clearNodeStates(".rupa-node");
    applySamutthanaBorders(rupaMode === "samutthana");
    if (rupaMode === "summary") {
      applySelection();
      applyVibhagaOverlay();
    } else if (rupaMode === "samutthana") {
      applySamutthanaHighlight();
    } else if (rupaMode === "cittaja") {
      applyCittajaHighlight();
    }
  });
});

const vibhagaSelect = document.getElementById("rupa-lens-select");
const vibhagaCategorySelect = document.getElementById("rupa-lens-category-select");
const vibhagaClearBtn = document.getElementById("rupa-lens-clear");

Object.keys(RUPA_VIBHAGA_LABELS).forEach((key) => {
  const opt = document.createElement("option");
  opt.value = key;
  opt.textContent = RUPA_VIBHAGA_LABELS[key];
  vibhagaSelect.appendChild(opt);
});

function populateVibhagaCategories(pairKey) {
  vibhagaCategorySelect.innerHTML = "";
  if (!pairKey || !DATA) {
    vibhagaCategorySelect.disabled = true;
    vibhagaClearBtn.disabled = true;
    return;
  }
  const values = new Set(Object.values(DATA.rupaLenses).map((v) => v[pairKey]));
  [...values].forEach((v) => {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    vibhagaCategorySelect.appendChild(opt);
  });
  vibhagaCategorySelect.disabled = false;
  vibhagaClearBtn.disabled = false;
}

function applyVibhagaOverlay() {
  const pairKey = vibhagaSelect.value;
  const category = vibhagaCategorySelect.value;
  const active = pairKey && category && DATA;

  document.querySelectorAll(".rupa-node").forEach((el) => {
    el.classList.remove("lens-match", "lens-nomatch");
    if (!active) return;
    const isMatch = DATA.rupaLenses[el.dataset.id][pairKey] === category;
    el.classList.add(isMatch ? "lens-match" : "lens-nomatch");
  });
}

vibhagaSelect.addEventListener("change", () => {
  populateVibhagaCategories(vibhagaSelect.value);
  applyVibhagaOverlay();
});
vibhagaCategorySelect.addEventListener("change", applyVibhagaOverlay);
vibhagaClearBtn.addEventListener("click", () => {
  vibhagaSelect.value = "";
  populateVibhagaCategories("");
  applyVibhagaOverlay();
});

fetch("data/data.json")
  .then((r) => r.json())
  .then((data) => {
    DATA = data;
    render();
    applyVibhagaOverlay();
    renderSamutthanaPanel();
    renderCittajaPanels();
    updateModeVisibility();
  })
  .catch((err) => {
    infoPanel.innerHTML = `<p class="info-placeholder">โหลดข้อมูลไม่สำเร็จ: ${err.message}</p>`;
  });
