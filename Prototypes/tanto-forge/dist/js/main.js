// Browser rendering and input for the tantō study. Exploratory: the shape data and strike recipe
// (blade-core.js + data/*.json) are the parts meant to carry over to Roblox; this file is not.
import * as THREE from 'three';
import { RoomEnvironment } from '../vendor/RoomEnvironment.js';
import * as core from './blade-core.js';
import { createBladeMap, describeRuns, spotName } from './blade-map.js';

// ---------- exploratory pacing (not approved) ----------
const TIMING = { windup: 0.13, drop: 0.06, deform: 0.09, recover: 0.22, move: 0.34, cool: 0.9 };
const ANVIL_TOP = 0;
const TANG_LENGTH = 6;
const REDUCED_MOTION = matchMedia('(prefers-reduced-motion: reduce)').matches;

const $ = (id) => document.getElementById(id);
const lerp = (a, b, t) => a + (b - a) * t;
const easeOut = (t) => 1 - (1 - t) ** 3;
const easeIn = (t) => t * t * t;
const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);

const [blankData, tantoData] = await Promise.all(
  ['data/blank.json', 'data/tanto.json'].map((u) => fetch(u).then((r) => {
    if (!r.ok) throw new Error(`Could not load ${u}`);
    return r.json();
  })),
);
const blade = core.createBlade(blankData, tantoData);
const N = blade.stations;

// ---------- renderer, scene, camera ----------
const canvas = $('stage-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x15110e);
scene.fog = new THREE.Fog(0x15110e, 140, 260);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

scene.add(new THREE.HemisphereLight(0xffe6cc, 0x1a1210, 0.35));
const key = new THREE.DirectionalLight(0xfff1e0, 1.6);
key.position.set(-30, 60, 35);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -45, right: 45, top: 30, bottom: -30, near: 10, far: 160 });
key.shadow.bias = -0.0005;
scene.add(key);
const forgeGlow = new THREE.PointLight(0xff7a2a, 900, 120, 2);
forgeGlow.position.set(-48, 12, -30);
scene.add(forgeGlow);

const camera = new THREE.PerspectiveCamera(28, 1, 1, 600);
const lookAt = new THREE.Vector3(0, ANVIL_TOP, 0);
const cameraHome = new THREE.Vector3();
const maxStageLength = Math.max(blankData.length, ...Object.values(tantoData.stages).map((s) => s.length));
const REACH_X = TANG_LENGTH + maxStageLength + 3; // blade can extend this far either side of the hammer
const REACH_Z = 12;
// While grinding the blade stays put, so the camera can come in closer.
const GRIND_REACH_X = TANG_LENGTH + tantoData.stages.refined.length / 2 + 2;
const GRIND_REACH_Z = 7;
let grindFraming = false;
const view = { dist: 100, offsetY: 0, portrait: false };
const hudTop = document.querySelector('.hud-top');
const hudBottom = document.querySelector('.hud-bottom');

// Fit the blade's reach into the space between the top and bottom HUD, not the whole window.
function framing() {
  const w = innerWidth, h = innerHeight;
  const top = hudTop.getBoundingClientRect().bottom - 12;
  const bottom = h - hudBottom.getBoundingClientRect().top - 20;
  const free = Math.max(h * 0.35, h - top - bottom);
  const portrait = w / h < 0.85;
  const tanV = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
  const tanFreeV = (tanV * free) / h;
  const tanH = tanV * (w / h);
  // In portrait the blade runs up the screen instead of across it.
  const [tanAlong, tanAcross] = portrait ? [tanFreeV, tanH] : [tanH, tanFreeV];
  const [reach, reachZ] = grindFraming ? [GRIND_REACH_X, GRIND_REACH_Z] : [REACH_X, REACH_Z];
  return { dist: Math.max(reach / tanAlong, reachZ / tanAcross), offsetY: (bottom - top) / 2, portrait };
}

function applyView() {
  const w = innerWidth, h = innerHeight;
  const elevation = THREE.MathUtils.degToRad(64);
  cameraHome.set(0, Math.sin(elevation) * view.dist, Math.cos(elevation) * view.dist).add(lookAt);
  camera.up.set(view.portrait ? -1 : 0, view.portrait ? 0 : 1, 0);
  camera.position.copy(cameraHome);
  camera.lookAt(lookAt);
  camera.setViewOffset(w, h, 0, view.offsetY, w, h);
  scene.fog.near = view.dist + 40; // keep fog behind the anvil however far the camera sits
  scene.fog.far = view.dist + 160;
  camera.updateProjectionMatrix();
}

function fitCamera(duration = 0) {
  renderer.setSize(innerWidth, innerHeight, false);
  camera.aspect = innerWidth / innerHeight;
  const to = framing();
  if (!duration || to.portrait !== view.portrait) { Object.assign(view, to); applyView(); return Promise.resolve(); }
  const from = { ...view };
  return tween(duration, (t) => {
    const e = easeInOut(t);
    view.dist = lerp(from.dist, to.dist, e);
    view.offsetY = lerp(from.offsetY, to.offsetY, e);
    applyView();
  });
}
addEventListener('resize', () => { fitCamera(); drawMap(); });

// ---------- workshop props ----------
const iron = new THREE.MeshStandardMaterial({ color: 0x2c2b2d, metalness: 0.7, roughness: 0.5 });
function addMesh(geometry, material, position, parent = scene) {
  const m = new THREE.Mesh(geometry, material);
  m.position.copy(position);
  m.castShadow = m.receiveShadow = true;
  parent.add(m);
  return m;
}
addMesh(new THREE.BoxGeometry(24, 2, 7.5), iron, new THREE.Vector3(0, ANVIL_TOP - 1, 0));
addMesh(new THREE.BoxGeometry(12, 7, 5.5), iron, new THREE.Vector3(0, ANVIL_TOP - 5.5, 0));
addMesh(new THREE.BoxGeometry(20, 3, 10), iron, new THREE.Vector3(0, ANVIL_TOP - 10.5, 0));
const horn = addMesh(new THREE.ConeGeometry(3.6, 9, 24), iron, new THREE.Vector3(-16.5, ANVIL_TOP - 1.4, 0));
horn.rotation.z = Math.PI / 2;
horn.scale.set(1, 1, 0.7);
const wood = new THREE.MeshStandardMaterial({ color: 0x3b2a1e, roughness: 0.9 });
addMesh(new THREE.CylinderGeometry(13, 14, 10, 40), wood, new THREE.Vector3(0, ANVIL_TOP - 17, 0));
const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshStandardMaterial({ color: 0x1d1612, roughness: 1 }));
floor.rotation.x = -Math.PI / 2;
floor.position.y = ANVIL_TOP - 22;
floor.receiveShadow = true;
scene.add(floor);

// ---------- blade ----------
const pivot = new THREE.Group();   // sits on the anvil under the hammer; rotation = turn × flip
const bladeRoot = new THREE.Group(); // offset so the struck point lands on the pivot
pivot.add(bladeRoot);
scene.add(pivot);

const geometry = new THREE.BufferGeometry();
const posAttr = new THREE.BufferAttribute(new Float32Array(core.vertexCount(N) * 3), 3);
posAttr.setUsage(THREE.DynamicDrawUsage);
const colAttr = new THREE.BufferAttribute(new Float32Array(core.vertexCount(N) * 3), 3);
geometry.setAttribute('position', posAttr);
geometry.setAttribute('color', colAttr);
geometry.setIndex(new THREE.BufferAttribute(core.buildIndex(N), 1));

const bladeMat = new THREE.MeshStandardMaterial({ vertexColors: true, envMapIntensity: 1.2 });
const bladeMesh = new THREE.Mesh(geometry, bladeMat);
bladeMesh.castShadow = bladeMesh.receiveShadow = true;
bladeRoot.add(bladeMesh);

const tangMat = new THREE.MeshStandardMaterial({ color: 0x3a3430, metalness: 0.5, roughness: 0.8 });
addMesh(new THREE.BoxGeometry(TANG_LENGTH, 0.5, 1.8), tangMat, new THREE.Vector3(-TANG_LENGTH / 2, 0, -0.35), bladeRoot);

const vertexStation = Array.from({ length: core.vertexCount(N) }, (_, v) => core.stationOfVertex(v, N));
const vertexBevel = Array.from({ length: core.vertexCount(N) }, (_, v) => core.BEVEL_RING.has(core.ringOfVertex(v, N)));

function setGeometry(params) {
  core.buildPositions(params, posAttr.array);
  posAttr.needsUpdate = true;
  geometry.computeVertexNormals();
  geometry.computeBoundingSphere();
}

// Dull steel brightens per section as it is ground; bevels catch more light than the flats.
const DULL_FLAT = new THREE.Color(0.2, 0.2, 0.21), BRIGHT_FLAT = new THREE.Color(0.56, 0.57, 0.6);
const DULL_BEVEL = new THREE.Color(0.27, 0.27, 0.28), BRIGHT_BEVEL = new THREE.Color(0.95, 0.96, 0.98);
const tmpColor = new THREE.Color();
function setColors(refinement) {
  const a = colAttr.array;
  for (let v = 0; v < vertexStation.length; v++) {
    const r = refinement[vertexStation[v]];
    if (vertexBevel[v]) tmpColor.lerpColors(DULL_BEVEL, BRIGHT_BEVEL, r);
    else tmpColor.lerpColors(DULL_FLAT, BRIGHT_FLAT, r);
    a[v * 3] = tmpColor.r; a[v * 3 + 1] = tmpColor.g; a[v * 3 + 2] = tmpColor.b;
  }
  colAttr.needsUpdate = true;
}

const HOT_TINT = new THREE.Color(0.35, 0.12, 0.06), HOT_GLOW = new THREE.Color(1.0, 0.26, 0.03);
function setHeat(h) {
  bladeMat.color.setRGB(1, 1, 1).lerp(HOT_TINT, h);
  bladeMat.emissive.copy(HOT_GLOW).multiplyScalar(0.7 * h);
  bladeMat.metalness = lerp(0.9, 0.1, h);
  bladeMat.roughness = lerp(0.4, 0.6, h);
  bladeMat.envMapIntensity = lerp(1.2, 0.15, h);
  tangMat.emissive.copy(HOT_GLOW).multiplyScalar(0.25 * h);
}

// ---------- hammer (fixed point) ----------
const HANDLE = 15, HEAD_HALF = 2.2;
const hammer = new THREE.Group();
const wrapped = new THREE.MeshStandardMaterial({ color: 0x5a3e28, roughness: 0.85 });
const hammerSteel = new THREE.MeshStandardMaterial({ color: 0x3d3d40, metalness: 0.85, roughness: 0.35 });
const handle = addMesh(new THREE.CylinderGeometry(0.35, 0.42, HANDLE, 12), wrapped, new THREE.Vector3(0, 0, HANDLE / 2), hammer);
handle.rotation.x = Math.PI / 2;
addMesh(new THREE.CylinderGeometry(1.5, 1.5, HEAD_HALF * 2, 24), hammerSteel, new THREE.Vector3(0, 0, HANDLE), hammer);
scene.add(hammer);
const HAMMER_PIVOT_Y = ANVIL_TOP + 1.2 + HEAD_HALF;
hammer.position.set(0, HAMMER_PIVOT_Y, -HANDLE);
const REST = -0.38, WIND = -0.62, PARKED = -1.15;
hammer.rotation.x = REST;
// Angle at which the face meets a surface at height y.
const contactAngle = (y) => Math.asin(THREE.MathUtils.clamp((HAMMER_PIVOT_Y - HEAD_HALF - y) / HANDLE, -0.5, 0.5));

// ---------- strike circle ----------
const ring = new THREE.Mesh(
  new THREE.RingGeometry(1.15, 1.45, 48),
  new THREE.MeshBasicMaterial({ color: 0xfff4e2, transparent: true, opacity: 0.95, depthTest: false }),
);
ring.rotation.x = -Math.PI / 2;
ring.renderOrder = 10;
ring.visible = false;
scene.add(ring);

// ---------- sparks ----------
const SPARKS = 90;
const sparkPos = new Float32Array(SPARKS * 3);
const sparkVel = new Float32Array(SPARKS * 3);
const sparkLife = new Float32Array(SPARKS);
const sparkGeo = new THREE.BufferGeometry();
sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
const sparkMat = new THREE.PointsMaterial({ color: 0xffb35c, size: 0.4, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
const sparks = new THREE.Points(sparkGeo, sparkMat);
sparks.frustumCulled = false;
scene.add(sparks);
let sparkCursor = 0;
function emitSparks(at, count, speed, color) {
  sparkMat.color.set(color);
  for (let n = 0; n < count; n++) {
    const i = sparkCursor++ % SPARKS;
    const a = Math.random() * Math.PI * 2, up = 0.4 + Math.random() * 0.8;
    sparkPos.set([at.x, at.y + 0.2, at.z], i * 3);
    sparkVel.set([Math.cos(a) * speed * (0.4 + Math.random()), up * speed, Math.sin(a) * speed * (0.4 + Math.random())], i * 3);
    sparkLife[i] = 0.25 + Math.random() * 0.35;
  }
}
function updateSparks(dt) {
  for (let i = 0; i < SPARKS; i++) {
    if (sparkLife[i] <= 0) { sparkPos[i * 3 + 1] = -999; continue; }
    sparkLife[i] -= dt;
    sparkVel[i * 3 + 1] -= 60 * dt;
    for (let k = 0; k < 3; k++) sparkPos[i * 3 + k] += sparkVel[i * 3 + k] * dt;
  }
  sparkGeo.attributes.position.needsUpdate = true;
}

// ---------- whetstone (grinding cursor) ----------
const stone = addMesh(new THREE.BoxGeometry(3.2, 1.0, 1.4), new THREE.MeshStandardMaterial({ color: 0x8c8a80, roughness: 0.95 }), new THREE.Vector3());
stone.visible = false;

// Target edge shown while grinding, so it is clear where the stone stops.
const outlineGeo = new THREE.BufferGeometry();
outlineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
const outline = new THREE.Line(outlineGeo, new THREE.LineDashedMaterial({ color: 0xf3d9b0, dashSize: 0.5, gapSize: 0.35, transparent: true, opacity: 0.75 }));
outline.visible = false;
bladeRoot.add(outline);
function updateOutline(params) {
  const target = blade.shapes[4];
  const { px, py, angle } = core.centerline(params);
  const a = outlineGeo.attributes.position.array;
  for (let i = 0; i < N; i++) {
    const ridgeY = params.spine[i] + params.ridge[i] * (params.edge[i] - params.spine[i]);
    const frac = (target.edge[i] - params.edge[i]) / (ridgeY - params.edge[i] || 1);
    const h = params.edgeT[i] / 2 + frac * (params.thick[i] / 2 - params.edgeT[i] / 2) + 0.04;
    const x = px[i] - Math.sin(angle[i]) * target.edge[i];
    const y = py[i] + Math.cos(angle[i]) * target.edge[i];
    a.set([x, h, -y], i * 3);
  }
  outlineGeo.attributes.position.needsUpdate = true;
  outline.computeLineDistances();
}

// ---------- sound ----------
let audio = null, soundOn = true, grindGain = null;
function ensureAudio() {
  if (audio || !soundOn) return;
  const Ctx = window.AudioContext || window.webkitAudioContext;
  if (!Ctx) return;
  audio = new Ctx();
  const noise = audio.createBuffer(1, audio.sampleRate, audio.sampleRate);
  const d = noise.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  const src = audio.createBufferSource();
  src.buffer = noise; src.loop = true;
  const band = audio.createBiquadFilter();
  band.type = 'bandpass'; band.frequency.value = 2600; band.Q.value = 0.8;
  grindGain = audio.createGain(); grindGain.gain.value = 0;
  src.connect(band).connect(grindGain).connect(audio.destination);
  src.start();
}
function clang(strength = 1) {
  if (!audio || !soundOn) return;
  const t = audio.currentTime;
  const out = audio.createGain();
  out.gain.value = 0.22 * strength;
  out.connect(audio.destination);
  [[523, 0.5, 0.9], [1247, 0.3, 0.6], [1981, 0.18, 0.4], [2713, 0.1, 0.25]].forEach(([f, g, decay]) => {
    const o = audio.createOscillator(), e = audio.createGain();
    o.frequency.value = f * (0.98 + Math.random() * 0.04);
    e.gain.setValueAtTime(g, t);
    e.gain.exponentialRampToValueAtTime(0.0001, t + decay);
    o.connect(e).connect(out);
    o.start(t); o.stop(t + decay + 0.05);
  });
}
function setGrindSound(level) {
  if (!grindGain) return;
  grindGain.gain.setTargetAtTime(soundOn ? level : 0, audio.currentTime, 0.04);
}

// ---------- tweening ----------
const tweens = new Set();
let clock = performance.now();
function tween(duration, fn) {
  return new Promise((resolve) => {
    if (duration <= 0) { fn(1); resolve(); return; }
    tweens.add({ start: clock, duration: duration * 1000, fn, resolve });
  });
}
function runTweens(now) {
  for (const tw of tweens) {
    const t = Math.min(1, Math.max(0, (now - tw.start) / tw.duration));
    tw.fn(t);
    if (t >= 1) { tweens.delete(tw); tw.resolve(); }
  }
}

// ---------- pose: put a point of the blade under the hammer ----------
const pose = { point: new THREE.Vector3(), yaw: 0, flip: 0, thickness: 1, lift: 0 };
const qYaw = new THREE.Quaternion(), qFlip = new THREE.Quaternion();
const Y = new THREE.Vector3(0, 1, 0), X = new THREE.Vector3(1, 0, 0);
function applyPose() {
  qYaw.setFromAxisAngle(Y, pose.yaw);
  qFlip.setFromAxisAngle(X, pose.flip * Math.PI);
  pivot.quaternion.multiplyQuaternions(qYaw, qFlip);
  pivot.position.set(0, ANVIL_TOP + pose.thickness / 2 + pose.lift, 0);
  bladeRoot.position.copy(pose.point).negate();
}
function poseFor(target) {
  return {
    point: new THREE.Vector3(...target.point),
    yaw: (target.flip ? target.angle : -target.angle) + target.turn,
    flip: target.flip ? 1 : 0,
    thickness: target.thickness,
    halfWidth: target.halfWidth,
  };
}
async function moveTo(next, duration) {
  const from = { point: pose.point.clone(), yaw: pose.yaw, flip: pose.flip, thickness: pose.thickness };
  const flipping = from.flip !== next.flip;
  const liftHeight = flipping ? (next.halfWidth || 1.5) + 0.8 : 0.25;
  await tween(duration, (t) => {
    const e = easeInOut(t);
    pose.point.lerpVectors(from.point, next.point, e);
    pose.yaw = lerp(from.yaw, next.yaw, e);
    pose.flip = lerp(from.flip, next.flip, e);
    pose.thickness = lerp(from.thickness, next.thickness, e);
    pose.lift = Math.sin(Math.PI * t) * liftHeight;
    applyPose();
  });
  pose.lift = 0;
  applyPose();
}

// ---------- game state ----------
let state = core.createState(blade);
let params = core.stationParams(blade, state);
let mode = 'ready'; // ready | busy | grind | done
let queued = false;
let heat = 1;
let shake = 0;
const scratch = {};

function contactY(target) { return ANVIL_TOP + pose.thickness / 2 + target.thickness / 2; }

function showRing() {
  const target = core.strikeTarget(blade, params, state.strikeIndex);
  ring.position.set(0, contactY(target) + 0.05, 0);
  ring.visible = true;
}

async function strike() {
  if (mode !== 'ready') {
    if (mode === 'busy' && !core.isForged(blade, state)) queued = true;
    return;
  }
  mode = 'busy';
  ring.visible = false;
  const k = state.strikeIndex;
  const target = core.strikeTarget(blade, params, k);
  const hitAngle = contactAngle(contactY(target));
  await tween(TIMING.windup, (t) => { hammer.rotation.x = lerp(REST, WIND, easeOut(t)); });
  await tween(TIMING.drop, (t) => { hammer.rotation.x = lerp(WIND, hitAngle, easeIn(t)); });

  // Contact: the struck section changes, the rest follows, and the struck point stays under the hammer.
  const before = params;
  state = core.applyStrike(blade, state);
  const after = core.stationParams(blade, state);
  emitSparks(new THREE.Vector3(0, contactY(target), 0), 26, 22, 0xffb35c);
  clang(1);
  if (!REDUCED_MOTION) shake = 0.35;
  updateHud();
  await Promise.all([
    tween(TIMING.deform, (t) => {
      params = core.lerpParams(before, after, easeOut(t), scratch);
      setGeometry(params);
      pose.point.set(...core.strikeTarget(blade, params, k).point);
      applyPose();
    }),
    tween(TIMING.recover, (t) => { hammer.rotation.x = lerp(hitAngle, REST, easeOut(t)); }),
  ]);
  params = after;

  if (core.isForged(blade, state)) {
    queued = false;
    await finishForging();
    return;
  }
  await moveTo(poseFor(core.strikeTarget(blade, params, state.strikeIndex)), TIMING.move);
  mode = 'ready';
  showRing();
  if (queued) { queued = false; strike(); }
}

async function finishForging() {
  const mid = Math.round((N - 1) / 2);
  const { px, py, angle } = core.centerline(params);
  const across = (params.spine[mid] + params.edge[mid]) / 2;
  const centre = {
    point: new THREE.Vector3(px[mid] - Math.sin(angle[mid]) * across, 0, -(py[mid] + Math.cos(angle[mid]) * across)),
    yaw: -angle[mid], flip: 0, thickness: params.thick[mid], halfWidth: 1.5,
  };
  await Promise.all([
    tween(0.5, (t) => { hammer.rotation.x = lerp(REST, PARKED, easeInOut(t)); }),
    moveTo(centre, 0.6),
    tween(TIMING.cool, (t) => { heat = 1 - easeInOut(t); setHeat(heat); }),
  ]);
  updateOutline(params);
  outline.visible = true;
  mode = 'grind';
  updateHud();
  grindFraming = true;
  await fitCamera(0.6);
}

// ---------- grinding ----------
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
let grinding = false;
let lastGrindPoint = null;
let grindSoundUntil = 0;

function pick(event) {
  const rect = canvas.getBoundingClientRect();
  pointer.set(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObject(bladeMesh, false)[0];
  if (!hit) return null;
  const v = hit.face.a;
  const station = vertexStation[v];
  const onEdge = vertexBevel[v] || (core.ringOfVertex(v, N) < 0 && station === N - 1);
  return { point: hit.point, u: station / (N - 1), onEdge };
}

function grindAt(event) {
  const hit = pick(event);
  if (!hit) { stone.visible = false; lastGrindPoint = null; setMapMarker(null); return; }
  stone.visible = true;
  setMapMarker(hit.u);
  stone.position.copy(hit.point).add(new THREE.Vector3(0, 0.6, 0));
  stone.rotation.y = pivot.rotation.y + 0.3;
  if (!grinding) { lastGrindPoint = null; return; }
  if (!hit.onEdge) { setHint('Grind along the edge, the bright bevel side of the blade.', true); lastGrindPoint = hit.point.clone(); return; }
  if (lastGrindPoint) {
    const cm = Math.min(3, hit.point.distanceTo(lastGrindPoint));
    if (cm > 0.01) {
      const was = core.quality(blade, state);
      state = core.applyGrind(blade, state, hit.u, cm * core.GRIND_PER_CM);
      if (core.quality(blade, state) > was) {
        params = core.stationParams(blade, state);
        setGeometry(params);
        setColors(state.refinement);
        updateOutline(params);
        emitSparks(hit.point, 3, 10, 0xfff0c8);
        grindSoundUntil = clock + 90;
        updateHud();
      }
    }
  }
  lastGrindPoint = hit.point.clone();
  if (core.isRefined(blade, state)) finishGrinding();
}

function finishGrinding() {
  mode = 'done';
  grinding = false;
  stone.visible = false;
  outline.visible = false;
  setGrindSound(0);
  mapMarkerU = null;
  updateHud();
  fitCamera(0.3);
}

// ---------- input ----------
function ringHit(event) {
  if (!ring.visible) return false;
  const p = ring.position.clone().project(camera);
  const rect = canvas.getBoundingClientRect();
  const sx = ((p.x + 1) / 2) * rect.width + rect.left, sy = ((1 - p.y) / 2) * rect.height + rect.top;
  const edge = ring.position.clone().add(new THREE.Vector3(1.45, 0, 0)).project(camera);
  const radiusPx = Math.abs(((edge.x - p.x) / 2) * rect.width) + Math.abs(((edge.y - p.y) / 2) * rect.height);
  return Math.hypot(event.clientX - sx, event.clientY - sy) < Math.max(56, radiusPx * 2.2);
}

canvas.addEventListener('pointerdown', (event) => {
  ensureAudio();
  if (audio && audio.state === 'suspended') audio.resume();
  if (mode === 'ready' || mode === 'busy') {
    if (mode === 'busy' || ringHit(event)) strike();
    else setHint('Strike inside the circle.', true);
  } else if (mode === 'grind') {
    grinding = true;
    canvas.setPointerCapture(event.pointerId);
    grindAt(event);
  }
});
canvas.addEventListener('pointermove', (event) => {
  if (mode === 'grind') grindAt(event);
  else stone.visible = false;
  if (mode === 'ready') canvas.style.cursor = ringHit(event) ? 'pointer' : 'default';
  else canvas.style.cursor = mode === 'grind' ? 'crosshair' : 'default';
});
const stopGrinding = () => { grinding = false; lastGrindPoint = null; if (mode === 'grind') updateHud(); };
canvas.addEventListener('pointerup', stopGrinding);
canvas.addEventListener('pointercancel', stopGrinding);
canvas.addEventListener('pointerleave', () => { if (!grinding) { stone.visible = false; setMapMarker(null); } });

addEventListener('keydown', (event) => {
  if (event.target.closest && event.target.closest('textarea, button')) return;
  if (event.code === 'Space' || event.code === 'Enter') {
    event.preventDefault();
    ensureAudio();
    strike();
  }
});

// ---------- HUD ----------
const STAGE_NAMES = { lengthen: 'Lengthen', taper: 'Taper & curve', tip: 'Point' };
const STAGE_LINES = {
  lengthen: 'Stage 1 of 3 · Lengthen the blank',
  taper: 'Stage 2 of 3 · Taper and curve',
  tip: 'Stage 3 of 3 · Form the point',
};
const tally = $('tally');
const marks = [];
core.STAGES.forEach((stage) => {
  const li = document.createElement('li');
  li.dataset.stage = stage;
  const row = document.createElement('div');
  row.className = 'marks';
  blade.recipe.forEach((s) => {
    if (s.stage !== stage) return;
    const m = document.createElement('span');
    m.className = 'mark';
    row.append(m);
    marks.push(m);
  });
  const label = document.createElement('span');
  label.className = 'label';
  label.textContent = STAGE_NAMES[stage];
  li.append(row, label);
  tally.append(li);
});
const grindLi = document.createElement('li');
grindLi.dataset.stage = 'grind';
grindLi.innerHTML = '<div class="marks"><span class="mark grind"><span id="grind-fill"></span></span></div><span class="label">Grind · optional</span>';
tally.append(grindLi);

// ---------- grinding map ----------
const bladeMap = createBladeMap($('map-canvas'), { stations: N, tangLength: TANG_LENGTH, tangHalfWidth: 0.9, tangOffset: 0.35 });
let mapMarkerU = null;
function setMapMarker(u) {
  if (u === mapMarkerU) return;
  mapMarkerU = u;
  drawMap();
}
function drawMap() {
  if ($('blade-map').hidden) return;
  const runs = core.unfinishedRuns(blade, state);
  bladeMap.draw(params, state.refinement, runs, mapMarkerU);
  const ground = Math.floor(((core.quality(blade, state) - core.FORGED_QUALITY) / (core.MAX_QUALITY - core.FORGED_QUALITY)) * 100 + 1e-9);
  $('map-pct').textContent = `${runs.length ? Math.min(ground, 99) : 100}%`;
  const left = $('map-left');
  const where = describeRuns(runs, N);
  left.textContent = runs.length ? `Still to grind: ${where}` : 'Whole edge ground';
  left.classList.toggle('done', !runs.length);
  $('map-canvas').setAttribute('aria-label', `Blade diagram. ${left.textContent}.`);
}
const mapCanvas = $('map-canvas');
mapCanvas.addEventListener('pointermove', (event) => {
  const i = bladeMap.stationAt(event.clientX);
  const tip = $('map-tip');
  if (i < 0) { tip.hidden = true; return; }
  const r = state.refinement[i];
  const where = spotName(i / (N - 1));
  tip.textContent = `${where[0].toUpperCase()}${where.slice(1)} · ${r >= 1 ? 'ground' : `${Math.floor(r * 100)}% ground`}`;
  tip.style.left = `${event.clientX - mapCanvas.getBoundingClientRect().left}px`;
  tip.hidden = false;
});
mapCanvas.addEventListener('pointerleave', () => { $('map-tip').hidden = true; });

let hintTimer = 0;
function setHint(text, nudge = false) {
  const el = $('hint');
  el.textContent = text;
  el.classList.toggle('nudge', nudge);
  clearTimeout(hintTimer);
  if (nudge) hintTimer = setTimeout(updateHud, 1600);
}

function updateHud() {
  const k = state.strikeIndex;
  const forged = core.isForged(blade, state);
  const q = core.displayQuality(blade, state);
  $('quality').textContent = q;
  marks.forEach((m, i) => { m.classList.toggle('done', i < k); m.classList.toggle('next', i === k); });
  const currentStage = forged ? 'grind' : blade.recipe[k].stage;
  tally.querySelectorAll('li').forEach((li) => li.classList.toggle('current', li.dataset.stage === currentStage));
  const refined = forged ? (core.quality(blade, state) - core.FORGED_QUALITY) / (core.MAX_QUALITY - core.FORGED_QUALITY) : 0;
  $('grind-fill').style.width = `${(refined * 100).toFixed(1)}%`;
  $('blade-map').hidden = !forged;
  tally.hidden = forged; // the map takes over once forging is done
  drawMap();
  const stageLine = $('stage-line');
  stageLine.classList.toggle('cool', forged);
  const touch = matchMedia('(pointer: coarse)').matches;
  if (!forged) {
    stageLine.textContent = STAGE_LINES[blade.recipe[k].stage];
    $('quality-note').textContent = `Strike ${Math.min(k + 1, blade.recipe.length)} of ${blade.recipe.length}`;
    setHint(touch ? 'Tap the circle to strike.' : 'Click the circle or press Space to strike.');
  } else if (mode === 'done' || core.isRefined(blade, state)) {
    stageLine.textContent = 'Finished · fully refined';
    $('quality-note').textContent = 'Ready for the hilt';
    setHint('Fully refined. Start over to forge another.');
  } else {
    stageLine.textContent = 'Forged · optional grinding';
    $('quality-note').textContent = q > 90 ? 'Grinding' : 'Forged, ready for the hilt';
    setHint(`${touch ? 'Drag' : 'Hold and drag'} along the edge. Grind until the whole edge on the map is bright.`);
  }
}

// ---------- reset / data ----------
function loadState(next) {
  tweens.clear();
  state = next;
  params = core.stationParams(blade, state);
  setGeometry(params);
  setColors(state.refinement);
  queued = false; grinding = false; stone.visible = false;
  const forged = core.isForged(blade, state);
  heat = forged ? 0 : 1;
  setHeat(heat);
  if (forged) {
    hammer.rotation.x = PARKED;
    mode = core.isRefined(blade, state) ? 'done' : 'grind';
    ring.visible = false;
    const mid = Math.round((N - 1) / 2);
    const { px, py, angle } = core.centerline(params);
    const across = (params.spine[mid] + params.edge[mid]) / 2;
    Object.assign(pose, { yaw: -angle[mid], flip: 0, thickness: params.thick[mid], lift: 0 });
    pose.point.set(px[mid] - Math.sin(angle[mid]) * across, 0, -(py[mid] + Math.cos(angle[mid]) * across));
    applyPose();
    updateOutline(params);
    outline.visible = mode === 'grind';
  } else {
    hammer.rotation.x = REST;
    mode = 'ready';
    const p = poseFor(core.strikeTarget(blade, params, state.strikeIndex));
    Object.assign(pose, { yaw: p.yaw, flip: p.flip, thickness: p.thickness, lift: 0 });
    pose.point.copy(p.point);
    applyPose();
    outline.visible = false;
    showRing();
  }
  grindFraming = forged;
  mapMarkerU = null;
  updateHud();
  fitCamera();
}

$('btn-reset').addEventListener('click', () => loadState(core.createState(blade)));

let dataView = 'state';
function showData(view) {
  dataView = view;
  const json = view === 'state' ? core.exportState(blade, state) : core.exportProfile(blade);
  $('data-text').value = JSON.stringify(json, null, view === 'state' ? 2 : 1);
  $('btn-show-state').classList.toggle('primary', view === 'state');
  $('btn-show-profile').classList.toggle('primary', view === 'profile');
  $('btn-load').disabled = view !== 'state';
  $('data-status').textContent = '';
}
function openSheet(id) { $(id).hidden = false; $(id).querySelector('button').focus(); }
function closeSheet(id) { $(id).hidden = true; canvas.focus?.(); }
$('btn-data').addEventListener('click', () => { showData('state'); openSheet('data-sheet'); });
$('btn-show-state').addEventListener('click', () => showData('state'));
$('btn-show-profile').addEventListener('click', () => showData('profile'));
$('btn-close-data').addEventListener('click', () => closeSheet('data-sheet'));
$('btn-copy').addEventListener('click', () => {
  const text = $('data-text').value;
  navigator.clipboard.writeText(text).then(
    () => { $('data-status').textContent = 'Copied'; },
    () => { $('data-text').select(); $('data-status').textContent = 'Copy blocked here. The text is selected; press Ctrl/Cmd+C.'; },
  );
});
$('btn-load').addEventListener('click', () => {
  try {
    loadState(core.importState(blade, JSON.parse($('data-text').value)));
    $('data-status').textContent = 'Loaded';
  } catch (e) {
    $('data-status').textContent = `Could not load: ${e.message}.`;
  }
});
$('btn-about').addEventListener('click', () => openSheet('about-sheet'));
$('btn-close-about').addEventListener('click', () => closeSheet('about-sheet'));
document.querySelectorAll('.sheet-backdrop').forEach((b) => b.addEventListener('click', (e) => { if (e.target === b) closeSheet(b.id); }));
addEventListener('keydown', (e) => { if (e.key === 'Escape') document.querySelectorAll('.sheet-backdrop').forEach((b) => closeSheet(b.id)); });
$('btn-sound').addEventListener('click', () => {
  soundOn = !soundOn;
  $('btn-sound').textContent = soundOn ? 'Sound on' : 'Sound off';
  $('btn-sound').setAttribute('aria-pressed', String(soundOn));
  if (soundOn) ensureAudio(); else setGrindSound(0);
});

// ---------- loop ----------
function step(now) {
  const dt = Math.min(0.05, Math.max(0, (now - clock) / 1000));
  clock = now;
  runTweens(now);
  updateSparks(dt);
  if (ring.visible) {
    const s = 1 + Math.sin(now / 260) * 0.06;
    ring.scale.set(s, s, s);
  }
  if (grindGain) setGrindSound(now < grindSoundUntil ? 0.08 : 0);
  camera.position.copy(cameraHome);
  if (shake > 0) {
    shake = Math.max(0, shake - dt * 3);
    camera.position.x += (Math.random() - 0.5) * shake;
    camera.position.z += (Math.random() - 0.5) * shake;
  }
  camera.lookAt(lookAt);
  renderer.render(scene, camera);
}
function frame(now) {
  step(Math.max(now, clock)); // never run time backwards (advance() may have stepped ahead)
  requestAnimationFrame(frame);
}

loadState(state);
$('loading').hidden = true;
requestAnimationFrame(frame);

// Debug/inspection handle for the study (not gameplay).
window.forgeStudy = { blade, core, get state() { return state; }, get mode() { return mode; }, get heat() { return heat; }, bladeMat, bladeMesh, camera, canvas, ring, pose, tweens, strike, loadState,
  // Steps the scene without requestAnimationFrame (for checks in a hidden tab).
  advance(ms) { for (let t = 0; t < ms; t += 16) step(clock + 16); } };
