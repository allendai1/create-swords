(() => {
const S = 512, C = 64;
const mulberry = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const R = mulberry(7);
const cv = document.createElement('canvas'); cv.width = cv.height = S;
const g = cv.getContext('2d');
const blotch = (cx, cy, cols, n, a0, a1, r0, r1) => {
  for (let i = 0; i < n; i++) {
    g.globalAlpha = a0 + R() * (a1 - a0); g.fillStyle = cols[i % cols.length];
    g.beginPath(); g.ellipse(cx * C + R() * C, cy * C + R() * C, r0 + R() * (r1 - r0), (r0 + R() * (r1 - r0)) * 0.6, R() * 3, 0, 7); g.fill();
  }
  g.globalAlpha = 1;
};
const clipCell = (cx, cy, fn) => { g.save(); g.beginPath(); g.rect(cx * C, cy * C, C, C); g.clip(); fn(); g.restore(); };
const vgrad = (cx, cy, stops) => {
  const gr = g.createLinearGradient(0, cy * C, 0, cy * C + C);
  stops.forEach(([p, c]) => gr.addColorStop(p, c)); g.fillStyle = gr; g.fillRect(cx * C, cy * C, C, C);
};
const crack = (cx, cy, col) => {
  g.strokeStyle = col; g.globalAlpha = 0.35; g.lineWidth = 1;
  let x = cx * C + 8 + R() * 48, y = cy * C + 10 + R() * 30; g.beginPath(); g.moveTo(x, y);
  for (let k = 0; k < 4; k++) { x += (R() - 0.5) * 14; y += 3 + R() * 6; g.lineTo(x, y); }
  g.stroke(); g.globalAlpha = 1;
};
const ROCK = [
  ['#a6b0bb', '#78838f', '#3b424c', '#b4bec8'],
  ['#a9a8a6', '#7e7c7a', '#41403f', '#b8b6b2'],
  ['#9fa9a8', '#737e7e', '#3b4344', '#adb7b6'],
  ['#a7abb1', '#7a7f86', '#3f4349', '#b6babf'],
];
ROCK.forEach(([top, mid, bot, lit], v) => {
  clipCell(v, 0, () => {
    vgrad(v, 0, [[0, lit], [0.1, top], [0.4, mid], [1, bot]]);
    blotch(v, 0, [top, bot, mid], 40, 0.05, 0.14, 4, 14);
    if (R() < 0.8) crack(v, 0, bot);
  });
  clipCell(v + 4, 0, () => {
    g.fillStyle = top; g.fillRect((v + 4) * C, 0, C, C);
    blotch(v + 4, 0, [lit, mid, '#8f9a8c'], 36, 0.06, 0.16, 5, 16);
    crack(v + 4, 0, mid);
  });
});
clipCell(0, 1, () => { g.fillStyle = '#30353c'; g.fillRect(0, C, C, C); blotch(0, 1, ['#262a30', '#3a4048'], 24, 0.1, 0.2, 4, 12); });
const plank = (cx, cy, vertical, dark) => clipCell(cx, cy, () => {
  g.save();
  if (vertical) { g.translate(cx * C + C, cy * C); g.rotate(Math.PI / 2); g.translate(-cx * C, -cy * C); }
  const x0 = cx * C, y0 = cy * C;
  g.fillStyle = '#c08447'; g.fillRect(x0, y0, C, C);
  blotch(cx, cy, ['#cf9558', '#a96f38'], 20, 0.1, 0.25, 6, 20);
  g.strokeStyle = '#86552a'; g.lineWidth = 1.2;
  for (let k = 0; k < 7; k++) {
    g.globalAlpha = 0.35 + R() * 0.3; g.beginPath();
    let y = y0 + 8 + k * 7 + R() * 3; g.moveTo(x0, y);
    for (let x = 0; x <= C; x += 8) g.lineTo(x0 + x, y + Math.sin(x * 0.11 + k) * 1.5);
    g.stroke();
  }
  g.globalAlpha = 1; g.fillStyle = '#e0aa70'; g.fillRect(x0, y0, C, 3);
  g.fillStyle = '#6e4220'; g.fillRect(x0, y0 + C - 3, C, 3);
  g.restore();
  if (dark) { g.fillStyle = '#000'; g.globalAlpha = dark; g.fillRect(cx * C, cy * C, C, C); g.globalAlpha = 1; }
});
plank(1, 1, false, 0); plank(2, 1, true, 0); plank(5, 1, false, 0.55); plank(6, 1, false, 0.75);
clipCell(3, 1, () => {
  g.fillStyle = '#a8723d'; g.fillRect(3 * C, C, C, C); g.strokeStyle = '#7a4c25'; g.lineWidth = 1.5;
  for (let r = 6; r < 46; r += 7) { g.globalAlpha = 0.5; g.beginPath(); g.arc(3 * C + 30, C + 34, r, 0, 7); g.stroke(); }
  g.globalAlpha = 1;
});
clipCell(4, 1, () => {
  g.fillStyle = '#d8bd7c'; g.fillRect(4 * C, C, C, C); g.strokeStyle = '#9e7f43'; g.lineWidth = 3;
  for (let k = -C; k < 2 * C; k += 9) { g.beginPath(); g.moveTo(4 * C + k, C); g.lineTo(4 * C + k + C, 2 * C); g.stroke(); }
});
g.fillStyle = '#050506'; g.fillRect(7 * C, C, C, C);
['#3b4048', '#2b2f35', '#1e2125', '#131518', '#0a0b0c'].forEach((c, i) => clipCell(i, 2, () => {
  g.fillStyle = c; g.fillRect(i * C, 2 * C, C, C); blotch(i, 2, ['#000', '#5a606a'], 18, 0.06, 0.14 - i * 0.02, 4, 14);
}));
const tex = new Texture({ name: 'mine_entrance' }).fromDataURL(cv.toDataURL('image/png'));
tex.uv_width = S; tex.uv_height = S;
Project.texture_width = S; Project.texture_height = S;

Undo.initEdit({ outliner: true, elements: [], textures: [] });
tex.add(false);
const made = [];
const grp = n => { const gr = new Group({ name: n, origin: [0, 0, 0] }).init(); return gr; };
const G = { rocks: grp('Rocks'), portal: grp('Portal'), tunnel: grp('Tunnel') };
const BB = ([x, y, z]) => [x * 10, z * 10, -y * 10];
const cellUV = ([cx, cy]) => [cx * C + 3, cy * C + 3, cx * C + C - 3, cy * C + C - 3];
const cube = (name, group, c, s, rot, cells) => {
  const [X, Y, Z] = BB(c), sx = s[0] * 5, sy = s[2] * 5, sz = s[1] * 5;
  const faces = {};
  for (const f of ['north', 'south', 'east', 'west', 'up', 'down']) faces[f] = { uv: cellUV(cells[f] || cells.side), texture: tex.uuid };
  const cb = new Cube({ name, from: [X - sx, Y - sy, Z - sz], to: [X + sx, Y + sy, Z + sz], origin: [X, Y, Z], rotation: rot || [0, 0, 0], faces });
  cb.addTo(group).init(); made.push(cb); return cb;
};
const PLANK = { side: [1, 1], east: [3, 1], west: [3, 1] };
const POST = { side: [2, 1], up: [3, 1], down: [3, 1] };
const ROPE = { side: [4, 1] };

const POST_X = 2.05, POST_Y = -2.4, POST_W = 0.55;
[-1, 1].forEach((s, i) => {
  const h = 3.4 + 0.03 * i, yaw = (i ? -2.5 : 2);
  cube(`Post${i}`, G.portal, [s * POST_X, POST_Y, h / 2 - 0.1], [POST_W, POST_W, h], [0, yaw, 0], POST);
  [2.85, 3.02].forEach((z, k) => cube(`Lash${i}${k}`, G.portal, [s * POST_X, POST_Y, z], [0.68, 0.68, 0.13], [0, yaw + 8 * k, 0], ROPE));
  [0, 0.17].forEach((dx, k) => cube(`LintelLash${i}${k}`, G.portal, [s * (POST_X + 0.25 + dx), POST_Y, 3.525], [0.12, 0.78, 0.67], [0, 0, -1.2], ROPE));
});
cube('Lintel', G.portal, [0, -2.4, 3.525], [6.0, 0.66, 0.55], [0, 0, -1.2], PLANK);
const RW = mulberry(31);
let py = -3.15;
[0.66, 0.58, 0.64, 0.55, 0.6].forEach((w, i) => {
  const x0 = -3.03 + RW() * 0.4 - 0.25, x1 = 3.03 + RW() * 0.4 - 0.15, t = 0.2 + 0.02 * (i % 3);
  cube(`Roof${i}`, G.portal, [(x0 + x1) / 2, py + w / 2, 3.76 + t / 2 + 0.01 * (i % 2)], [x1 - x0, w, t], [(RW() - 0.5) * 3, (RW() - 0.5) * 2.4, 0], PLANK);
  py += w + 0.04;
});
cube('LanternRope', G.portal, [2.65, -2.95, 3.63], [0.07, 0.07, 0.4], [0, 0, 0], ROPE);

const Y0 = -2.45, Y1 = 3.4, NSEG = 5;
const tw = y => 1.95 * (1 - 0.15 * (y - Y0) / (Y1 - Y0));
const th = y => 3.3 * (1 - 0.06 * (y - Y0) / (Y1 - Y0));
for (let k = 0; k < NSEG; k++) {
  const a = Y0 + (Y1 - Y0) * k / NSEG, b = Y0 + (Y1 - Y0) * (k + 1) / NSEG, m = (a + b) / 2, w = tw(m), h = th(m), L = b - a;
  const cell = { side: [k, 2] };
  [-1, 1].forEach(s => cube(`Wall${k}${s > 0 ? 'R' : 'L'}`, G.tunnel, [s * (w + 0.125), m, h / 2], [0.25, L, h + 0.02], [0, 0, 0], cell));
  cube(`Ceiling${k}`, G.tunnel, [0, m, h + 0.135], [2 * w + 0.52, L, 0.25], [0, 0, 0], cell);
  cube(`Floor${k}`, G.tunnel, [0, m, 0.01], [2 * w + 0.02, L, 0.06], [0, 0, 0], cell);
}
[0, 2].forEach((fy, k) => {
  const px = tw(fy) - 0.17, top = th(fy) - 0.28, cell = { side: [5 + k, 1], up: [7, 1], down: [7, 1] };
  [-1, 1].forEach((s, i) => { const hh = top + 0.05 + 0.02 * i; cube(`InnerPost${k}${i}`, G.tunnel, [s * px, fy, hh / 2 - 0.05], [0.4, 0.4, hh], [0, 0, 0], cell); });
  cube(`InnerCap${k}`, G.tunnel, [0, fy, top - 0.1], [2 * px + 0.5, 0.42, 0.34], [0, 0, 0], cell);
});
const vw = tw(Y1) + 0.1, vh = th(Y1) + 0.1;
cube('void', G.tunnel, [0, Y1 - 0.08, vh / 2 - 0.02], [2 * vw, 0.1, vh], [0, 0, 0], { side: [7, 1] });

const BOULDERS = [
  [[0.6, 6.4, 1.6], [8.8, 5.4, 5.6], 30], [[1.0, 5.6, 4.9], [6.0, 4.4, 3.0], 29],
  [[-3.75, -0.8, 1.8], [3.0, 4.6, 3.8], 59, 10], [[4.1, -1.3, 1.3], [3.8, 3.8, 2.8], 52, -8],
  [[3.95, 0.2, 2.2], [2.8, 2.8, 2.0], 55, -14], [[3.4, 1.4, 4.6], [3.2, 3.2, 2.6], 53],
  [[0.1, 0.9, 4.9], [4.6, 3.0, 2.4], 33, 3],
  [[3.6, 2.8, 2.0], [3.8, 3.4, 4.0], 34], [[4.0, 5.0, 2.6], [3.4, 3.0, 4.4], 56],
  [[1.6, 4.6, 5.5], [3.6, 3.4, 3.4], 35], [[3.4, 6.0, 6.1], [3.6, 3.4, 3.4], 61],
  [[4.4, 7.4, 1.4], [3.4, 3.4, 3.6], 36], [[1.0, 3.0, 5.4], [3.6, 3.4, 3.0], 37],
  [[-0.3, 6.6, 5.3], [3.6, 3.4, 3.2], 42],
  [[-2.8, 2.8, 2.6], [3.8, 4.2, 4.6], 60], [[-1.7, 5.0, 3.8], [4.4, 4.2, 3.2], 39],
  [[-3.6, 6.6, 1.6], [3.6, 4.0, 3.2], 40], [[-0.4, 8.4, 1.8], [4.4, 2.8, 3.6], 41],
  [[4.6, 1.8, 1.0], [2.6, 3.0, 2.4], 43], [[4.9, -2.7, 0.7], [2.4, 2.2, 1.8], 44],
  [[-4.8, 3.4, 1.0], [2.2, 2.6, 2.0], 45], [[4.8, 6.6, 0.9], [2.4, 2.6, 1.9], 46],
  [[-3.0, -2.9, 0.45], [1.5, 1.3, 1.1], 47], [[-2.9, -1.2, 1.6], [2.0, 3.0, 3.4], 62, 4], [[2.9, -1.0, 2.3], [1.8, 2.6, 3.0], 63, -4], [[-4.3, 8.2, 0.6], [2.0, 2.0, 1.2], 48],
];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const newell = ps => { const n = [0, 0, 0]; ps.forEach((p, i) => { const q = ps[(i + 1) % ps.length]; n[0] += (p[1] - q[1]) * (p[2] + q[2]); n[1] += (p[2] - q[2]) * (p[0] + q[0]); n[2] += (p[0] - q[0]) * (p[1] + q[1]); }); const l = Math.hypot(...n) || 1; return n.map(v => v / l); };
const KEEP = [[[-2.0, -3.6, -0.5], [2.0, 3.5, 3.35]], [[-3.3, -3.6, 3.72], [3.3, -0.75, 4.5]]];
const samples = KEEP.map(([lo, hi]) => { const out = []; for (let i = 0; i <= 10; i++) for (let j = 0; j <= 14; j++) for (let k = 0; k <= 8; k++) out.push([lo[0] + (hi[0] - lo[0]) * i / 10, lo[1] + (hi[1] - lo[1]) * j / 14, lo[2] + (hi[2] - lo[2]) * k / 8]); return out; });
const shifts = {};
BOULDERS.forEach(([c, s, seed, yawSet]) => {
  const r = mulberry(seed * 977);
  const a = s[0] * 0.5, b = s[1] * 0.5, cc = s[2] * 0.5, N = 3;
  const V = [], K = {}, F = [];
  const vid = p => { const key = p.map(v => Math.round(v * 1000)).join(); if (!(key in K)) { K[key] = V.length; V.push(p); } return K[key]; };
  for (const [i0, i1, i2] of [[0, 1, 2], [1, 2, 0], [2, 0, 1]]) for (const sg of [-1, 1]) for (let u = 0; u < N; u++) for (let v = 0; v < N; v++) {
    F.push([[u, v], [u + 1, v], [u + 1, v + 1], [u, v + 1]].map(([uu, vv]) => { const q = [0, 0, 0]; q[i0] = sg; q[i1] = -1 + 2 * uu / N; q[i2] = -1 + 2 * vv / N; return vid(q); }));
  }
  const cuts = [[[(r() - 0.5) * 0.35, (r() - 0.5) * 0.35, 1], cc * (0.62 + r() * 0.2)], [[0, 0, -1], cc * 0.85]];
  for (let n = 1 + Math.floor(r() * 2.5); n > 0; n--) {
    const th = r() * 6.283, nn = [Math.cos(th), Math.sin(th), (r() - 0.3) * 0.5], ext = Math.hypot(a * nn[0], b * nn[1]);
    cuts.push([nn, ext * (0.72 + r() * 0.16)]);
  }
  cuts.forEach(cu => { const l = Math.hypot(...cu[0]); cu[0] = cu[0].map(v => v / l); });
  const taper = 0.08 + r() * 0.16, kx = (r() - 0.5) * 0.24, ky = (r() - 0.5) * 0.24;
  const yaw = (yawSet !== undefined ? yawSet : (r() - 0.5) * 50) * Math.PI / 180, tx = (r() - 0.5) * 10 * Math.PI / 180, ty = (r() - 0.5) * 10 * Math.PI / 180;
  const W0 = V.map(q => {
    const nrm = Math.pow(q.reduce((m, v) => m + v ** 4, 0), 0.25), jr = 1 + (r() - 0.5) * 0.14;
    let p = [q[0] / nrm * a * jr, q[1] / nrm * b * jr, q[2] / nrm * cc * jr];
    cuts.forEach(([n, d]) => { const e = dot(n, p) - d; if (e > 0) p = p.map((v, i) => v - e * n[i]); });
    let [x, y, z] = p;
    const t = (z + cc) / (2 * cc), f = 1 - taper * t;
    x *= f; y *= f; z += (kx * x + ky * y) * t;
    let y2 = y * Math.cos(tx) - z * Math.sin(tx), z2 = y * Math.sin(tx) + z * Math.cos(tx); y = y2; z = z2;
    let x2 = x * Math.cos(ty) + z * Math.sin(ty); z2 = -x * Math.sin(ty) + z * Math.cos(ty); x = x2; z = z2;
    x2 = x * Math.cos(yaw) - y * Math.sin(yaw); y2 = x * Math.sin(yaw) + y * Math.cos(yaw);
    return [x2, y2, z];
  });
  let off = [...c];
  const planes = () => F.map(f => { const ps = f.map(i => W0[i].map((v, q) => v + off[q])); return [newell(ps), ps.reduce((m, p) => m.map((v, i) => v + p[i] / ps.length), [0, 0, 0])]; });
  const c0 = W0.reduce((m, p) => m.map((v, i) => v + p[i] / W0.length), [0, 0, 0]);
  const hits = () => { const cin = c0.map((v, q) => v + off[q]); const pl = planes().map(([n, fc]) => dot(n, sub(fc, cin)) < 0 ? [n.map(v => -v), fc] : [n, fc]); return samples.map(ss => ss.some(p => pl.every(([n, fc]) => dot(n, sub(p, fc)) < 0))); };
  const clear = () => { const h = hits(); return !h[0] && !h[1]; };
  if (!clear()) {
    let best = null;
    for (const d of [[Math.sign(c[0]) || 1, 0, 0], [0, 1, 0], [0, 0, 1]]) {
      for (let it = 1; it <= 80; it++) { off = c.map((v, q) => v + d[q] * 0.08 * it); if (clear()) { if (!best || it < best[0]) best = [it, off]; break; } }
    }
    off = best ? best[1] : [...c];
  }
  if (off.some((v, q) => v !== c[q])) shifts[seed] = off.map((v, q) => +(v - c[q]).toFixed(2));
  const W = W0.map(p => p.map((v, q) => v + off[q]));
  const P = W.map(BB), cen = P.reduce((m, p) => m.map((v, i) => v + p[i] / P.length), [0, 0, 0]);
  const hmin = Math.min(...P.map(p => p[1])), hmax = Math.max(...P.map(p => p[1])), span = Math.max(a, b) * 20;
  const variant = seed % 4;
  const mesh = new Mesh({ name: `Rock${seed}`, color: variant, vertices: {} });
  const keys = mesh.addVertices(...P);
  F.forEach(f => {
    let ps = f.map(i => P[i]);
    const fc = ps.reduce((m, p) => m.map((v, i) => v + p[i] / ps.length), [0, 0, 0]);
    let n = newell(ps);
    if (dot(n, sub(fc, cen)) < 0) { f = f.slice().reverse(); ps = ps.slice().reverse(); n = n.map(v => -v); }
    let cell, uv;
    if (n[1] > 0.55) {
      cell = [variant + 4, 0];
      uv = ps.map(p => [(p[0] - cen[0]) / span + 0.5, (p[2] - cen[2]) / span + 0.5]);
    } else if (n[1] < -0.35) {
      cell = [0, 1]; uv = ps.map(() => [0.5, 0.5]);
    } else {
      cell = [variant, 0];
      const tg = [-n[2], 0, n[0]], tl = Math.hypot(tg[0], tg[2]) || 1;
      uv = ps.map(p => [dot(sub(p, cen), tg) / tl / span + 0.5, 1 - (p[1] - hmin) / (hmax - hmin)]);
    }
    const uvo = {};
    f.forEach((vi, i) => { uvo[keys[vi]] = [cell[0] * C + 3 + Math.min(1, Math.max(0, uv[i][0])) * (C - 6), cell[1] * C + 3 + Math.min(1, Math.max(0, uv[i][1])) * (C - 6)]; });
    mesh.addFaces(new MeshFace(mesh, { vertices: f.map(vi => keys[vi]), uv: uvo, texture: tex.uuid }));
  });
  mesh.addTo(G.rocks).init(); made.push(mesh);
});
Undo.finishEdit('Build mine entrance', { outliner: true, elements: made, textures: [tex] });
Canvas.updateAll();
return { elements: made.length, textures: Texture.all.length, uv: [tex.uv_width, tex.uv_height], shifts };
})()
