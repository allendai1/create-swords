"""Upload files to Roblox through Open Cloud (Assets API) as the group that owns the game, and print {name: assetId}.
python -I Development/upload_asset.py <file> [<file> ...]      (needs ROBLOX_API_KEY)
  .fbx / .glb -> Model, .png / .jpg -> Decal (a Decal's Image id is under it: InsertService:LoadAsset in Studio),
  .mp3 / .ogg -> Audio (starts in moderation "Reviewing" for a few minutes).
  name = the file name without its extension. Each id is printed to stderr as soon as it is ready, so a later failure
  doesn't lose the earlier ones; a failed file maps to {"error": ...} and the exit code is 1.
Creator: group 336242048 (Swordsmith Tycoon's group, since 2026-11-09): a group place can't load a user's uploads.
Sounds go here too: a user-owned sound failed live even with a universe grant (2026-11-11, "Requester does not
have permission"). Animations (.rbxm) aren't covered yet."""
import json
import os
import sys
import time
import urllib.request
import uuid

API = "https://apis.roblox.com/assets/v1/"
CREATOR = {"groupId": "336242048"}
TYPES = {".fbx": ("Model", "model/fbx"), ".glb": ("Model", "model/gltf-binary"),
         ".png": ("Decal", "image/png"), ".jpg": ("Decal", "image/jpeg"), ".jpeg": ("Decal", "image/jpeg"),
         ".mp3": ("Audio", "audio/mpeg"), ".ogg": ("Audio", "audio/ogg")}


def call(req):
    req.add_header("x-api-key", os.environ["ROBLOX_API_KEY"])
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def upload(path):
    """One file -> its asset id (raises on any failure)."""
    name, ext = os.path.splitext(os.path.basename(path))
    asset_type, mime = TYPES[ext.lower()]
    meta = {"assetType": asset_type, "displayName": name, "description": "Sell Swords! " + asset_type.lower(),
            "creationContext": {"creator": CREATOR}}
    bd = uuid.uuid4().hex
    with open(path, "rb") as f:
        data = f.read()
    body = (f'--{bd}\r\nContent-Disposition: form-data; name="request"\r\n\r\n{json.dumps(meta)}\r\n'
            f'--{bd}\r\nContent-Disposition: form-data; name="fileContent"; filename="{name}{ext}"\r\n'
            f'Content-Type: {mime}\r\n\r\n').encode() + data + f"\r\n--{bd}--\r\n".encode()
    req = urllib.request.Request(API + "assets", data=body, method="POST")
    req.add_header("Content-Type", "multipart/form-data; boundary=" + bd)
    op = call(req)
    where = op.get("path") or ("operations/" + op["operationId"])
    for _ in range(60):
        if op.get("done"):
            return op["response"]["assetId"]
        time.sleep(2)
        op = call(urllib.request.Request(API + where))
    raise TimeoutError(json.dumps(op)[:300])


if __name__ == "__main__":
    if "ROBLOX_API_KEY" not in os.environ or len(sys.argv) < 2:
        sys.exit(__doc__)
    out, failed = {}, False
    for p in sys.argv[1:]:
        key = os.path.splitext(os.path.basename(p))[0]
        try:
            out[key] = upload(p)
        except Exception as e:  # keep going: the other files' ids still print
            out[key], failed = {"error": f"{type(e).__name__}: {e}"}, True
        print(key, out[key], file=sys.stderr, flush=True)
    print(json.dumps(out))
    sys.exit(1 if failed else 0)
