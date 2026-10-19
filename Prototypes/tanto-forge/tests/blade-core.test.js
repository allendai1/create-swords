// Run: npm test   (plain Node, no test framework; works on Node 14+)
import { readFileSync } from 'fs';
import assert from 'assert';
import * as core from '../dist/js/blade-core.js';

const load = (name) => JSON.parse(readFileSync(new URL(`../dist/data/${name}.json`, import.meta.url), 'utf8'));
const blank = load('blank');
const tanto = load('tanto');
const blade = core.createBlade(blank, tanto);
const N = blade.stations;
const index = core.buildIndex(N);

let passed = 0;
const failures = [];
function test(name, fn) {
  try { fn(); passed++; console.log(`  ok  ${name}`); }
  catch (e) { failures.push(name); console.log(`  FAIL ${name}\n       ${e.message}`); }
}

// Deterministic pseudo-random for repeatable "random" grinding.
let seed = 12345;
const rand = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);

function forgedState() {
  let s = core.createState(blade);
  while (!core.isForged(blade, s)) s = core.applyStrike(blade, s);
  return s;
}

function signedVolume(pos) {
  let v = 0;
  for (let t = 0; t < index.length; t += 3) {
    const a = index[t] * 3, b = index[t + 1] * 3, c = index[t + 2] * 3;
    v += pos[a] * (pos[b + 1] * pos[c + 2] - pos[b + 2] * pos[c + 1])
      - pos[a + 1] * (pos[b] * pos[c + 2] - pos[b + 2] * pos[c])
      + pos[a + 2] * (pos[b] * pos[c + 1] - pos[b + 1] * pos[c]);
  }
  return v / 6;
}

function checkGeometry(state, label) {
  const p = core.stationParams(blade, state);
  for (let i = 0; i < N; i++) {
    assert.ok(p.spine[i] > p.edge[i], `${label}: spine must stay above edge at station ${i}`);
    assert.ok(p.thick[i] > 0 && p.edgeT[i] > 0 && p.spineT[i] > 0, `${label}: thickness must stay positive at ${i}`);
    assert.ok(p.ridge[i] >= 0 && p.ridge[i] <= 1, `${label}: ridge outside blade at ${i}`);
    if (i < N - 1) assert.ok(p.segLen[i] > 0, `${label}: segment ${i} collapsed`);
  }
  const pos = core.buildPositions(p);
  assert.strictEqual(pos.length, core.vertexCount(N) * 3, `${label}: vertex count changed`);
  assert.ok(pos.every(Number.isFinite), `${label}: non-finite vertex`);
  assert.ok(signedVolume(pos) > 0, `${label}: mesh is inside-out or empty`);
  return pos;
}

console.log(`${blade.name}: ${N} stations, ${core.totalStrikes(blade)} strikes, ${core.vertexCount(N)} vertices`);

test('every forging stage covers the whole blade', () => {
  blade.minCoverage.forEach((c, k) => assert.ok(c > 0.15, `${core.STAGES[k]} min coverage ${c}`));
});

test('strike contributions sum to exactly one per station per stage', () => {
  core.STAGES.forEach((_, si) => {
    for (let i = 0; i < N; i++) {
      let sum = 0;
      blade.recipe.forEach((s, k) => { if (s.stageIndex === si) sum += blade.contrib[k][i]; });
      assert.ok(Math.abs(sum - 1) < 1e-9, `stage ${si} station ${i}: ${sum}`);
    }
  });
});

test('stage endpoints need no catch-up snap', () => {
  let s = core.createState(blade);
  for (let k = 0; k < core.totalStrikes(blade); k++) {
    s = core.applyStrike(blade, s);
    assert.ok(s.lastResidual < 1e-9, `strike ${k + 1} residual ${s.lastResidual}`);
  }
});

test('forging: each strike adds quality and all strikes reach exactly 90%', () => {
  let s = core.createState(blade);
  assert.strictEqual(core.quality(blade, s), 0);
  let prev = 0;
  while (!core.isForged(blade, s)) {
    s = core.applyStrike(blade, s);
    const q = core.quality(blade, s);
    assert.ok(q > prev, `quality did not rise at strike ${s.strikeIndex}`);
    prev = q;
  }
  assert.strictEqual(core.quality(blade, s), 90);
  assert.strictEqual(core.displayQuality(blade, s), 90);
  assert.strictEqual(core.applyStrike(blade, s), null, 'strikes after completion must be refused');
});

test('forging ends on the forged (90%) shape exactly', () => {
  const p = core.stationParams(blade, forgedState());
  for (const k of core.PARAMS) {
    for (let i = 0; i < N; i++) assert.ok(Math.abs(p[k][i] - blade.shapes[3][k][i]) < 1e-9, `${k}[${i}]`);
  }
});

test('grinding does nothing before forging is complete', () => {
  let s = core.createState(blade);
  for (let k = 0; k < 5; k++) s = core.applyStrike(blade, s);
  const g = core.applyGrind(blade, s, 0.5, 1);
  assert.ok(g.refinement.every((r) => r === 0));
  assert.strictEqual(core.quality(blade, g), core.quality(blade, s));
});

test('grinding only improves, never overcuts, and caps at 100%', () => {
  let s = forgedState();
  let prev = core.quality(blade, s);
  for (let k = 0; k < 400; k++) {
    s = core.applyGrind(blade, s, rand() * 1.1 - 0.05, rand() * 0.2);
    const q = core.quality(blade, s);
    assert.ok(q >= prev - 1e-12, `quality dropped ${prev} → ${q}`);
    assert.ok(q <= 100 + 1e-9, `quality above 100: ${q}`);
    prev = q;
    const p = core.stationParams(blade, s);
    for (let i = 0; i < N; i++) {
      const lo = Math.min(blade.shapes[3].edge[i], blade.shapes[4].edge[i]);
      const hi = Math.max(blade.shapes[3].edge[i], blade.shapes[4].edge[i]);
      assert.ok(p.edge[i] >= lo - 1e-9 && p.edge[i] <= hi + 1e-9, `edge ${i} past the target`);
    }
  }
  // Negative, zero and NaN input are ignored.
  const before = core.quality(blade, s);
  for (const bad of [-1, 0, NaN]) s = core.applyGrind(blade, s, 0.5, bad);
  s = core.applyGrind(blade, s, NaN, 0.5);
  assert.strictEqual(core.quality(blade, s), before);
});

test('full grind reaches exactly 100% and the refined shape', () => {
  let s = forgedState();
  for (let pass = 0; pass < 3; pass++) for (let u = 0; u <= 1.0001; u += 0.01) s = core.applyGrind(blade, s, u, 0.5);
  assert.ok(core.isRefined(blade, s));
  assert.strictEqual(core.quality(blade, s), 100);
  assert.strictEqual(core.displayQuality(blade, s), 100);
  const p = core.stationParams(blade, s);
  for (let i = 0; i < N; i++) assert.ok(Math.abs(p.edge[i] - blade.shapes[4].edge[i]) < 1e-9);
});

test('a few edge-to-edge passes finish the blade, ends included', () => {
  let s = forgedState();
  let passes = 0;
  while (!core.isRefined(blade, s) && passes < 20) {
    // One sweep base → point in 0.5 cm steps at the study's grind rate.
    for (let u = 0.02; u <= 0.98; u += 0.5 / 26) s = core.applyGrind(blade, s, u, 0.5 * core.GRIND_PER_CM);
    passes++;
  }
  assert.ok(core.isRefined(blade, s), `not refined after ${passes} passes`);
  assert.ok(passes >= 3 && passes <= 5, `took ${passes} passes`);
});

test('display quality never rounds up to unearned 100%', () => {
  let s = forgedState();
  for (let u = 0; u <= 1.0001; u += 0.01) s = core.applyGrind(blade, s, u, 0.5);
  s.refinement[N - 1] = 0.98;
  assert.ok(core.quality(blade, s) > 99.9);
  assert.strictEqual(core.displayQuality(blade, s), 99);
});

test('geometry stays finite, outward-facing and same-sized through every strike', () => {
  let s = core.createState(blade);
  checkGeometry(s, 'blank');
  while (!core.isForged(blade, s)) {
    s = core.applyStrike(blade, s);
    checkGeometry(s, `strike ${s.strikeIndex}`);
  }
  for (let k = 0; k < 50; k++) {
    s = core.applyGrind(blade, s, rand(), rand() * 0.3);
    checkGeometry(s, `grind ${k}`);
  }
});

test('end caps face outward (base toward −x, point toward +x)', () => {
  for (const st of [core.createState(blade), forgedState()]) {
    const pos = core.buildPositions(core.stationParams(blade, st));
    const capTris = index.length - 2 * 6 * 3;
    const normalX = (t) => {
      const [a, b, c] = [index[t], index[t + 1], index[t + 2]].map((v) => v * 3);
      const u = [pos[b] - pos[a], pos[b + 1] - pos[a + 1], pos[b + 2] - pos[a + 2]];
      const w = [pos[c] - pos[a], pos[c + 1] - pos[a + 1], pos[c + 2] - pos[a + 2]];
      return u[1] * w[2] - u[2] * w[1];
    };
    let base = 0, tip = 0;
    for (let t = capTris; t < capTris + 18; t += 3) base += normalX(t);
    for (let t = capTris + 18; t < index.length; t += 3) tip += normalX(t);
    assert.ok(base < 0, `base cap faces inward (${base})`);
    assert.ok(tip > 0, `point cap faces inward (${tip})`);
  }
});

test('in-between frames of an impact stay valid', () => {
  let s = core.createState(blade);
  while (!core.isForged(blade, s)) {
    const a = core.stationParams(blade, s);
    s = core.applyStrike(blade, s);
    const b = core.stationParams(blade, s);
    for (const t of [0.25, 0.5, 0.75]) {
      const pos = core.buildPositions(core.lerpParams(a, b, t));
      assert.ok(pos.every(Number.isFinite));
    }
  }
});

test('blank → forged: length grows from the universal blank to the tantō', () => {
  const len = (st) => core.stationParams(blade, st).segLen.reduce((x, y) => x + y, 0);
  assert.ok(Math.abs(len(core.createState(blade)) - blank.length) < 1e-9);
  assert.ok(Math.abs(len(forgedState()) - tanto.stages.refined.length) < 1e-9);
});

test('the blank shape comes only from the universal blank', () => {
  const alone = core.sampleShape(blank, N);
  for (const k of core.PARAMS) assert.deepStrictEqual(Array.from(blade.shapes[0][k]), Array.from(alone[k]));
});

test('every strike target sits on the blade', () => {
  let s = core.createState(blade);
  while (!core.isForged(blade, s)) {
    const t = core.strikeTarget(blade, core.stationParams(blade, s), s.strikeIndex);
    assert.ok(t.point.every(Number.isFinite) && t.thickness > 0 && t.halfWidth > 0);
    s = core.applyStrike(blade, s);
  }
});

test('export → import round-trips; reset gives a fresh blade', () => {
  let s = forgedState();
  s = core.applyGrind(blade, s, 0.3, 0.6);
  const saved = JSON.parse(JSON.stringify(core.exportState(blade, s)));
  const loaded = core.importState(blade, saved);
  assert.deepStrictEqual(core.exportState(blade, loaded), saved);
  assert.ok(Math.abs(core.quality(blade, loaded) - core.quality(blade, s)) < 0.01);
  const mid = core.importState(blade, { ...saved, strikeIndex: 7, refinement: new Array(N).fill(0) });
  assert.strictEqual(mid.strikeIndex, 7);
  const fresh = core.createState(blade);
  assert.strictEqual(core.quality(blade, fresh), 0);
  assert.ok(fresh.refinement.every((r) => r === 0));
});

test('import rejects invalid or tampered states', () => {
  const ok = core.exportState(blade, forgedState());
  const bad = [
    { ...ok, blade: 'katana' },
    { ...ok, version: 99 },
    { ...ok, strikeIndex: 13 },
    { ...ok, strikeIndex: 2.5 },
    { ...ok, refinement: ok.refinement.slice(1) },
    { ...ok, refinement: ok.refinement.map(() => 1.5) },
    { ...ok, refinement: ok.refinement.map(() => NaN) },
    { ...ok, strikeIndex: 3, refinement: ok.refinement.map(() => 0.5) },
  ];
  bad.forEach((b, i) => assert.throws(() => core.importState(blade, b), undefined, `case ${i}`));
});

test('profile export is plain JSON with every stage', () => {
  const p = JSON.parse(JSON.stringify(core.exportProfile(blade)));
  assert.deepStrictEqual(Object.keys(p.shapes), ['blank', 'lengthened', 'preform', 'forged', 'refined']);
  assert.strictEqual(p.shapes.refined.edge.length, N);
  assert.strictEqual(p.recipe.length, 12);
});

console.log(`\n${passed} passed, ${failures.length} failed`);
if (failures.length) process.exit(1);
