// Top-down diagram of the blade with a grinding heatmap along the edge bevel.
// Base on the left, point on the right, spine on top, edge at the bottom: the same way round as
// the blade lies on the anvil while grinding. Unground sections are dim; ground sections are
// bright steel; ember brackets under the edge mark every stretch still left to grind.
import * as core from './blade-core.js';

const SPOTS = [[0.2, 'the base'], [0.45, 'the lower blade'], [0.7, 'the middle'], [0.88, 'the upper blade'], [1.01, 'the point']];
export function spotName(u) { return SPOTS.find(([max]) => u < max)[1]; }

// Plain-language list of the places still to grind, e.g. "the base and the point".
export function describeRuns(runs, stations) {
  if (!runs.length) return '';
  const covered = runs.reduce((n, [a, b]) => n + b - a + 1, 0);
  if (covered > stations * 0.8) return 'the whole edge';
  const names = [];
  runs.forEach(([a, b]) => {
    const from = spotName(a / (stations - 1)), to = spotName(b / (stations - 1));
    const name = from === to ? from : `${from} through ${to}`;
    if (!names.includes(name)) names.push(name);
  });
  return names.length === 1 ? names[0] : `${names.slice(0, -1).join(', ')} and ${names[names.length - 1]}`;
}

function hexToRgb(hex) {
  const v = parseInt(hex.replace('#', ''), 16);
  return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
}
function mix(a, b, t) {
  return `rgb(${a.map((x, i) => Math.round(x + (b[i] - x) * t)).join(',')})`;
}

export function createBladeMap(canvas, { stations, tangLength, tangHalfWidth, tangOffset }) {
  const ctx = canvas.getContext('2d');
  const css = getComputedStyle(canvas);
  const token = (name) => css.getPropertyValue(name).trim();
  const colors = {
    unground: hexToRgb(token('--map-unground')),
    ground: hexToRgb(token('--map-ground')),
    flat: token('--map-flat'),
    tang: token('--map-tang'),
    outline: token('--map-outline'),
    todo: token('--ember'),
    marker: token('--paper'),
  };
  let layout = null;

  // runs: core.unfinishedRuns(); markerU: where the stone is (0 base … 1 point) or null.
  function draw(params, refinement, runs, markerU = null) {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const W = canvas.clientWidth, H = canvas.clientHeight;
    if (!W || !H) return;
    if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    const { px, py, angle } = core.centerline(params);
    const at = (i, offset) => [px[i] - Math.sin(angle[i]) * offset, py[i] + Math.cos(angle[i]) * offset];
    const spine = [], ridge = [], edge = [];
    let ymin = Infinity, ymax = -Infinity, xmax = 0;
    for (let i = 0; i < stations; i++) {
      const r = params.spine[i] + params.ridge[i] * (params.edge[i] - params.spine[i]);
      spine.push(at(i, params.spine[i]));
      ridge.push(at(i, r));
      edge.push(at(i, params.edge[i]));
      ymin = Math.min(ymin, edge[i][1], spine[i][1]);
      ymax = Math.max(ymax, edge[i][1], spine[i][1]);
      xmax = Math.max(xmax, spine[i][0], edge[i][0]);
    }
    const xmin = -tangLength;
    const pad = 8, bracket = 12;
    const scale = Math.min((W - 2 * pad) / (xmax - xmin), (H - 2 * pad - bracket) / (ymax - ymin));
    const left = (W - (xmax - xmin) * scale) / 2;
    const top = pad + (H - 2 * pad - bracket - (ymax - ymin) * scale) / 2;
    const X = (x) => left + (x - xmin) * scale;
    const Y = (y) => top + (ymax - y) * scale;
    layout = { X, px, edgeBottom: Y(ymin) };

    // Tang
    ctx.fillStyle = colors.tang;
    ctx.fillRect(X(-tangLength), Y(tangOffset + tangHalfWidth), tangLength * scale, 2 * tangHalfWidth * scale);

    // Flat (spine to ridge), not ground
    ctx.beginPath();
    spine.forEach(([x, y], i) => (i ? ctx.lineTo(X(x), Y(y)) : ctx.moveTo(X(x), Y(y))));
    for (let i = stations - 1; i >= 0; i--) ctx.lineTo(X(ridge[i][0]), Y(ridge[i][1]));
    ctx.closePath();
    ctx.fillStyle = colors.flat;
    ctx.fill();

    // Edge bevel heatmap, one cell per segment
    for (let i = 0; i < stations - 1; i++) {
      const t = (refinement[i] + refinement[i + 1]) / 2;
      ctx.fillStyle = mix(colors.unground, colors.ground, t);
      ctx.strokeStyle = ctx.fillStyle;
      ctx.lineWidth = 0.6;
      ctx.beginPath();
      ctx.moveTo(X(ridge[i][0]), Y(ridge[i][1]));
      ctx.lineTo(X(ridge[i + 1][0]), Y(ridge[i + 1][1]));
      ctx.lineTo(X(edge[i + 1][0]), Y(edge[i + 1][1]));
      ctx.lineTo(X(edge[i][0]), Y(edge[i][1]));
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    // Silhouette outline
    ctx.beginPath();
    spine.forEach(([x, y], i) => (i ? ctx.lineTo(X(x), Y(y)) : ctx.moveTo(X(x), Y(y))));
    for (let i = stations - 1; i >= 0; i--) ctx.lineTo(X(edge[i][0]), Y(edge[i][1]));
    ctx.closePath();
    ctx.strokeStyle = colors.outline;
    ctx.lineWidth = 1;
    ctx.stroke();

    // Brackets under every stretch still to grind
    const by = Math.min(H - 4, Y(ymin) + 7);
    ctx.strokeStyle = colors.todo;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    runs.forEach(([a, b]) => {
      const x0 = X(px[a]), x1 = Math.max(X(px[b]), x0 + 2);
      ctx.beginPath();
      ctx.moveTo(x0, by - 4); ctx.lineTo(x0, by); ctx.lineTo(x1, by); ctx.lineTo(x1, by - 4);
      ctx.stroke();
    });

    // Where the stone is
    if (markerU !== null) {
      const i = Math.round(markerU * (stations - 1));
      const mx = X(px[i]);
      ctx.strokeStyle = colors.marker;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(mx, Y(spine[i][1]) - 4);
      ctx.lineTo(mx, Y(edge[i][1]) + 2);
      ctx.stroke();
    }
  }

  // Station under a canvas x coordinate, or -1 when off the blade.
  function stationAt(clientX) {
    if (!layout) return -1;
    const x = clientX - canvas.getBoundingClientRect().left;
    let best = -1, bestD = Infinity;
    for (let i = 0; i < stations; i++) {
      const d = Math.abs(layout.X(layout.px[i]) - x);
      if (d < bestD) { bestD = d; best = i; }
    }
    return bestD < 12 ? best : -1;
  }

  return { draw, stationAt };
}
