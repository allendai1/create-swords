// Blade profile editor: reshape a blueprint's stage curves, check it, compare it, export JSON.
// Uses the same core as the forge study, so what you draw here is exactly what forges there.
import * as THREE from 'three';
import { RoomEnvironment } from '../vendor/RoomEnvironment.js';
import * as core from './blade-core.js';

const $ = (id) => document.getElementById(id);
const DRAFT_KEY = 'forge-study-draft';
const CURVE_LABELS = {
  thickness: 'Thickness (cm)', ridge: 'Ridge (0 spine … 1 edge)',
  edgeThickness: 'Edge thickness (cm)', spineThickness: 'Spine thickness (× thickness)',
};
const getJson = (u) => fetch(u).then((r) => {
  if (!r.ok) throw new Error(`Could not load ${u}`);
  return r.json();
});

// ---------- data ----------
const { profiles: index } = await getJson('data/profiles.json');
const blank = await getJson('data/blank.json');
const files = {};
await Promise.all(index.map(async (p) => { files[p.id] = await getJson(`data/${p.file}`); }));

let profile = structuredCloneish(files[index[0].id]);
let stageKey = 'refined';
let curveKey = 'outline';
let selected = null; // { key: 'spine' | 'edge' | curve key, i }
const undoStack = [];

function structuredCloneish(v) { return JSON.parse(JSON.stringify(v)); }
const stage = () => profile.stages[stageKey];
const round = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

// sori (cm) ↔ bend (rad): an arc of length L bent by θ rises about L·θ/8 above its chord.
const soriCm = (s) => (s.length * s.curve.sori) / 8;
const bendFor = (cm, length) => (8 * cm) / length;

// ---------- profile picker ----------
const select = $('profile-select');
index.forEach((p) => select.add(new Option(files[p.id].name, p.id)));
select.addEventListener('change', () => loadProfile(structuredCloneish(files[select.value])));

function loadProfile(p, keepUndo = false) {
  profile = p;
  if (!keepUndo) undoStack.length = 0;
  selected = null;
  select.value = files[p.id] ? p.id : select.value;
  $('export-file').textContent = (index.find((e) => e.id === p.id) || { file: `${p.id}.json` }).file;
  fillSpecFromProfile();
  fitView();
  changed(false);
}

// ---------- undo ----------
function pushUndo() {
  undoStack.push(JSON.stringify(profile));
  if (undoStack.length > 100) undoStack.shift();
  $('btn-undo').disabled = false;
}
$('btn-undo').addEventListener('click', undo);
function undo() {
  if (!undoStack.length) return;
  profile = JSON.parse(undoStack.pop());
  selected = null;
  $('btn-undo').disabled = !undoStack.length;
  changed(false);
}
$('btn-revert').addEventListener('click', () => {
  if (!files[profile.id]) return;
  pushUndo();
  loadProfile(structuredCloneish(files[profile.id]), true);
});

// ---------- stage & curve controls ----------
document.querySelectorAll('[data-stage]').forEach((b) => b.addEventListener('click', () => {
  stageKey = b.dataset.stage;
  document.querySelectorAll('[data-stage]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
  selected = null;
  $('scrub').value = { lengthened: 4, preform: 8, refined: 13 }[stageKey];
  fitView();
  changed(false);
}));
$('curve-select').addEventListener('change', (e) => { curveKey = e.target.value; selected = null; changed(false); });

const numberInput = (id, read, write) => {
  const el = $(id);
  el.addEventListener('change', () => {
    const v = parseFloat(el.value);
    if (!Number.isFinite(v)) { syncFields(); return; }
    pushUndo();
    write(v);
    changed();
  });
  return { el, read };
};
const stageFields = [
  numberInput('f-length', () => stage().length, (v) => { const cm = soriCm(stage()); stage().length = Math.max(1, v); stage().curve.sori = round(bendFor(cm, stage().length), 4); }),
  numberInput('f-sori', () => round(soriCm(stage()), 2), (v) => { stage().curve.sori = round(bendFor(v, stage().length), 4); }),
  numberInput('f-center', () => stage().curve.center, (v) => { stage().curve.center = Math.min(1, Math.max(0, v)); }),
  numberInput('f-spread', () => stage().curve.spread, (v) => { stage().curve.spread = Math.max(0.05, v); }),
  numberInput('t-length', () => (profile.tang || {}).length ?? 6, (v) => { profile.tang = { ...(profile.tang || { width: 1.8 }), length: Math.max(1, v) }; }),
  numberInput('t-width', () => (profile.tang || {}).width ?? 1.8, (v) => { profile.tang = { ...(profile.tang || { length: 6 }), width: Math.max(0.5, v) }; }),
];
const pointU = $('f-u'), pointV = $('f-value');
pointU.addEventListener('change', () => editSelected((pt, pts, i) => { pt[0] = clampU(pts, i, parseFloat(pointU.value)); }));
pointV.addEventListener('change', () => editSelected((pt) => { pt[1] = round(parseFloat(pointV.value)); }));
function editSelected(fn) {
  const pts = selectedPoints();
  if (!pts) return;
  pushUndo();
  fn(pts[selected.i], pts, selected.i);
  changed();
}
$('btn-delete').addEventListener('click', deleteSelected);
addEventListener('keydown', (e) => {
  if (e.target.closest('input, textarea, select')) return;
  if ((e.key === 'Delete' || e.key === 'Backspace') && selected) { e.preventDefault(); deleteSelected(); }
  if ((e.metaKey || e.ctrlKey) && e.key === 'z') { e.preventDefault(); undo(); }
});
function deleteSelected() {
  const pts = selectedPoints();
  if (!pts || pts.length <= 1) return;
  pushUndo();
  pts.splice(selected.i, 1);
  selected = null;
  changed();
}

function selectedPoints() {
  if (!selected) return null;
  return stage()[selected.key];
}
// Interior points keep their order; the first and last point stay at the ends they started at.
function clampU(pts, i, u) {
  if (!Number.isFinite(u)) return pts[i][0];
  if (pts.length === 1) return pts[i][0];
  if (i === 0 && pts[0][0] === 0) return 0;
  if (i === pts.length - 1 && pts[i][0] === 1) return 1;
  const lo = i > 0 ? pts[i - 1][0] + 0.002 : 0;
  const hi = i < pts.length - 1 ? pts[i + 1][0] - 0.002 : 1;
  return round(Math.min(hi, Math.max(lo, u)), 4);
}

function syncFields() {
  stageFields.forEach((f) => { f.el.value = f.read(); });
  const pts = selectedPoints();
  pointU.disabled = pointV.disabled = $('btn-delete').disabled = !pts;
  if (pts) {
    pointU.value = pts[selected.i][0];
    pointV.value = pts[selected.i][1];
    $('btn-delete').disabled = pts.length <= 1;
  } else {
    pointU.value = pointV.value = '';
  }
  $('f-value-label').firstChild.textContent = selected
    ? ({ spine: 'Spine offset (cm)', edge: 'Edge offset (cm)' }[selected.key] || CURVE_LABELS[selected.key])
    : 'Value';
}

// ---------- catalogue measurements ----------
function fillSpecFromProfile() {
  const r = profile.stages.refined;
  const spec = profile.spec || {};
  const width = (u) => sampleAt(r.spine, u) - sampleAt(r.edge, u);
  $('s-nagasa').value = spec.nagasa ?? r.length;
  $('s-sori').value = spec.sori ?? round(soriCm(r), 2);
  $('s-motohaba').value = spec.motohaba ?? round(width(0), 2);
  $('s-sakihaba').value = spec.sakihaba ?? round(width(0.9), 2);
  $('s-kasane').value = spec.kasane ?? sampleAt(r.thickness, 0);
  $('s-kissaki').value = spec.kissaki ?? round(r.length * 0.06, 1);
}
function sampleAt(points, u) { return core.makeCurve(points)(u); }

function readSpec() {
  const v = (id) => parseFloat($(id).value);
  const spec = { nagasa: v('s-nagasa'), sori: v('s-sori'), motohaba: v('s-motohaba'), sakihaba: v('s-sakihaba'), kasane: v('s-kasane'), kissaki: v('s-kissaki') };
  if (!Object.values(spec).every(Number.isFinite)) throw new Error('Fill in every measurement first.');
  if (spec.kissaki >= spec.nagasa / 2) throw new Error('The point section must be shorter than half the blade.');
  return spec;
}

// Rebuilds the refined outline from catalogue numbers, using the starter blades' point shape.
$('btn-apply-spec').addEventListener('click', () => {
  let spec;
  try { spec = readSpec(); } catch (e) { setStatus(e.message); return; }
  pushUndo();
  const { nagasa: L, motohaba: W0, sakihaba: W1, kasane: T, sori: S, kissaki: K } = spec;
  const uk = round(1 - K / L, 3);
  const at = (f) => round(uk + f * (1 - uk), 3);
  const r = profile.stages.refined;
  r.length = L;
  r.curve = { ...r.curve, sori: round(bendFor(S, L), 4) };
  r.spine = [[0, round(W0 / 2)], [uk, round(W1 / 2)], [at(0.5), round(W1 / 2 * 0.93)], [1, round(W1 / 2 * 0.7)]];
  r.edge = [[0, -round(W0 / 2)], [round(uk / 2, 3), -round((W0 + W1) / 4)], [uk, -round(W1 / 2)], [at(0.35), -round(W1 / 2 * 0.82)], [at(0.75), -round(W1 / 2 * 0.3)], [1, round(W1 / 2 * 0.62)]];
  r.thickness = [[0, T], [round(uk * 0.95, 3), round(T * 0.77)], [uk, round(T * 0.65)], [1, 0.12]];
  profile.spec = { note: profile.spec?.note || 'Catalogue-style targets this draft was built from (cm).', ...spec };
  changed();
  setStatus('Refined outline rebuilt from the measurements.');
});

// Derives the lengthened bar and the preform from the universal blank and the refined blade.
$('btn-derive').addEventListener('click', () => {
  pushUndo();
  const r = profile.stages.refined;
  const W0 = sampleAt(r.spine, 0) - sampleAt(r.edge, 0);
  const W1 = sampleAt(r.spine, 0.9) - sampleAt(r.edge, 0.9);
  const T = sampleAt(r.thickness, 0);
  const blankW = sampleAt(blank.spine, 0) - sampleAt(blank.edge, 0);
  const blankT = sampleAt(blank.thickness, 0);
  const barW = round((blankW + 2 * W0) / 3 / 2);
  const barT = round((blankT + T) / 2);
  profile.stages.lengthened = {
    length: round(blank.length + 0.75 * (r.length - blank.length), 1),
    curve: { sori: 0, center: 0.5, spread: 0.35 },
    spine: [[0, barW], [0.92, round(barW * 0.97)], [1, round(barW * 0.82)]],
    edge: [[0, -barW], [0.92, -round(barW * 0.97)], [1, -round(barW * 0.82)]],
    ridge: [[0, 0.85]],
    thickness: [[0, barT], [1, round(barT * 0.88)]],
    edgeThickness: [[0, 0.55]],
    spineThickness: [[0, 0.92]],
  };
  profile.stages.preform = {
    length: r.length,
    curve: { ...r.curve, sori: round(r.curve.sori * 0.6, 4) },
    spine: [[0, round(W0 / 2 + 0.05)], [1, round(W1 / 2 + 0.1)]],
    edge: [[0, -round(W0 / 2 + 0.05)], [0.85, -round(W1 / 2 + 0.2)], [1, -round(W1 / 2 * 0.75)]],
    ridge: [[0, 0.4]],
    thickness: [[0, round(T * 1.1)], [1, round(T * 0.8)]],
    edgeThickness: [[0, 0.28]],
    spineThickness: [[0, 0.85]],
  };
  changed();
  setStatus('Lengthened and preform stages derived from the refined blade.');
});

// ---------- drawing canvas ----------
const outline = $('outline');
const octx = outline.getContext('2d');
const view = { scale: 10, ox: 40, oy: 150 };
let fitPending = true;
let refImage = null;

function sizeCanvas(c) {
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const w = c.clientWidth, h = c.clientHeight;
  if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
  return { w, h, dpr };
}

// Centreline of a sampled stage, with interpolation between stations.
function frameOf(params) {
  const cl = core.centerline(params);
  const N = params.segLen.length;
  return (u) => {
    const f = Math.min(N - 1, Math.max(0, u * (N - 1)));
    const i = Math.min(N - 2, Math.floor(f)), t = f - i;
    const x = cl.px[i] + (cl.px[i + 1] - cl.px[i]) * t;
    const y = cl.py[i] + (cl.py[i + 1] - cl.py[i]) * t;
    const a = cl.angle[i] + (cl.angle[i + 1] - cl.angle[i]) * t;
    return { x, y, nx: -Math.sin(a), ny: Math.cos(a) };
  };
}
const sampled = (s) => core.sampleShape(s, profile.stations);
const toScreen = (x, y) => [view.ox + x * view.scale, view.oy - y * view.scale];
const toWorld = (sx, sy) => [(sx - view.ox) / view.scale, (view.oy - sy) / view.scale];

function fitView() { fitPending = true; }
$('btn-fit').addEventListener('click', () => { fitView(); draw(); });
function doFit(w, h) {
  const s = stage();
  const tang = (profile.tang || {}).length ?? 6;
  const p = sampled(s);
  const frame = frameOf(p);
  let xmin = -tang, xmax = 0, ymin = -2, ymax = 2;
  for (let k = 0; k <= 40; k++) {
    const u = k / 40, f = frame(u);
    const sp = sampleAt(s.spine, u), ed = sampleAt(s.edge, u);
    [[f.x + f.nx * sp, f.y + f.ny * sp], [f.x + f.nx * ed, f.y + f.ny * ed]].forEach(([x, y]) => {
      xmax = Math.max(xmax, x); ymin = Math.min(ymin, y); ymax = Math.max(ymax, y);
    });
  }
  view.scale = Math.min((w - 40) / (xmax - xmin), (h - 40) / (ymax - ymin));
  view.ox = 20 - xmin * view.scale + ((w - 40) - (xmax - xmin) * view.scale) / 2;
  view.oy = h / 2 + ((ymax + ymin) / 2) * view.scale;
  fitPending = false;
}

// Graph layout for the non-outline curves.
function graphLayout(w, h) {
  const s = stage();
  const pts = s[curveKey];
  const sampledVals = Array.from({ length: 41 }, (_, k) => sampleAt(pts, k / 40));
  const vmax = curveKey === 'ridge' ? 1 : Math.max(0.1, ...pts.map((p) => p[1]), ...sampledVals) * 1.25;
  const left = 48, right = 16, top = 16, bottom = 28;
  return {
    X: (u) => left + u * (w - left - right),
    Y: (v) => h - bottom - (v / vmax) * (h - top - bottom),
    U: (sx) => (sx - left) / (w - left - right),
    V: (sy) => ((h - bottom - sy) / (h - top - bottom)) * vmax,
    vmax, left, right, top, bottom,
  };
}

const css = getComputedStyle(document.documentElement);
const C = (name) => css.getPropertyValue(name).trim();

function draw() {
  const { w, h, dpr } = sizeCanvas(outline);
  octx.setTransform(dpr, 0, 0, dpr, 0, 0);
  octx.clearRect(0, 0, w, h);
  if (curveKey === 'outline') drawOutline(w, h); else drawGraph(w, h);
}

function drawOutline(w, h) {
  if (fitPending) doFit(w, h);
  const s = stage();
  const p = sampled(s);
  const frame = frameOf(p);
  const tang = profile.tang || { length: 6, width: 1.8 };

  // cm grid
  const step = view.scale > 25 ? 1 : view.scale > 6 ? 5 : 10;
  octx.strokeStyle = C('--grid');
  octx.lineWidth = 1;
  const [x0, y1] = toWorld(0, 0), [x1, y0] = toWorld(w, h);
  for (let x = Math.ceil(x0 / step) * step; x <= x1; x += step) { const [sx] = toScreen(x, 0); octx.beginPath(); octx.moveTo(sx, 0); octx.lineTo(sx, h); octx.stroke(); }
  for (let y = Math.ceil(y0 / step) * step; y <= y1; y += step) { const [, sy] = toScreen(0, y); octx.beginPath(); octx.moveTo(0, sy); octx.lineTo(w, sy); octx.stroke(); }

  // reference image
  if (refImage) {
    const widthCm = parseFloat($('ref-width').value) || 40;
    const heightCm = widthCm * (refImage.height / refImage.width);
    const [sx, sy] = toScreen(parseFloat($('ref-x').value) || 0, parseFloat($('ref-y').value) || 0);
    octx.save();
    octx.globalAlpha = parseFloat($('ref-opacity').value);
    octx.translate(sx, sy);
    octx.rotate((-(parseFloat($('ref-rot').value) || 0) * Math.PI) / 180);
    if ($('ref-flip').checked) { octx.translate(widthCm * view.scale, 0); octx.scale(-1, 1); }
    octx.drawImage(refImage, 0, -heightCm * view.scale / 2, widthCm * view.scale, heightCm * view.scale);
    octx.restore();
  }

  // previous stage as a ghost
  const order = ['lengthened', 'preform', 'refined'];
  const prevShape = order.indexOf(stageKey) === 0 ? blank : profile.stages[order[order.indexOf(stageKey) - 1]];
  traceShape(prevShape, frameOf(sampled(prevShape)), C('--line'), null, [4, 4]);

  // tang
  octx.fillStyle = C('--charcoal');
  const [tx, ty] = toScreen(-tang.length, 0.35 + tang.width / 2);
  octx.fillRect(tx, ty, tang.length * view.scale, tang.width * view.scale);

  // this stage
  traceShape(s, frame, C('--paper'), 'rgba(201, 210, 218, 0.12)');
  // ridge line
  octx.setLineDash([3, 4]);
  octx.strokeStyle = C('--ash');
  octx.beginPath();
  for (let k = 0; k <= 80; k++) {
    const u = k / 80, f = frame(u);
    const sp = sampleAt(s.spine, u), ed = sampleAt(s.edge, u), rg = sampleAt(s.ridge, u);
    const off = sp + rg * (ed - sp);
    const [sx, sy] = toScreen(f.x + f.nx * off, f.y + f.ny * off);
    k ? octx.lineTo(sx, sy) : octx.moveTo(sx, sy);
  }
  octx.stroke();
  octx.setLineDash([]);

  // control points
  ['spine', 'edge'].forEach((key) => s[key].forEach(([u, v], i) => {
    const f = frame(u);
    const [sx, sy] = toScreen(f.x + f.nx * v, f.y + f.ny * v);
    drawHandle(sx, sy, key === 'spine' ? C('--steel') : C('--ember'), selected && selected.key === key && selected.i === i);
  }));
}

function traceShape(shape, frame, stroke, fill, dash) {
  const pts = [];
  for (let k = 0; k <= 120; k++) { const u = k / 120, f = frame(u), v = sampleAt(shape.spine, u); pts.push(toScreen(f.x + f.nx * v, f.y + f.ny * v)); }
  for (let k = 120; k >= 0; k--) { const u = k / 120, f = frame(u), v = sampleAt(shape.edge, u); pts.push(toScreen(f.x + f.nx * v, f.y + f.ny * v)); }
  octx.beginPath();
  pts.forEach(([x, y], i) => (i ? octx.lineTo(x, y) : octx.moveTo(x, y)));
  octx.closePath();
  if (fill) { octx.fillStyle = fill; octx.fill(); }
  octx.setLineDash(dash || []);
  octx.strokeStyle = stroke;
  octx.lineWidth = 1.5;
  octx.stroke();
  octx.setLineDash([]);
}

function drawHandle(x, y, color, isSelected) {
  octx.beginPath();
  octx.arc(x, y, isSelected ? 7 : 5, 0, Math.PI * 2);
  octx.fillStyle = isSelected ? color : C('--soot');
  octx.fill();
  octx.lineWidth = 2;
  octx.strokeStyle = color;
  octx.stroke();
}

function drawGraph(w, h) {
  const s = stage();
  const g = graphLayout(w, h);
  const pts = s[curveKey];
  const L = s.length;
  octx.font = `11px ${C('--font-mono')}`;
  octx.fillStyle = C('--ash');
  octx.strokeStyle = C('--grid');
  octx.lineWidth = 1;
  const vStep = g.vmax > 2 ? 0.5 : g.vmax > 0.6 ? 0.2 : 0.1;
  for (let v = 0; v <= g.vmax + 1e-9; v += vStep) {
    octx.beginPath(); octx.moveTo(g.left, g.Y(v)); octx.lineTo(w - g.right, g.Y(v)); octx.stroke();
    octx.textAlign = 'right'; octx.fillText(round(v, 2), g.left - 6, g.Y(v) + 4);
  }
  const cmStep = L > 50 ? 10 : 5;
  for (let cm = 0; cm <= L + 1e-9; cm += cmStep) {
    const x = g.X(cm / L);
    octx.beginPath(); octx.moveTo(x, g.top); octx.lineTo(x, h - g.bottom); octx.stroke();
    octx.textAlign = 'center'; octx.fillText(`${cm}`, x, h - 10);
  }
  octx.textAlign = 'left';
  octx.fillText(`${CURVE_LABELS[curveKey]} along the blade (cm)`, g.left + 6, g.top + 10);
  octx.strokeStyle = C('--paper');
  octx.lineWidth = 2;
  octx.beginPath();
  for (let k = 0; k <= 120; k++) { const u = k / 120, x = g.X(u), y = g.Y(sampleAt(pts, u)); k ? octx.lineTo(x, y) : octx.moveTo(x, y); }
  octx.stroke();
  pts.forEach(([u, v], i) => drawHandle(g.X(u), g.Y(v), C('--ember'), selected && selected.key === curveKey && selected.i === i));
}

// ---------- drawing input ----------
let drag = null;
function eventPos(e) { const r = outline.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }

function hitPoint(sx, sy) {
  const s = stage();
  const { w, h } = sizeCanvas(outline);
  let best = null, bestD = 10;
  if (curveKey === 'outline') {
    const frame = frameOf(sampled(s));
    ['spine', 'edge'].forEach((key) => s[key].forEach(([u, v], i) => {
      const f = frame(u);
      const [px, py] = toScreen(f.x + f.nx * v, f.y + f.ny * v);
      const d = Math.hypot(px - sx, py - sy);
      if (d < bestD) { bestD = d; best = { key, i }; }
    }));
  } else {
    const g = graphLayout(w, h);
    s[curveKey].forEach(([u, v], i) => {
      const d = Math.hypot(g.X(u) - sx, g.Y(v) - sy);
      if (d < bestD) { bestD = d; best = { key: curveKey, i }; }
    });
  }
  return best;
}

// Nearest point on the centreline to a world position: returns u and the signed offset.
function projectToBlade(x, y) {
  const frame = frameOf(sampled(stage()));
  let best = { u: 0, d: Infinity };
  for (let k = 0; k <= 400; k++) {
    const u = k / 400, f = frame(u);
    const d = Math.hypot(x - f.x, y - f.y);
    if (d < best.d) best = { u, d };
  }
  const f = frame(best.u);
  return { u: best.u, offset: (x - f.x) * f.nx + (y - f.y) * f.ny };
}

function pointerToValue(sx, sy) {
  if (curveKey === 'outline') {
    const [x, y] = toWorld(sx, sy);
    const { u, offset } = projectToBlade(x, y);
    return [u, offset];
  }
  const { w, h } = sizeCanvas(outline);
  const g = graphLayout(w, h);
  let v = g.V(sy);
  if (curveKey === 'ridge') v = Math.min(1, Math.max(0, v));
  else v = Math.max(0.01, v);
  return [Math.min(1, Math.max(0, g.U(sx))), v];
}

outline.addEventListener('pointerdown', (e) => {
  const [sx, sy] = eventPos(e);
  const hit = hitPoint(sx, sy);
  outline.setPointerCapture(e.pointerId);
  if (hit) {
    selected = hit;
    pushUndo();
    drag = { kind: 'point', moved: false };
  } else {
    selected = null;
    drag = curveKey === 'outline' ? { kind: 'pan', sx, sy, ox: view.ox, oy: view.oy } : null;
  }
  changed(false);
});
outline.addEventListener('pointermove', (e) => {
  const [sx, sy] = eventPos(e);
  if (curveKey === 'outline') {
    const [x, y] = toWorld(sx, sy);
    const { u, offset } = projectToBlade(x, y);
    $('outline-readout').textContent = `${round(u * stage().length, 1)} cm along · ${round(offset, 2)} cm from centre`;
  } else {
    const [u, v] = pointerToValue(sx, sy);
    $('outline-readout').textContent = `${round(u * stage().length, 1)} cm along · ${round(v, 3)}`;
  }
  if (!drag) return;
  if (drag.kind === 'pan') {
    view.ox = drag.ox + (sx - drag.sx);
    view.oy = drag.oy + (sy - drag.sy);
    draw();
    return;
  }
  const pts = selectedPoints();
  const [u, v] = pointerToValue(sx, sy);
  pts[selected.i][0] = clampU(pts, selected.i, u);
  pts[selected.i][1] = round(v);
  drag.moved = true;
  changed(true, true);
});
const endDrag = () => {
  if (drag && drag.kind === 'point' && !drag.moved) undoStack.pop(); // a click, not an edit
  $('btn-undo').disabled = !undoStack.length;
  if (drag && drag.kind === 'point' && drag.moved) changed();
  drag = null;
};
outline.addEventListener('pointerup', endDrag);
outline.addEventListener('pointercancel', endDrag);
outline.addEventListener('dblclick', (e) => {
  const [sx, sy] = eventPos(e);
  if (hitPoint(sx, sy)) return;
  const [u, v] = pointerToValue(sx, sy);
  const key = curveKey === 'outline' ? (v >= 0 ? 'spine' : 'edge') : curveKey;
  const pts = stage()[key];
  pushUndo();
  let i = pts.findIndex((p) => p[0] > u);
  if (i < 0) i = pts.length;
  pts.splice(i, 0, [round(u, 4), round(v)]);
  pts[i][0] = clampU(pts, i, u);
  selected = { key, i };
  changed();
});
outline.addEventListener('wheel', (e) => {
  if (curveKey !== 'outline') return;
  e.preventDefault();
  const [sx, sy] = eventPos(e);
  const [x, y] = toWorld(sx, sy);
  view.scale = Math.min(400, Math.max(2, view.scale * Math.exp(-e.deltaY * 0.0015)));
  view.ox = sx - x * view.scale;
  view.oy = sy + y * view.scale;
  draw();
}, { passive: false });
addEventListener('resize', () => { fitView(); draw(); drawCompare(); renderPreview(); });

// ---------- reference image ----------
$('ref-file').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => { refImage = img; $('btn-ref-clear').disabled = false; draw(); };
    img.src = reader.result;
  };
  reader.readAsDataURL(file);
});
['ref-width', 'ref-rot', 'ref-x', 'ref-y', 'ref-opacity', 'ref-flip'].forEach((id) => $(id).addEventListener('input', draw));
$('btn-ref-clear').addEventListener('click', () => { refImage = null; $('ref-file').value = ''; $('btn-ref-clear').disabled = true; draw(); });

// ---------- 3D preview ----------
const previewCanvas = $('preview');
const renderer = new THREE.WebGLRenderer({ canvas: previewCanvas, antialias: true });
renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene();
scene.background = new THREE.Color(C('--soot'));
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const keyLight = new THREE.DirectionalLight(0xfff1e0, 1.4);
keyLight.position.set(-20, 40, 30);
scene.add(keyLight, new THREE.HemisphereLight(0xffe6cc, 0x1a1210, 0.4));
const camera3 = new THREE.PerspectiveCamera(30, 1, 0.5, 1000);
const turntable = new THREE.Group();
scene.add(turntable);
const N = profile.stations;
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(core.vertexCount(N) * 3), 3));
geometry.setIndex(new THREE.BufferAttribute(core.buildIndex(N), 1));
const steel = new THREE.MeshStandardMaterial({ color: 0xb8bec6, metalness: 0.85, roughness: 0.35 });
const bladeMesh = new THREE.Mesh(geometry, steel);
const tangMesh = new THREE.Mesh(new THREE.BoxGeometry(1, 0.5, 1), new THREE.MeshStandardMaterial({ color: 0x3a3430, roughness: 0.8 }));
const bladeGroup = new THREE.Group();
bladeGroup.add(bladeMesh, tangMesh);
turntable.add(bladeGroup);
let yaw = -0.35, pitch = 0.75;
let spin = null;
previewCanvas.addEventListener('pointerdown', (e) => { spin = { x: e.clientX, y: e.clientY, yaw, pitch }; previewCanvas.setPointerCapture(e.pointerId); });
previewCanvas.addEventListener('pointermove', (e) => {
  if (!spin) return;
  yaw = spin.yaw + (e.clientX - spin.x) * 0.01;
  pitch = Math.min(1.5, Math.max(-1.5, spin.pitch + (e.clientY - spin.y) * 0.01));
  renderPreview();
});
previewCanvas.addEventListener('pointerup', () => { spin = null; });
const STEP_LABELS = ['Universal blank', ...Array.from({ length: 12 }, (_, k) => `After strike ${k + 1}`), 'Fully ground'];
$('scrub').addEventListener('input', renderPreview);

let previewBlade = null;
function renderPreview() {
  const { w, h } = sizeCanvas(previewCanvas);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(w, h, false);
  camera3.aspect = w / h;
  let params;
  const k = parseInt($('scrub').value, 10);
  if (previewBlade) {
    const states = core.forgingStates(previewBlade);
    $('scrub').max = states.length - 1;
    const i = Math.min(k, states.length - 1);
    params = core.stationParams(previewBlade, states[i]);
    $('scrub-label').textContent = i === states.length - 1 ? 'Fully ground (100%)' : i === states.length - 2 ? 'Forged (90%)' : STEP_LABELS[i];
    steel.color.set(i < states.length - 2 ? 0xd08a5a : 0xb8bec6);
  } else {
    params = sampled(stage()); // the profile doesn't build; show the stage on its own
    $('scrub-label').textContent = `${stageKey} stage only`;
  }
  core.buildPositions(params, geometry.attributes.position.array);
  geometry.attributes.position.needsUpdate = true;
  geometry.computeVertexNormals();
  geometry.computeBoundingBox();
  const tang = profile.tang || { length: 6, width: 1.8 };
  tangMesh.scale.set(tang.length, 1, tang.width);
  tangMesh.position.set(-tang.length / 2, 0, -0.35);
  const box = geometry.boundingBox;
  const span = box.max.x + tang.length;
  bladeGroup.position.set(-(box.max.x - tang.length) / 2, 0, 0);
  turntable.rotation.set(0, yaw, 0);
  const dist = (span * 0.62) / Math.tan(THREE.MathUtils.degToRad(15)) / Math.min(1, camera3.aspect);
  camera3.position.set(0, Math.sin(pitch) * dist, Math.cos(pitch) * dist);
  camera3.lookAt(0, 0, 0);
  camera3.updateProjectionMatrix();
  renderer.render(scene, camera3);
}

// ---------- comparison ----------
function drawCompare() {
  const c = $('compare');
  const ctx = c.getContext('2d');
  const { w, h, dpr } = sizeCanvas(c);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  const rows = [{ name: 'Universal blank', shape: blank, tang: null }].concat(index.map((e) => {
    const p = e.id === profile.id ? profile : files[e.id];
    return { name: p.name + (e.id === profile.id ? ' (editing)' : ''), shape: p.stages.refined, tang: p.tang || { length: 6, width: 1.8 }, current: e.id === profile.id };
  }));
  const maxTang = Math.max(...rows.map((r) => (r.tang ? r.tang.length : 0)));
  const maxLen = Math.max(...rows.map((r) => r.shape.length));
  const labelW = 130, pad = 16;
  const scale = (w - labelW - pad * 2) / (maxTang + maxLen + 2);
  const originX = labelW + pad + maxTang * scale;
  const rowH = (h - 30) / rows.length;
  ctx.font = `12px ${C('--font-body')}`;
  // ruler: every 10 cm from the base of the blade (machi)
  ctx.strokeStyle = C('--grid');
  ctx.fillStyle = C('--ash');
  ctx.textAlign = 'center';
  for (let cm = 0; cm <= maxLen + 1e-9; cm += 10) {
    const x = originX + cm * scale;
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h - 22); ctx.stroke();
    ctx.fillText(`${cm} cm`, x, h - 8);
  }
  rows.forEach((row, r) => {
    const cy = rowH * (r + 0.5);
    const p = sampled(row.shape);
    const frame = frameOf(p);
    const X = (x) => originX + x * scale, Y = (y) => cy - y * scale;
    if (row.tang) {
      ctx.fillStyle = C('--charcoal');
      ctx.fillRect(X(-row.tang.length), Y(0.35 + row.tang.width / 2), row.tang.length * scale, row.tang.width * scale);
    }
    ctx.beginPath();
    for (let k = 0; k <= 120; k++) { const u = k / 120, f = frame(u), v = sampleAt(row.shape.spine, u); const x = X(f.x + f.nx * v), y = Y(f.y + f.ny * v); k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    for (let k = 120; k >= 0; k--) { const u = k / 120, f = frame(u), v = sampleAt(row.shape.edge, u); ctx.lineTo(X(f.x + f.nx * v), Y(f.y + f.ny * v)); }
    ctx.closePath();
    ctx.fillStyle = row.current ? C('--steel') : 'rgba(201, 210, 218, 0.55)';
    ctx.fill();
    ctx.textAlign = 'left';
    ctx.fillStyle = row.current ? C('--paper') : C('--ash');
    ctx.fillText(row.name, 0, cy - 2);
    ctx.fillStyle = C('--ash');
    ctx.fillText(`${round(row.shape.length, 1)} cm`, 0, cy + 13);
  });
}

// ---------- checks ----------
function runChecks() {
  const results = core.validateProfile(blank, profile);
  const list = $('checks');
  list.replaceChildren(...results.map((r) => {
    const li = document.createElement('li');
    li.className = r.ok ? 'ok' : 'fail';
    li.innerHTML = `<span class="mark" aria-hidden="true">${r.ok ? '✓' : '✗'}</span><span><span class="name"></span> <span class="detail"></span></span>`;
    li.querySelector('.name').textContent = `${r.ok ? '' : 'Failed: '}${r.name}`;
    li.querySelector('.detail').textContent = r.detail ? `(${r.detail})` : '';
    return li;
  }));
  const failed = results.filter((r) => !r.ok).length;
  const summary = $('check-summary');
  summary.textContent = failed ? `${failed} check${failed > 1 ? 's' : ''} failed. Fix these before using the profile.` : 'All checks pass.';
  summary.className = `summary ${failed ? 'fail' : 'ok'}`;
  try { previewBlade = core.createBlade(blank, profile); } catch { previewBlade = null; }
  return failed === 0;
}

// ---------- export ----------
const exportBox = $('export');
function setStatus(text) { $('export-status').textContent = text; }
$('btn-copy').addEventListener('click', () => {
  navigator.clipboard.writeText(exportBox.value).then(
    () => setStatus('Copied'),
    () => { exportBox.select(); setStatus('Copy is blocked here. The text is selected; press Ctrl/Cmd+C.'); },
  );
});
$('btn-load').addEventListener('click', () => {
  try {
    const p = JSON.parse(exportBox.value);
    if (!p.stages || !p.stages.refined || !p.recipe) throw new Error('that JSON is not a blade profile');
    pushUndo();
    loadProfile(p, true);
    setStatus('Loaded');
  } catch (e) {
    setStatus(`Could not load: ${e.message}.`);
  }
});
$('btn-try').addEventListener('click', () => {
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(profile));
    location.href = 'index.html#draft';
  } catch {
    setStatus('This browser blocked saving the draft. Copy the JSON into dist/data instead.');
  }
});

// ---------- refresh ----------
let checkTimer = 0, frameQueued = false;
// fast: only redraw (while dragging); full refresh re-runs checks and the export.
function changed(edited = true, fast = false) {
  if (edited) setStatus('');
  syncFields();
  if (!frameQueued) {
    frameQueued = true;
    requestAnimationFrame(() => { frameQueued = false; draw(); renderPreview(); drawCompare(); });
  }
  clearTimeout(checkTimer);
  checkTimer = setTimeout(() => {
    runChecks();
    renderPreview();
    exportBox.value = `${core.formatJson(profile)}\n`;
  }, fast ? 250 : 0);
}

loadProfile(profile);

// Inspection handle for checks (not part of the tool).
window.profileEditor = {
  get profile() { return profile; }, files, core, formatted: () => exportBox.value, loadProfile,
  setStage: (k) => document.querySelector(`[data-stage="${k}"]`).click(),
};
