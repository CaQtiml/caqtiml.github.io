const CITTA_GROUPS = [
  { id: "lobha-mula", label: "โลภมูลจิต ๘ (รากเหง้าคือโลภะ)", prefix: "ล", chunkSize: 4 },
  { id: "dosa-mula", label: "โทสมูลจิต ๒ (รากเหง้าคือโทสะ)", prefix: "ท" },
  { id: "moha-mula", label: "โมหมูลจิต ๒ (รากเหง้าคือโมหะ)", prefix: "ม" },
  { id: "ahetuka", label: "อเหตุกจิต ๑๘ (ไม่มีเหตุ: ๗ อกุศลวิบาก, ๘ กุศลวิบาก, ๓ กิริยา)", prefix: "อห", rows: [7, 8, 3] },
  { id: "mahakusala", label: "มหากุศลจิต ๘ (กามาวจรโสภณ)", prefix: "กศ", chunkSize: 4 },
  { id: "mahavipaka", label: "มหาวิปากจิต ๘ (กามาวจรโสภณ)", prefix: "วบ", chunkSize: 4 },
  { id: "mahakiriya", label: "มหากิริยาจิต ๘ (กามาวจรโสภณ)", prefix: "กร", chunkSize: 4 },
  { id: "rupa-jhana", label: "รูปาวจรจิต ๑๕ (แถวละ กุศล/วิบาก/กิริยา × ฌาน ๑-๕)", prefix: "รป", chunkSize: 5 },
  { id: "arupa-jhana", label: "อรูปาวจรจิต ๑๒ (แถวละ กุศล/วิบาก/กิริยา × อรูปฌาน ๔)", prefix: "อร", chunkSize: 4 },
  { id: "lokuttara", label: "โลกุตตรจิต ๔๐ (พิสดาร, มรรค-ผล ๘ × ฌาน ๑-๕)", prefix: "ลก", chunkSize: 5 },
];

const CETASIKA_GROUPS = [
  { id: "sabbacitta-sadharana", label: "สัพพจิตตสาธารณเจตสิก ๗ — ประกอบกับจิตทุกดวง" },
  { id: "pakinnaka", label: "ปกิณณกเจตสิก ๖ — ประกอบเป็นบางครั้ง" },
  { id: "moha-catuka", label: "โมจตุกเจตสิก ๔ — ประกอบกับอกุศลจิตทุกดวง" },
  { id: "lobha-tika", label: "โลติกเจตสิก ๓ — เฉพาะโลภมูลจิต" },
  { id: "dosa-catuka", label: "โทจตุกเจตสิก ๔ — เฉพาะโทสมูลจิต" },
  { id: "thina-duka", label: "ถีทุกเจตสิก ๒ — เฉพาะจิตที่เป็นสสังขาริก" },
  { id: "vicikiccha", label: "วิจิกิจฉาเจตสิก ๑ — เฉพาะโมหมูลจิตดวงที่ ๑" },
  { id: "sobhana-sadharana", label: "โสภณสาธารณเจตสิก ๑๙ — ประกอบกับจิตที่ดีงามทุกดวง" },
  { id: "virati", label: "วิรตีเจตสิก ๓ — งดเว้นจากทุจริต (กุศล/กิริยาบางดวง)" },
  { id: "appamanna", label: "อัปปมัญญาเจตสิก ๒ — แผ่ไปในสัตว์ไม่มีประมาณ" },
  { id: "pannindriya", label: "ปัญญินทรีย์เจตสิก ๑ — ปัญญา" },
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
    // `rows` gives explicit, possibly-uneven row sizes (e.g. [7, 8, 3]); falls
    // back to uniform `chunkSize` rows, then to one single row.
    const rowSizes = g.rows || (g.chunkSize ? Array(Math.ceil(members.length / g.chunkSize)).fill(g.chunkSize) : [members.length]);
    wrap.appendChild(label);
    let i = 0;
    rowSizes.forEach((size) => {
      const row = document.createElement("div");
      row.className = "circle-row";
      members.slice(i, i + size).forEach((c, j) => {
        row.appendChild(makeNode("citta", c.id, `${g.prefix}.${i + j + 1}`, c.thai));
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
    const row = document.createElement("div");
    row.className = "circle-row";
    members.forEach((c) => {
      row.appendChild(makeNode("cetasika", c.id, c.thai, c.thai));
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

function showCittaInfo(citta) {
  const names = citta.cetasikas.map((id) => byId(DATA.cetasikas, id).thai);
  infoPanel.innerHTML = `
    <h3 class="info-title">${citta.thai}</h3>
    <p class="info-pali">${citta.pali}</p>
    <p class="info-meaning">มีเจตสิกประกอบ ${citta.cetasikas.length} ดวง (สังคหนัย)</p>
    <p class="info-related-label">เจตสิกที่ประกอบ:</p>
    <ul class="info-related-list">${names.map((n) => `<li>${n}</li>`).join("")}</ul>
  `;
}

function showCetasikaInfo(id, relatedCittaIds) {
  const ceta = byId(DATA.cetasikas, id);
  const cittaNames = relatedCittaIds.map((cid) => byId(DATA.cittas, cid).thai);
  infoPanel.innerHTML = `
    <h3 class="info-title">${ceta.thai}</h3>
    <p class="info-meaning">${ceta.meaning}</p>
    <p class="info-related-label">ประกอบได้ในจิต ${relatedCittaIds.length} ดวง (สัมปโยคนัย):</p>
    <ul class="info-related-list">${cittaNames.map((n) => `<li>${n}</li>`).join("")}</ul>
  `;
}

function showTadubhayaInfo(id, relatedCittaIds, relatedCetasikaIds) {
  const ceta = byId(DATA.cetasikas, id);
  const cittaNames = relatedCittaIds.map((cid) => byId(DATA.cittas, cid).thai);
  const cetaNames = relatedCetasikaIds.map((cid) => byId(DATA.cetasikas, cid).thai);
  infoPanel.innerHTML = `
    <h3 class="info-title">${ceta.thai}</h3>
    <p class="info-meaning">${ceta.meaning}</p>
    <p class="info-related-label">ประกอบได้ในจิต ${relatedCittaIds.length} ดวง (สัมปโยคนัย):</p>
    <ul class="info-related-list">${cittaNames.map((n) => `<li>${n}</li>`).join("")}</ul>
    <p class="info-related-label">เจตสิกที่ประกอบร่วมกันได้ ${relatedCetasikaIds.length} ดวง (ตทุภยมิสสกนัย):</p>
    <ul class="info-related-list">${cetaNames.map((n) => `<li>${n}</li>`).join("")}</ul>
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
    applyHighlight(null);
  });
});

fetch("data/data.json")
  .then((r) => r.json())
  .then((data) => {
    DATA = data;
    render();
  })
  .catch((err) => {
    infoPanel.innerHTML = `<p class="info-placeholder">โหลดข้อมูลไม่สำเร็จ: ${err.message}</p>`;
  });
