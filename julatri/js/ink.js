// Freehand annotation overlay: pen (a few colors) + eraser, drawn on a canvas
// layered over the whole page. Nothing is persisted - a reload clears it.
(function () {
  const canvas = document.createElement("canvas");
  canvas.id = "ink-canvas";
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  const toggleBtn = document.getElementById("ink-toggle");
  const tools = document.getElementById("ink-tools");
  const eraserBtn = document.getElementById("ink-eraser");
  const colorBtns = Array.from(document.querySelectorAll(".ink-color"));

  const PEN_WIDTH = 3;
  const ERASER_WIDTH = 28;

  let drawing = false;
  let erasing = false;
  let currentColor = colorBtns.length ? colorBtns[0].dataset.color : "#1a1a1a";
  let lastPoint = null;
  let lastW = 0;
  let lastH = 0;

  // Canvas width/height resets its bitmap whenever assigned, so only touch
  // them when the page's actual size changed - otherwise every DOM mutation
  // (e.g. hover highlighting) would silently wipe the drawing.
  function resizeCanvas() {
    const w = Math.max(document.documentElement.scrollWidth, window.innerWidth);
    const h = Math.max(document.documentElement.scrollHeight, window.innerHeight);
    if (w === lastW && h === lastH) return;
    lastW = w;
    lastH = h;
    canvas.width = w;
    canvas.height = h;
  }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  // Catches the async data load in app.js growing the page height, and any
  // later content changes, without coupling to app.js internals.
  new MutationObserver(resizeCanvas).observe(document.body, { childList: true, subtree: true });

  function setDrawMode(active) {
    canvas.classList.toggle("drawing", active);
    toggleBtn.classList.toggle("active", active);
    toggleBtn.textContent = active ? "ปิดโหมดวาด" : "โหมดวาด";
    tools.hidden = !active;
  }
  setDrawMode(false);

  toggleBtn.addEventListener("click", () => {
    setDrawMode(!canvas.classList.contains("drawing"));
  });

  colorBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      currentColor = btn.dataset.color;
      erasing = false;
      eraserBtn.classList.remove("active");
      colorBtns.forEach((b) => b.classList.toggle("active", b === btn));
    });
  });

  eraserBtn.addEventListener("click", () => {
    erasing = !erasing;
    eraserBtn.classList.toggle("active", erasing);
    if (erasing) colorBtns.forEach((b) => b.classList.remove("active"));
  });

  function getPoint(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function startDraw(e) {
    if (!canvas.classList.contains("drawing")) return;
    drawing = true;
    lastPoint = getPoint(e);
    canvas.setPointerCapture(e.pointerId);
  }

  function moveDraw(e) {
    if (!drawing) return;
    const point = getPoint(e);
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    ctx.moveTo(lastPoint.x, lastPoint.y);
    ctx.lineTo(point.x, point.y);
    if (erasing) {
      ctx.globalCompositeOperation = "destination-out";
      ctx.lineWidth = ERASER_WIDTH;
      ctx.strokeStyle = "rgba(0,0,0,1)";
    } else {
      ctx.globalCompositeOperation = "source-over";
      ctx.lineWidth = PEN_WIDTH;
      ctx.strokeStyle = currentColor;
    }
    ctx.stroke();
    lastPoint = point;
  }

  function endDraw() {
    drawing = false;
    lastPoint = null;
  }

  canvas.addEventListener("pointerdown", startDraw);
  canvas.addEventListener("pointermove", moveDraw);
  canvas.addEventListener("pointerup", endDraw);
  canvas.addEventListener("pointercancel", endDraw);
  canvas.addEventListener("pointerleave", endDraw);
})();
