// Minimal DOM/fetch shim to execute p3/app.js headlessly and assert the render
// for every built scheme.  Run: node scripts/test_p3_render.js
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
for (const id of ["scheme-switch", "subaxis-switch", "citta-groups", "cetasika-groups", "cat-rail", "info-panel", "citta-count", "cetasika-count"]) {
  const e = new El("div"); e._domId = id; byId[id] = e;
}
global.fetch = () => Promise.resolve({ json: () => Promise.resolve(data) });

require(path.join(ROOT, "p3/app.js"));

let failed = 0;
const ok = (c, m) => { if (!c) { console.error("FAIL:", m); failed++; } else console.log("ok:", m); };
const all = (root, sel) => root._all((c) => matchOne(c, sel), []);
const fire = (ev, target) => global.document._listeners[ev].forEach((fn) =>
  fn({ target: { closest: (s) => target.closest(s) } }));
const distBy = (nodes, key) => {
  const d = {};
  nodes.forEach((n) => (d[n.dataset[key]] = (d[n.dataset[key]] || 0) + 1));
  return d;
};

setTimeout(() => {
  // ============ shared shell ============
  const schemeBtns = byId["scheme-switch"].children;
  ok(schemeBtns.length === 6, "6 scheme tabs");
  ok(schemeBtns.filter((b) => b.disabled).length === 0, "0 tabs disabled (all 6 นัย built)");
  ["hetu", "kicca", "dvara", "arammana", "vatthu"].forEach((s) =>
    ok(!schemeBtns.find((b) => b.dataset.scheme === s).disabled, s + " tab enabled"));
  ok(/<ul class="info-notelist">/.test(byId["info-panel"].innerHTML)
     && /<li><strong>จิต<\/strong>/.test(byId["info-panel"].innerHTML)
     && /<ul><li>/.test(byId["info-panel"].innerHTML),
     "vedana: explanation box renders as a nested bulleted list");

  // ============ เวทนาสังคหะ (default, partition จิต) ============
  ok(byId["subaxis-switch"].children.length === 2 && !byId["subaxis-switch"].hidden, "เวทนา ๓/๕ toggle shown");
  ok(byId["citta-groups"].children.length === 10, "vedana: 10 จิต groups");
  let cittaNodes = all(byId["citta-groups"], ".node");
  ok(cittaNodes.length === 121, "vedana: 121 จิต nodes");
  ok(cittaNodes.every((n) => n.dataset.cat), "vedana: every จิต node tinted (partition -> data-cat)");
  ok(all(byId["citta-groups"].children[0], ".circle-row").length === 2, "vedana: โลภมูลจิต ๘ in 2 rows");
  ok(all(byId["citta-groups"].children[3], ".circle-row").map((r) => r.children.length).join(",") === "7,8,3",
     "vedana: อเหตุกจิต rows = 7,8,3");
  ok(byId["cetasika-groups"].children.length === 11, "vedana: 11 เจตสิก groups");
  ok(all(byId["cetasika-groups"], ".node").length === 52, "vedana: 52 เจตสิก nodes");
  ok(all(byId["cetasika-groups"], ".node").every((n) => n.dataset.nset !== undefined),
     "vedana: เจตสิก nodes are matrix (data-nset)");
  ok(byId["cat-rail"].children.length === 5, "vedana: 5 category chips");
  {
    const d = distBy(cittaNodes, "cat");
    ok(d.somanassa === 62 && d.upekkha === 55 && d.domanassa === 2 && d.dukkha === 1 && d.sukha === 1,
       "vedana: จิต by เวทนา ๕ = 62/55/2/1/1 (" + JSON.stringify(d) + ")");
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "lobhamula-1");
    fire("click", target);
    const sel = all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-selected"));
    ok(sel.length === 1 && sel[0].dataset.id === "lobhamula-1", "vedana: clicked citta is-selected");
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 61,
       "vedana: 61 sibling โสมนัส จิต highlighted");
    ok(all(byId["cetasika-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 46,
       "vedana: 46 เจตสิก co-occur with โสมนัส");
    ok(/โลภมูลจิต ๘/.test(byId["info-panel"].innerHTML), "vedana: info shows the จิต group label");
    fire("click", target); // unpin
  }
  {
    fire("click", byId["subaxis-switch"].children.find((b) => b.dataset.view === "vedana3"));
    ok(byId["cat-rail"].children.length === 3, "vedana ๓: 3 category chips");
    const d = distBy(all(byId["citta-groups"], ".node"), "cat");
    ok(d.sukha === 63 && d.dukkha === 3 && d.upekkha === 55, "vedana ๓: จิต = 63/3/55 (" + JSON.stringify(d) + ")");
    fire("click", byId["subaxis-switch"].children.find((b) => b.dataset.view === "vedana5"));
  }

  // ============ เหตุสังคหะ (matrix จิต + matrix เจตสิก over เหตุ ๖) ============
  fire("click", schemeBtns.find((b) => b.dataset.scheme === "hetu"));
  ok(byId["subaxis-switch"].hidden, "hetu: no sub-toggle");
  ok(byId["cat-rail"].children.length === 6, "hetu: 6 เหตุ chips");
  ok(byId["cat-rail"].children.map((c) => c.dataset.cat).join(",") === "lobha,dosa,moha,alobha,adosa,amoha",
     "hetu: rail order = โลภ โทส โมห อโลภ อโทส อโมห");

  cittaNodes = all(byId["citta-groups"], ".node");
  ok(cittaNodes.length === 121, "hetu: 121 จิต nodes");
  ok(cittaNodes.every((n) => n.dataset.nset !== undefined && n.dataset.cat === undefined),
     "hetu: จิต nodes are matrix (data-nset, no data-cat tint)");
  {
    const d = distBy(cittaNodes, "nset");
    ok(d[0] === 18 && d[1] === 2 && d[2] === 22 && d[3] === 79,
       "hetu: จิต by เหตุ set-size = 18/2/22/79 (" + JSON.stringify(d) + ")");
  }
  {
    const cetaNodes = all(byId["cetasika-groups"], ".node");
    ok(cetaNodes.length === 52, "hetu: 52 เจตสิก nodes");
    const d = distBy(cetaNodes, "nset");
    ok(d[1] === 3 && d[2] === 9 && d[3] === 27 && d[5] === 1 && d[6] === 12 && d[0] === undefined && d[4] === undefined,
       "hetu: เจตสิก by เหตุ set-size = 3/9/27/1/12 (" + JSON.stringify(d) + ")");
  }
  {
    // rail chip counts: โมหเหตุ -> จิต 12, เจต 26 ; อโลภเหตุ -> จิต 91, เจต 37
    const moha = byId["cat-rail"].children.find((c) => c.dataset.cat === "moha");
    ok(/จิต 12 · เจต 26/.test(moha.innerHTML), "hetu: โมหเหตุ chip = จิต 12 · เจต 26 (" + moha.innerHTML + ")");
    const alobha = byId["cat-rail"].children.find((c) => c.dataset.cat === "alobha");
    ok(/จิต 91 · เจต 37/.test(alobha.innerHTML), "hetu: อโลภเหตุ chip = จิต 91 · เจต 37");
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "lobhamula-1"); // เหตุ {โลภ, โมห}
    fire("click", target);
    ok(target.dataset.nset === "2", "hetu: โลภมูลจิต ดวงที่ ๑ has 2 เหตุ");
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 11,
       "hetu: 11 other จิต share โลภ/โมห (โลภมูล ๘ + โทสมูล ๒ + โมหมูล ๒ − self)");
    ok(all(byId["cetasika-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 27,
       "hetu: 27 เจตสิก co-arise with โลภ or โมห");
    ok(/ทวิเหตุกจิต/.test(byId["info-panel"].innerHTML), "hetu: info shows the ทวิเหตุก bucket");
    ok(/โลภมูลจิต ๘/.test(byId["info-panel"].innerHTML), "hetu: info shows the จิต group label");
    fire("click", target);
  }
  {
    // ปีติเจตสิก -> เหตุ ๕ (เว้นโทสเหตุ)
    const piti = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "piti");
    ok(piti.dataset.nset === "5", "hetu: ปีติเจตสิก has 5 เหตุ");
    // อัญญสมาน (e.g. phassa) -> เหตุ ๖
    const phassa = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "phassa");
    ok(phassa.dataset.nset === "6", "hetu: ผัสสเจตสิก has 6 เหตุ");
  }

  // ============ กิจจสังคหะ (matrix จิต + matrix เจตสิก over กิจ ๑๔) ============
  fire("click", schemeBtns.find((b) => b.dataset.scheme === "kicca"));
  ok(byId["subaxis-switch"].hidden, "kicca: no sub-toggle");
  ok(byId["cat-rail"].children.length === 14, "kicca: 14 กิจ chips");
  ok(byId["cat-rail"].children[0].dataset.cat === "patisandhi"
     && byId["cat-rail"].children[11].dataset.cat === "javana",
     "kicca: rail in textbook order (patisandhi ... javana ... cuti)");
  cittaNodes = all(byId["citta-groups"], ".node");
  ok(cittaNodes.length === 121 && cittaNodes.every((n) => n.dataset.nset !== undefined && n.dataset.cat === undefined),
     "kicca: 121 จิต nodes, all matrix");
  {
    const d = distBy(cittaNodes, "nset");
    ok(d[1] === 100 && d[2] === 2 && d[3] === 9 && d[4] === 8 && d[5] === 2,
       "kicca: จิต by กิจ set-size = 100/2/9/8/2 (" + JSON.stringify(d) + ")");
  }
  {
    const d = distBy(all(byId["cetasika-groups"], ".node"), "nset");
    ok(d[1] === 17 && d[4] === 2 && d[5] === 21 && d[6] === 1 && d[7] === 1 && d[9] === 3 && d[14] === 7,
       "kicca: เจตสิก by กิจ set-size = 17/2/21/1/1/3/7 (" + JSON.stringify(d) + ")");
  }
  {
    const javana = byId["cat-rail"].children.find((c) => c.dataset.cat === "javana");
    ok(/จิต 87 · เจต 52/.test(javana.innerHTML), "kicca: ชวนกิจ chip = จิต 87 · เจต 52 (" + javana.innerHTML + ")");
    const patis = byId["cat-rail"].children.find((c) => c.dataset.cat === "patisandhi");
    ok(/จิต 19 · เจต 35/.test(patis.innerHTML), "kicca: ปฏิสนธิกิจ chip = จิต 19 · เจต 35");
  }
  {
    const santirana = cittaNodes.find((n) => n.dataset.id === "ahetuka-kusalavipaka-upekkhasantirana");
    ok(santirana.dataset.nset === "5", "kicca: อุเบกขาสันตีรณจิต ทำ ๕ กิจ");
    const phassa = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "phassa");
    ok(phassa.dataset.nset === "14", "kicca: ผัสสเจตสิก ทำครบ ๑๔ กิจ");
    const vitakka = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "vitakka");
    ok(vitakka.dataset.nset === "9", "kicca: วิตกเจตสิก ทำ ๙ กิจ (ตำราพาดหัว ๘ แต่แจกแจง ๙)");
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "mahavipaka-1"); // กิจ {patisandhi,bhavanga,cuti,tadarammana}
    fire("click", target);
    ok(target.dataset.nset === "4", "kicca: มหาวิปากจิต ดวงที่ ๑ ทำ ๔ กิจ");
    ok(/จิตทำ ๔ กิจ/.test(byId["info-panel"].innerHTML), "kicca: info shows the ๔-กิจ bucket");
    fire("click", target);
  }

  // ============ ทวารสังคหะ (matrix จิต + matrix เจตสิก over ทวาร ๖) ============
  fire("click", schemeBtns.find((b) => b.dataset.scheme === "dvara"));
  ok(byId["cat-rail"].children.length === 6, "dvara: 6 ทวาร chips");
  ok(byId["cat-rail"].children.map((c) => c.dataset.cat).join(",") === "cakkhu,sota,ghana,jivha,kaya,mano",
     "dvara: rail order = จักขุ โสต ฆาน ชิวหา กาย มโน");
  cittaNodes = all(byId["citta-groups"], ".node");
  {
    const d = distBy(cittaNodes, "nset");
    ok(d[0] === 9 && d[1] === 68 && d[5] === 3 && d[6] === 41,
       "dvara: จิต by ทวาร set-size = 9/68/3/41 (" + JSON.stringify(d) + ")");
  }
  {
    const d = distBy(all(byId["cetasika-groups"], ".node"), "nset");
    ok(d[1] === 2 && d[6] === 50 && d[0] === undefined,
       "dvara: เจตสิก by ทวาร set-size = 2/50 (" + JSON.stringify(d) + ")");
  }
  {
    const mano = byId["cat-rail"].children.find((c) => c.dataset.cat === "mano");
    ok(/จิต 99 · เจต 52/.test(mano.innerHTML), "dvara: มโนทวาร chip = จิต 99 · เจต 52 (" + mano.innerHTML + ")");
    const cakkhu = byId["cat-rail"].children.find((c) => c.dataset.cat === "cakkhu");
    ok(/จิต 46 · เจต 50/.test(cakkhu.innerHTML), "dvara: จักขุทวาร chip = จิต 46 · เจต 50");
  }
  {
    const mv = cittaNodes.find((n) => n.dataset.id === "rupa-ปฐมฌาน-vipaka");
    ok(mv.dataset.nset === "0", "dvara: มหัคคตวิปากจิต = ทวารวิมุตต (set-size 0)");
    const karuna = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "karuna");
    ok(karuna.dataset.nset === "1", "dvara: กรุณาเจตสิก (อัปปมัญญา) เกิดทวารเดียว");
    fire("click", karuna);
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 99,
       "dvara: กรุณา related to the 99 มโนทวาริกจิต");
    fire("click", karuna);
  }

  // ============ อารัมมณสังคหะ (matrix จิต + matrix เจตสิก over อารมณ์ ๖) ============
  fire("click", schemeBtns.find((b) => b.dataset.scheme === "arammana"));
  ok(byId["subaxis-switch"].hidden, "arammana: no sub-toggle");
  ok(byId["cat-rail"].children.length === 6, "arammana: 6 อารมณ์ chips");
  ok(byId["cat-rail"].children.map((c) => c.dataset.cat).join(",") === "rupa,satta,gandha,rasa,photthabba,dhamma",
     "arammana: rail order = รูป สัทท คันธ รส โผฏฐัพพ ธัมมารมณ์");
  ok(/<ul class="info-notelist">/.test(byId["info-panel"].innerHTML)
     && (byId["info-panel"].innerHTML.match(/<li>/g) || []).length >= 8,
     "arammana: explanation box renders as a bulleted list (top + sub bullets)");
  cittaNodes = all(byId["citta-groups"], ".node");
  ok(cittaNodes.length === 121 && cittaNodes.every((n) => n.dataset.nset !== undefined && n.dataset.cat === undefined),
     "arammana: 121 จิต nodes, all matrix");
  {
    const d = distBy(cittaNodes, "nset");
    ok(d[1] === 75 && d[5] === 3 && d[6] === 43 && d[0] === undefined,
       "arammana: จิต by อารมณ์ ๖ set-size = 75/3/43 (" + JSON.stringify(d) + ")");
  }
  {
    const d = distBy(all(byId["cetasika-groups"], ".node"), "nset");
    ok(d[1] === 2 && d[6] === 50 && d[0] === undefined,
       "arammana: เจตสิก by อารมณ์ ๖ set-size = 2/50 (" + JSON.stringify(d) + ")");
  }
  {
    const dhamma = byId["cat-rail"].children.find((c) => c.dataset.cat === "dhamma");
    ok(/จิต 108 · เจต 52/.test(dhamma.innerHTML), "arammana: ธัมมารมณ์ chip = จิต 108 · เจต 52 (" + dhamma.innerHTML + ")");
    const rupa = byId["cat-rail"].children.find((c) => c.dataset.cat === "rupa");
    ok(/จิต 48 · เจต 50/.test(rupa.innerHTML), "arammana: รูปารมณ์ chip = จิต 48 · เจต 50");
  }
  {
    const cakkhuV = cittaNodes.find((n) => n.dataset.id === "ahetuka-akusalavipaka-cakkhu");
    ok(cakkhuV.dataset.nset === "1", "arammana: จักขุวิญญาณจิต รับอารมณ์เดียว (รูปารมณ์)");
    const manodhatu = cittaNodes.find((n) => n.dataset.id === "ahetuka-pancadvaravajjana");
    ok(manodhatu.dataset.nset === "5", "arammana: ปัญจทวาราวัชชนจิต (มโนธาตุ) รับปัญจารมณ์ ๕");
    const abhinna = cittaNodes.find((n) => n.dataset.id === "rupa-ปัญจมฌาน-kusala");
    ok(abhinna.dataset.nset === "6", "arammana: อภิญญาจิต (รูปปัญจมฌานกุศล) รับอารมณ์ครบ ๖");
    const jhana1 = cittaNodes.find((n) => n.dataset.id === "rupa-ปฐมฌาน-kusala");
    ok(jhana1.dataset.nset === "1", "arammana: รูปาวจรปฐมฌานกุศลจิต รับธัมมารมณ์อย่างเดียว");
    const karuna = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "karuna");
    ok(karuna.dataset.nset === "1", "arammana: กรุณาเจตสิก (อัปปมัญญา) รับธัมมารมณ์อย่างเดียว");
    const phassa = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "phassa");
    ok(phassa.dataset.nset === "6", "arammana: ผัสสเจตสิก รับอารมณ์ได้ทั้ง ๖");
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "ahetuka-akusalavipaka-cakkhu"); // {รูปารมณ์}
    fire("click", target);
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 47,
       "arammana: 47 other จิต also take รูปารมณ์ (48 − self)");
    ok(all(byId["cetasika-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 50,
       "arammana: 50 เจตสิก can take รูปารมณ์");
    fire("click", target);
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "mahakusala-1"); // อารมณ์ครบ ๖
    fire("click", target);
    ok(/รับอารมณ์ครบ ๖/.test(byId["info-panel"].innerHTML), "arammana: info shows the size-6 อารมณ์ bucket");
    fire("click", target);
  }

  // ============ วัตถุสังคหะ (matrix จิต + matrix เจตสิก over วัตถุ ๖; degenerate) ============
  fire("click", schemeBtns.find((b) => b.dataset.scheme === "vatthu"));
  ok(byId["subaxis-switch"].hidden, "vatthu: no sub-toggle");
  ok(byId["cat-rail"].children.length === 6, "vatthu: 6 วัตถุ chips");
  ok(byId["cat-rail"].children.map((c) => c.dataset.cat).join(",") === "cakkhu,sota,ghana,jivha,kaya,hadaya",
     "vatthu: rail order = จักขุ โสต ฆาน ชิวหา กาย หทัยวัตถุ");
  cittaNodes = all(byId["citta-groups"], ".node");
  ok(cittaNodes.length === 121 && cittaNodes.every((n) => n.dataset.nset !== undefined && n.dataset.cat === undefined),
     "vatthu: 121 จิต nodes, all matrix");
  {
    const d = distBy(cittaNodes, "nset");
    ok(d[0] === 4 && d[1] === 117 && d[2] === undefined,
       "vatthu: จิต by วัตถุ set-size = 4/117 (" + JSON.stringify(d) + ")");
  }
  {
    const d = distBy(all(byId["cetasika-groups"], ".node"), "nset");
    ok(d[1] === 45 && d[6] === 7 && d[0] === undefined,
       "vatthu: เจตสิก by วัตถุ set-size = 45/7 (" + JSON.stringify(d) + ")");
  }
  {
    const hadaya = byId["cat-rail"].children.find((c) => c.dataset.cat === "hadaya");
    ok(/จิต 107 · เจต 52/.test(hadaya.innerHTML), "vatthu: หทัยวัตถุ chip = จิต 107 · เจต 52 (" + hadaya.innerHTML + ")");
    const cakkhu = byId["cat-rail"].children.find((c) => c.dataset.cat === "cakkhu");
    ok(/จิต 2 · เจต 7/.test(cakkhu.innerHTML), "vatthu: จักขุวัตถุ chip = จิต 2 · เจต 7");
  }
  {
    const arupaV = cittaNodes.find((n) => n.dataset.id === "arupa-akasanancayatana-vipaka");
    ok(arupaV.dataset.nset === "0", "vatthu: อรูปวิปากจิต ไม่อาศัยวัตถุ (set-size 0)");
    const cakkhuV = cittaNodes.find((n) => n.dataset.id === "ahetuka-kusalavipaka-cakkhu");
    ok(cakkhuV.dataset.nset === "1", "vatthu: จักขุวิญญาณจิต อาศัยจักขุวัตถุ");
    const phassa = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "phassa");
    ok(phassa.dataset.nset === "6", "vatthu: ผัสสเจตสิก (สัพพจิตตสาธารณ) อาศัยได้ทั้ง ๖ วัตถุ");
    const karuna = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "karuna");
    ok(karuna.dataset.nset === "1", "vatthu: กรุณาเจตสิก อาศัยหทัยวัตถุอย่างเดียว");
  }
  {
    const target = cittaNodes.find((n) => n.dataset.id === "ahetuka-kusalavipaka-cakkhu"); // {จักขุวัตถุ}
    fire("click", target);
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 1,
       "vatthu: 1 other จิต also rests on จักขุวัตถุ (the อกุศลวิบาก จักขุวิญญาณ)");
    ok(all(byId["cetasika-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 7,
       "vatthu: 7 เจตสิก (สัพพจิตตสาธารณ) can rest on จักขุวัตถุ");
    fire("click", target);
  }
  {
    const target = all(byId["cetasika-groups"], ".node").find((n) => n.dataset.id === "karuna"); // {หทัยวัตถุ}
    fire("click", target);
    ok(all(byId["citta-groups"], ".node").filter((n) => n.classList.contains("is-related")).length === 107,
       "vatthu: กรุณา related to the 107 หทัยวัตถุ-จิต");
    fire("click", target);
  }

  console.log(failed ? "\n" + failed + " CHECK(S) FAILED" : "\nALL CHECKS PASSED");
  process.exitCode = failed ? 1 : 0;
}, 50);
