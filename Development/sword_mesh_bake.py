# Local helper for ServerStorage.Builders.bake_sword_meshes (vault: Development/Sword Mesh Pipeline).
# Run: python -I sword_mesh_bake.py   (needs ROBLOX_API_KEY; listens on 127.0.0.1:34999)
#   POST /bake/<name>  body = Studio mesh dump -> glb -> Open Cloud upload; replies {"operationId": ...}
#   GET  /op/<id>      -> {"assetId": ...} | {"pending": true} | {"error": ...}
# Dump format: u32 face count, then per face corner: pos f32x3, rgb u8x3, uv f32x2, normal f32x3.
import http.server, json, os, struct, sys, tempfile, urllib.error, urllib.parse, urllib.request, uuid

API = "https://apis.roblox.com/assets/v1/"
CREATOR = "14722022"
OUT = os.path.join(tempfile.gettempdir(), "sword_mesh_bake")


def to_glb(raw):
    (nf,) = struct.unpack_from("<I", raw, 0)
    corners, o = [], 4
    for _ in range(nf * 3):
        x, y, z = struct.unpack_from("<fff", raw, o); rgb = tuple(raw[o + 12:o + 15])
        u, v = struct.unpack_from("<ff", raw, o + 15); n = struct.unpack_from("<fff", raw, o + 23); o += 35
        # Roblox's glTF import turns the mesh 180 degrees about Y: negate x and z to cancel it
        corners.append(((-x, y, -z), rgb, (u, v), (-n[0], n[1], -n[2])))
    assert o == len(raw), "bad dump"
    # Uploads are re-centred on their bounds, while a live EditableMesh part keeps its origin: a degenerate
    # triangle mirroring the bounds makes them symmetric about the origin, so the baked part sits where the live one did.
    mn = [min(c[0][i] for c in corners) for i in range(3)]
    mx = [max(c[0][i] for c in corners) for i in range(3)]
    a, b = tuple(-v for v in mn), tuple(-v for v in mx)
    corners += [(a, (0, 0, 0), (0, 0), (0, 1, 0)), (b, (0, 0, 0), (0, 0), (0, 1, 0)), (b, (0, 0, 0), (0, 0), (0, 1, 0))]
    lo = [min(mn[i], -mx[i]) for i in range(3)]
    P = b"".join(struct.pack("<fff", *c[0]) for c in corners)
    C = b"".join(struct.pack("<fff", *(k / 255 for k in c[1])) for c in corners)
    U = b"".join(struct.pack("<ff", *c[2]) for c in corners)
    N = b"".join(struct.pack("<fff", *c[3]) for c in corners)
    views, off = [], 0
    for blob in (P, C, U, N):
        views.append({"buffer": 0, "byteOffset": off, "byteLength": len(blob), "target": 34962}); off += len(blob)
    n = len(corners)
    gltf = {
        "asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": "SwordMesh"}],
        "meshes": [{"name": "SwordMesh", "primitives": [{"attributes": {"POSITION": 0, "COLOR_0": 1, "TEXCOORD_0": 2, "NORMAL": 3}}]}],
        "buffers": [{"byteLength": off}], "bufferViews": views,
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": n, "type": "VEC3", "min": lo, "max": [-v for v in lo]},
            {"bufferView": 1, "componentType": 5126, "count": n, "type": "VEC3"},
            {"bufferView": 2, "componentType": 5126, "count": n, "type": "VEC2"},
            {"bufferView": 3, "componentType": 5126, "count": n, "type": "VEC3"},
        ],
    }
    js = json.dumps(gltf).encode(); js += b" " * (-len(js) % 4)
    body = P + C + U + N
    return (struct.pack("<III", 0x46546C67, 2, 28 + len(js) + len(body))
            + struct.pack("<II", len(js), 0x4E4F534A) + js + struct.pack("<II", len(body), 0x004E4942) + body)


def call(req):
    req.add_header("x-api-key", os.environ["ROBLOX_API_KEY"])
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def upload(name, glb):
    meta = {"assetType": "Model", "displayName": "SwordMesh " + name, "description": "Create Swords! baked sword mesh",
            "creationContext": {"creator": {"userId": CREATOR}}}
    bd = uuid.uuid4().hex
    body = (f'--{bd}\r\nContent-Disposition: form-data; name="request"\r\n\r\n{json.dumps(meta)}\r\n'
            f'--{bd}\r\nContent-Disposition: form-data; name="fileContent"; filename="mesh.glb"\r\n'
            f'Content-Type: model/gltf-binary\r\n\r\n').encode() + glb + f"\r\n--{bd}--\r\n".encode()
    req = urllib.request.Request(API + "assets", data=body, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=" + bd)
    return call(req)["operationId"]


class Handler(http.server.BaseHTTPRequestHandler):
    def reply(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(data)

    def do_POST(self):
        name = urllib.parse.unquote(self.path[len("/bake/"):])
        try:
            raw = self.rfile.read(int(self.headers["Content-Length"]))
            glb = to_glb(raw)
            safe = "".join(ch if ch.isalnum() else "_" for ch in name)
            open(os.path.join(OUT, safe + ".glb"), "wb").write(glb)
            self.reply({"operationId": upload(name, glb)})
        except Exception as e:  # report to Studio instead of dropping the connection
            self.reply({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_GET(self):
        try:
            d = call(urllib.request.Request(API + "operations/" + self.path[len("/op/"):]))
            if not d.get("done"):
                return self.reply({"pending": True})
            r = d.get("response") or {}
            state = (r.get("moderationResult") or {}).get("moderationState")
            self.reply({"assetId": r["assetId"], "moderation": state} if "assetId" in r else {"error": json.dumps(d)[:300]})
        except Exception as e:
            self.reply({"error": f"{type(e).__name__}: {e}"}, 500)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    if "ROBLOX_API_KEY" not in os.environ:
        sys.exit("ROBLOX_API_KEY is not set")
    os.makedirs(OUT, exist_ok=True)
    print("sword_mesh_bake listening on 127.0.0.1:34999, glbs in", OUT, flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", 34999), Handler).serve_forever()
