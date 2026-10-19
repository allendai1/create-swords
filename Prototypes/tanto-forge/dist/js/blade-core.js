// Blade shape and forging state. No rendering, no DOM: this is the part meant to port to Roblox
// (Luau + EditableMesh). Shapes are sampled at a fixed number of stations along the blade, so
// every state shares the same vertex layout (stable correspondence), and the whole forging state
// is just { strikeIndex, refinement[] }: strike progress is replayed from the recipe.

export const STAGES = ['lengthen', 'taper', 'tip'];
export const PARAMS = ['segLen', 'bend', 'spine', 'edge', 'ridge', 'thick', 'edgeT', 'spineT'];
export const RING = 12; // vertices per station, see buildPositions
export const FORGED_QUALITY = 90;
export const MAX_QUALITY = 100;
// Refinement per centimetre of stone travel along the edge. Exploratory pacing: about four passes.
export const GRIND_PER_CM = 0.25;

// ---------- curves ----------

// Monotone cubic (Fritsch–Carlson) through [[u, v], ...]; flat outside the first/last point.
export function makeCurve(points) {
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  const n = xs.length;
  if (n === 1) return () => ys[0];
  const d = [];
  for (let k = 0; k < n - 1; k++) d.push((ys[k + 1] - ys[k]) / (xs[k + 1] - xs[k]));
  const m = new Array(n);
  m[0] = d[0];
  m[n - 1] = d[n - 2];
  for (let k = 1; k < n - 1; k++) m[k] = d[k - 1] * d[k] <= 0 ? 0 : (d[k - 1] + d[k]) / 2;
  for (let k = 0; k < n - 1; k++) {
    if (d[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
    const a = m[k] / d[k], b = m[k + 1] / d[k], s = a * a + b * b;
    if (s > 9) { const t = 3 / Math.sqrt(s); m[k] = t * a * d[k]; m[k + 1] = t * b * d[k]; }
  }
  return (u) => {
    if (u <= xs[0]) return ys[0];
    if (u >= xs[n - 1]) return ys[n - 1];
    let k = 0;
    while (u > xs[k + 1]) k++;
    const h = xs[k + 1] - xs[k], t = (u - xs[k]) / h, t2 = t * t, t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * ys[k] + (t3 - 2 * t2 + t) * h * m[k]
      + (-2 * t3 + 3 * t2) * ys[k + 1] + (t3 - t2) * h * m[k + 1];
  };
}

function falloff(distance, radius) {
  const x = Math.abs(distance) / radius;
  return x >= 1 ? 0 : 0.5 * (1 + Math.cos(Math.PI * x));
}

// ---------- shapes ----------

// Samples one stage shape at every station into struct-of-arrays form.
export function sampleShape(shape, stations) {
  const out = {};
  for (const p of PARAMS) out[p] = new Float64Array(stations);
  const curves = {
    spine: makeCurve(shape.spine), edge: makeCurve(shape.edge), ridge: makeCurve(shape.ridge),
    thick: makeCurve(shape.thickness), edgeT: makeCurve(shape.edgeThickness),
    spineT: makeCurve(shape.spineThickness),
  };
  const segLen = shape.length / (stations - 1);
  // Curvature (sori) is spread over the segments with a gaussian around `center`.
  const { sori, center, spread } = shape.curve;
  const density = [];
  let total = 0;
  for (let i = 0; i < stations - 1; i++) {
    const mid = (i + 0.5) / (stations - 1);
    const w = Math.exp(-(((mid - center) / spread) ** 2));
    density.push(w);
    total += w;
  }
  for (let i = 0; i < stations; i++) {
    const u = i / (stations - 1);
    out.segLen[i] = i < stations - 1 ? segLen : 0;
    out.bend[i] = i < stations - 1 ? (sori * density[i]) / total : 0;
    out.spine[i] = curves.spine(u);
    out.edge[i] = curves.edge(u);
    out.ridge[i] = curves.ridge(u);
    out.thick[i] = curves.thick(u);
    out.edgeT[i] = curves.edgeT(u);
    out.spineT[i] = curves.spineT(u);
  }
  return out;
}

// The 90% shape: the refined blade plus a small edge allowance and a duller edge.
function forgedFrom(refined, allowance) {
  const out = {};
  for (const p of PARAMS) out[p] = Float64Array.from(refined[p]);
  for (let i = 0; i < out.edge.length; i++) {
    out.edge[i] -= allowance.edge;
    out.edgeT[i] += allowance.edgeThickness;
  }
  return out;
}

// ---------- blade definition ----------

export function createBlade(blank, profile) {
  const N = profile.stations;
  const refined = sampleShape(profile.stages.refined, N);
  // Order matters: each forging stage moves from shapes[k] to shapes[k + 1]; grinding is 3 → 4.
  const shapes = [
    sampleShape(blank, N),
    sampleShape(profile.stages.lengthened, N),
    sampleShape(profile.stages.preform, N),
    forgedFrom(refined, profile.forgedAllowance),
    refined,
  ];

  // Normalise each strike's falloff by the stage's total coverage, so every station reaches
  // exactly 100% of its stage change on the stage's last strike: no catch-up snap.
  const recipe = profile.recipe.map((s) => ({ ...s, stageIndex: STAGES.indexOf(s.stage) }));
  recipe.forEach((s, k) => {
    if (s.stageIndex < 0) throw new Error(`strike ${k + 1}: unknown stage "${s.stage}"`);
    if (k > 0 && s.stageIndex < recipe[k - 1].stageIndex) throw new Error(`strike ${k + 1}: stages out of order`);
  });
  const coverage = STAGES.map(() => new Float64Array(N));
  const raw = recipe.map((s) => {
    const w = new Float64Array(N);
    for (let i = 0; i < N; i++) w[i] = falloff(i / (N - 1) - s.u, s.radius);
    for (let i = 0; i < N; i++) coverage[s.stageIndex][i] += w[i];
    return w;
  });
  const minCoverage = coverage.map((c) => Math.min(...c));
  minCoverage.forEach((c, k) => {
    if (!(c > 0.15)) throw new Error(`stage "${STAGES[k]}" leaves part of the blade unshaped (min coverage ${c.toFixed(3)})`);
  });
  const contrib = raw.map((w, k) => w.map((v, i) => v / coverage[recipe[k].stageIndex][i]));
  const lastStrikeOfStage = STAGES.map((_, si) => {
    let last = -1;
    recipe.forEach((s, k) => { if (s.stageIndex === si) last = k; });
    return last;
  });

  // Grinding work is weighted by how much excess metal each station carries.
  const grindWeight = new Float64Array(N);
  let grindWeightTotal = 0;
  for (let i = 0; i < N; i++) {
    const len = i < N - 1 ? refined.segLen[i] : refined.segLen[N - 2] / 2;
    grindWeight[i] = len * (Math.abs(shapes[3].edge[i] - refined.edge[i]) + Math.abs(shapes[3].edgeT[i] - refined.edgeT[i]));
    grindWeightTotal += grindWeight[i];
  }

  return {
    id: profile.id, name: profile.name, version: profile.version, stations: N,
    shapes, recipe, contrib, minCoverage, lastStrikeOfStage, grindWeight, grindWeightTotal,
    profile, blank,
  };
}

// ---------- state ----------

export function createState(blade) {
  return {
    strikeIndex: 0,
    progress: STAGES.map(() => new Float64Array(blade.stations)),
    refinement: new Float64Array(blade.stations),
    lastResidual: 0,
  };
}

export function totalStrikes(blade) { return blade.recipe.length; }
export function isForged(blade, state) { return state.strikeIndex >= blade.recipe.length; }
export function isRefined(blade, state) { return isForged(blade, state) && state.refinement.every((r) => r === 1); }

function cloneState(state) {
  return {
    strikeIndex: state.strikeIndex,
    progress: state.progress.map((g) => Float64Array.from(g)),
    refinement: Float64Array.from(state.refinement),
    lastResidual: state.lastResidual,
  };
}

// One hammer strike. Returns a new state, or null when forging is already complete.
export function applyStrike(blade, state) {
  const k = state.strikeIndex;
  if (k >= blade.recipe.length) return null;
  const next = cloneState(state);
  const s = blade.recipe[k];
  const g = next.progress[s.stageIndex];
  const c = blade.contrib[k];
  for (let i = 0; i < g.length; i++) g[i] += c[i];
  next.lastResidual = 0;
  if (blade.lastStrikeOfStage[s.stageIndex] === k) {
    // Normalisation already sums to 1; this only removes floating-point dust.
    for (let i = 0; i < g.length; i++) {
      next.lastResidual = Math.max(next.lastResidual, Math.abs(1 - g[i]));
      g[i] = 1;
    }
  } else {
    for (let i = 0; i < g.length; i++) g[i] = Math.min(1, g[i]);
  }
  next.strikeIndex = k + 1;
  return next;
}

// Safe grinding at position u (0 base … 1 point). Only works after forging; refinement only
// rises and clamps at 1, so the blade can never be cut past the refined shape.
export function applyGrind(blade, state, u, amount, radius = 0.07) {
  if (!isForged(blade, state) || !(amount > 0) || !Number.isFinite(u)) return state;
  const next = cloneState(state);
  const N = blade.stations;
  for (let i = 0; i < N; i++) {
    const ui = i / (N - 1);
    // Near either end the stone overhangs it, so the last sections are as easy to finish as the rest.
    const overhang = (u < radius && ui < u) || (u > 1 - radius && ui > u);
    const w = overhang ? 1 : falloff(ui - u, radius);
    if (w <= 0) continue;
    let r = next.refinement[i] + amount * w;
    if (r >= 0.999) r = 1;
    next.refinement[i] = Math.min(1, Math.max(next.refinement[i], r));
  }
  return next;
}

export function quality(blade, state) {
  const strikes = blade.recipe.length;
  if (state.strikeIndex < strikes) return (FORGED_QUALITY * state.strikeIndex) / strikes;
  let done = 0;
  for (let i = 0; i < blade.stations; i++) done += blade.grindWeight[i] * state.refinement[i];
  return FORGED_QUALITY + (MAX_QUALITY - FORGED_QUALITY) * (done / blade.grindWeightTotal);
}

// Shown to players: never rounds up to a percentage the blade hasn't earned.
export function displayQuality(blade, state) {
  return isRefined(blade, state) ? MAX_QUALITY : Math.floor(quality(blade, state) + 1e-9);
}

// ---------- shape at a state ----------

// Current per-station parameters: blank + each stage's change × that station's progress,
// then the grinding change × refinement.
export function stationParams(blade, state) {
  const { shapes } = blade;
  const N = blade.stations;
  const out = {};
  for (const p of PARAMS) {
    const v = Float64Array.from(shapes[0][p]);
    for (let s = 0; s < STAGES.length; s++) {
      const g = state.progress[s], a = shapes[s][p], b = shapes[s + 1][p];
      for (let i = 0; i < N; i++) if (g[i]) v[i] += (b[i] - a[i]) * g[i];
    }
    const r = state.refinement, a = shapes[3][p], b = shapes[4][p];
    for (let i = 0; i < N; i++) if (r[i]) v[i] += (b[i] - a[i]) * r[i];
    out[p] = v;
  }
  return out;
}

export function lerpParams(a, b, t, out) {
  out = out || {};
  for (const p of PARAMS) {
    const x = a[p], y = b[p];
    const o = out[p] || (out[p] = new Float64Array(x.length));
    for (let i = 0; i < x.length; i++) o[i] = x[i] + (y[i] - x[i]) * t;
  }
  return out;
}

// Centreline in the blade's own plane. x runs base → point; y points toward the spine.
// Positive bend curves the point toward the spine (edge on the outside of the curve).
export function centerline(params) {
  const N = params.segLen.length;
  const px = new Float64Array(N), py = new Float64Array(N), angle = new Float64Array(N);
  const seg = new Float64Array(Math.max(N - 1, 1));
  let acc = 0;
  for (let i = 0; i < N - 1; i++) { seg[i] = acc + params.bend[i] / 2; acc += params.bend[i]; }
  for (let i = 0; i < N - 1; i++) {
    px[i + 1] = px[i] + params.segLen[i] * Math.cos(seg[i]);
    py[i + 1] = py[i] + params.segLen[i] * Math.sin(seg[i]);
  }
  for (let i = 0; i < N; i++) {
    angle[i] = i === 0 ? seg[0] : i === N - 1 ? seg[N - 2] : (seg[i - 1] + seg[i]) / 2;
  }
  return { px, py, angle };
}

// Where a strike lands, in blade-local 3D (x along, y up through the thickness, z = -planeY).
export function strikeTarget(blade, params, strikeIndex) {
  const s = blade.recipe[Math.min(strikeIndex, blade.recipe.length - 1)];
  const N = blade.stations;
  const i = Math.round(s.u * (N - 1));
  const { px, py, angle } = centerline(params);
  const ridgeY = params.spine[i] + params.ridge[i] * (params.edge[i] - params.spine[i]);
  const across = s.side === 'edge' ? (ridgeY + params.edge[i]) / 2
    : s.side === 'spine' ? (ridgeY + params.spine[i]) / 2
    : (params.spine[i] + params.edge[i]) / 2;
  const nx = -Math.sin(angle[i]), ny = Math.cos(angle[i]);
  const thickness = s.side === 'edge' ? (params.thick[i] + params.edgeT[i]) / 2 : params.thick[i];
  return {
    station: i,
    point: [px[i] + nx * across, 0, -(py[i] + ny * across)],
    angle: angle[i],
    thickness,
    halfWidth: (params.spine[i] - params.edge[i]) / 2,
    flip: !!s.flip,
    turn: ((s.turn || 0) * Math.PI) / 180,
    stage: s.stage,
  };
}

// ---------- geometry ----------
// Ring per station (cross-section, spine → edge → back):
//   0 spine top · 1 ridge top (flat face) · 2 ridge top (bevel) · 3 edge top (bevel)
//   4 edge bottom (bevel) · 5 ridge bottom (bevel) · 6 ridge bottom (flat) · 7 spine bottom
//   8/9 spine top/bottom (mune face) · 10/11 edge top/bottom (edge face)
// Duplicated corners keep creases crisp when normals are computed per vertex.
// After the stations come two caps (base, point): 6 outline vertices + a centre each.

const RING_FACES = [[0, 1], [2, 3], [10, 11], [4, 5], [6, 7], [9, 8]];
const CAP_RING = [0, 1, 3, 4, 5, 7];
export const BEVEL_RING = new Set([2, 3, 4, 5, 10, 11]);

export function vertexCount(stations) { return stations * RING + 2 * (CAP_RING.length + 1); }

export function buildIndex(stations) {
  const idx = [];
  for (let i = 0; i < stations - 1; i++) {
    const a = i * RING, b = (i + 1) * RING;
    for (const [p, q] of RING_FACES) {
      idx.push(a + p, a + q, b + p, a + q, b + q, b + p);
    }
  }
  const capBase = stations * RING;
  for (const [start, reverse] of [[capBase, true], [capBase + CAP_RING.length + 1, false]]) {
    const centre = start + CAP_RING.length;
    for (let j = 0; j < CAP_RING.length; j++) {
      const v0 = start + j, v1 = start + ((j + 1) % CAP_RING.length);
      if (reverse) idx.push(centre, v1, v0); else idx.push(centre, v0, v1);
    }
  }
  return stations * RING > 65535 ? new Uint32Array(idx) : new Uint16Array(idx);
}

export function buildPositions(params, out) {
  const N = params.segLen.length;
  out = out || new Float32Array(vertexCount(N) * 3);
  const { px, py, angle } = centerline(params);
  const put = (v, x, planeY, h) => { out[v * 3] = x; out[v * 3 + 1] = h; out[v * 3 + 2] = -planeY; };
  const ringPoint = (i, offset) => {
    const nx = -Math.sin(angle[i]), ny = Math.cos(angle[i]);
    return [px[i] + nx * offset, py[i] + ny * offset];
  };
  const ringPositions = (i) => {
    const spine = params.spine[i], edge = params.edge[i];
    const ridge = spine + params.ridge[i] * (edge - spine);
    const t = params.thick[i] / 2, te = params.edgeT[i] / 2, ts = (params.thick[i] * params.spineT[i]) / 2;
    const S = ringPoint(i, spine), R = ringPoint(i, ridge), E = ringPoint(i, edge);
    return [
      [S, ts], [R, t], [R, t], [E, te], [E, -te], [R, -t], [R, -t], [S, -ts],
      [S, ts], [S, -ts], [E, te], [E, -te],
    ];
  };
  for (let i = 0; i < N; i++) {
    ringPositions(i).forEach(([p, h], r) => put(i * RING + r, p[0], p[1], h));
  }
  [0, N - 1].forEach((i, c) => {
    const start = N * RING + c * (CAP_RING.length + 1);
    const ring = ringPositions(i);
    let cx = 0, cy = 0;
    CAP_RING.forEach((r, j) => {
      const [p, h] = ring[r];
      put(start + j, p[0], p[1], h);
      cx += p[0]; cy += p[1];
    });
    put(start + CAP_RING.length, cx / CAP_RING.length, cy / CAP_RING.length, 0);
  });
  return out;
}

export function stationOfVertex(vertex, stations) {
  if (vertex < stations * RING) return Math.floor(vertex / RING);
  return vertex < stations * RING + CAP_RING.length + 1 ? 0 : stations - 1;
}

export function ringOfVertex(vertex, stations) {
  return vertex < stations * RING ? vertex % RING : -1;
}

// ---------- save / load ----------

export function exportState(blade, state) {
  return {
    blade: blade.id,
    version: blade.version,
    strikeIndex: state.strikeIndex,
    totalStrikes: blade.recipe.length,
    refinement: Array.from(state.refinement, (r) => Math.round(r * 10000) / 10000),
    quality: Math.round(quality(blade, state) * 100) / 100,
  };
}

// Rebuilds a state from saved data by replaying the recipe. Throws on anything invalid.
export function importState(blade, data) {
  if (!data || data.blade !== blade.id) throw new Error('state is for a different blade');
  if (data.version !== blade.version) throw new Error('state is for a different blade version');
  const k = data.strikeIndex;
  if (!Number.isInteger(k) || k < 0 || k > blade.recipe.length) throw new Error('invalid strikeIndex');
  const r = data.refinement;
  if (!Array.isArray(r) || r.length !== blade.stations) throw new Error('invalid refinement length');
  if (!r.every((v) => typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= 1)) throw new Error('refinement values must be 0–1');
  if (k < blade.recipe.length && r.some((v) => v > 0)) throw new Error('cannot grind before forging is complete');
  let state = createState(blade);
  for (let s = 0; s < k; s++) state = applyStrike(blade, state);
  state.refinement = Float64Array.from(r, (v) => (v >= 0.999 ? 1 : v));
  return state;
}

// Sampled stage shapes, for porting the profile without the curve maths.
export function exportProfile(blade) {
  const names = ['blank', 'lengthened', 'preform', 'forged', 'refined'];
  const shapes = {};
  blade.shapes.forEach((shape, k) => {
    shapes[names[k]] = Object.fromEntries(PARAMS.map((p) => [p, Array.from(shape[p], (v) => Math.round(v * 1e5) / 1e5)]));
  });
  return {
    blade: blade.id, version: blade.version, stations: blade.stations, units: 'cm',
    params: PARAMS, shapes,
    recipe: blade.recipe.map(({ stageIndex, ...s }) => s),
  };
}
