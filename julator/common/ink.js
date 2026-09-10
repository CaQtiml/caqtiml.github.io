// Freehand annotation overlay: pen (a few colors) + two erasers, drawn on a
// canvas layered over the whole page. Nothing is persisted - a reload clears it.
(function () {
  const canvas = document.createElement("canvas");
  canvas.id = "ink-canvas";
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  const visibilityToggleBtn = document.getElementById("ink-visibility-toggle");
  const panel = document.getElementById("ink-panel");
  const toggleBtn = document.getElementById("ink-toggle");
  const tools = document.getElementById("ink-tools");
  const toolTabs = Array.from(document.querySelectorAll(".ink-tool-tab"));
  const colorToggleBtn = document.getElementById("ink-color-toggle");
  const colorsEl = document.getElementById("ink-colors");
  const colorBtns = Array.from(document.querySelectorAll(".ink-color"));

  const PEN_WIDTH = 3;
  const ERASER_WIDTH = 28;
  const ALPHA_THRESHOLD = 10; // treat near-transparent (anti-aliased edge) pixels as "ink" too

  let currentTool = "pen"; // 'pen' | 'eraser' | 'eraser-connected'
  let currentColor = colorBtns.length ? colorBtns[0].dataset.color : "#1a1a1a";
  let drawing = false;
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

  // Master toggle for the whole tool - collapses everything down to just
  // this handle. Also exits draw mode on collapse, so the page isn't left
  // uninteractive with no visible way to turn drawing back off.
  visibilityToggleBtn.addEventListener("click", () => {
    const collapsing = !panel.hidden;
    if (collapsing) setDrawMode(false);
    panel.hidden = collapsing;
    visibilityToggleBtn.textContent = collapsing ? "▸ คำอธิบายภาพ" : "▾ คำอธิบายภาพ";
  });

  function setTool(tool) {
    currentTool = tool;
    toolTabs.forEach((t) => t.classList.toggle("active", t.dataset.tool === tool));
    // Color only matters for the pen - hide the color picker entirely for
    // either eraser so it doesn't imply color affects erasing.
    const isPen = tool === "pen";
    colorToggleBtn.hidden = !isPen;
    if (!isPen) colorsEl.hidden = true;
  }
  setTool("pen");

  toolTabs.forEach((tab) => {
    tab.addEventListener("click", () => setTool(tab.dataset.tool));
  });

  colorToggleBtn.addEventListener("click", () => {
    colorsEl.hidden = !colorsEl.hidden;
    colorToggleBtn.classList.toggle("active", !colorsEl.hidden);
  });

  colorBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      currentColor = btn.dataset.color;
      colorBtns.forEach((b) => b.classList.toggle("active", b === btn));
      setTool("pen");
    });
  });

  function getPoint(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  // A pen stroke is only PEN_WIDTH (3px) wide, far too thin to require an
  // exact pixel-perfect click - search a small neighborhood for the nearest
  // ink pixel instead of only accepting the exact point clicked.
  const HIT_RADIUS = 12;

  function findNearestInkPixel(data, w, h, px, py) {
    let best = -1;
    let bestDist = Infinity;
    const r = HIT_RADIUS;
    for (let dy = -r; dy <= r; dy++) {
      const cy = py + dy;
      if (cy < 0 || cy >= h) continue;
      for (let dx = -r; dx <= r; dx++) {
        const cx = px + dx;
        if (cx < 0 || cx >= w) continue;
        const dist = dx * dx + dy * dy;
        if (dist > r * r || dist >= bestDist) continue;
        const idx = cy * w + cx;
        if (data[idx * 4 + 3] > ALPHA_THRESHOLD) {
          best = idx;
          bestDist = dist;
        }
      }
    }
    return best;
  }

  // Erases every ink pixel connected (4-connectivity) to the clicked point,
  // regardless of color - a "select this whole stroke and delete it" eraser,
  // as opposed to the drag eraser which only clears pixels it touches.
  function floodFillErase(x, y) {
    const w = canvas.width;
    const h = canvas.height;
    const px = Math.round(x);
    const py = Math.round(y);
    if (px < 0 || py < 0 || px >= w || py >= h) return;

    const imageData = ctx.getImageData(0, 0, w, h);
    const data = imageData.data;
    let startIdx = py * w + px;
    if (data[startIdx * 4 + 3] <= ALPHA_THRESHOLD) {
      startIdx = findNearestInkPixel(data, w, h, px, py);
      if (startIdx < 0) return; // nothing within reach - genuinely empty space
    }

    const visited = new Uint8Array(w * h);
    const stack = [startIdx];
    visited[startIdx] = 1;

    while (stack.length) {
      const p = stack.pop();
      const cx = p % w;
      const cy = (p - cx) / w;
      const di = p * 4;
      data[di] = 0;
      data[di + 1] = 0;
      data[di + 2] = 0;
      data[di + 3] = 0;

      if (cx > 0) tryVisit(p - 1);
      if (cx < w - 1) tryVisit(p + 1);
      if (cy > 0) tryVisit(p - w);
      if (cy < h - 1) tryVisit(p + w);
    }
    function tryVisit(np) {
      if (visited[np]) return;
      visited[np] = 1;
      if (data[np * 4 + 3] > ALPHA_THRESHOLD) stack.push(np);
    }

    ctx.putImageData(imageData, 0, 0);
  }

  function startDraw(e) {
    if (!canvas.classList.contains("drawing")) return;
    if (currentTool === "eraser-connected") {
      const point = getPoint(e);
      floodFillErase(point.x, point.y);
      return; // single-click action, not a drag
    }
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
    if (currentTool === "eraser") {
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
