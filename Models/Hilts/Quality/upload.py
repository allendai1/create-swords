# python -I upload.py <Kind> [<Kind> ...] : upload Models/Hilts/Quality/<Kind>HiltGame.fbx through Open Cloud
# (Assets API, assetType Model, creator user 14722022, header x-api-key from ROBLOX_API_KEY) and print {kind: assetId}.
import json
import os
import sys
import time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ["ROBLOX_API_KEY"]
URL = "https://apis.roblox.com/assets/v1/assets"


def upload(kind):
    path = os.path.join(HERE, kind + "HiltGame.fbx")
    req = {"assetType": "Model", "displayName": kind + "Hilt (quality pass)",
           "description": "Sell Swords! hilt, quality pass 2026-10-29",
           "creationContext": {"creator": {"userId": "14722022"}}}
    with open(path, "rb") as f:
        r = requests.post(URL, headers={"x-api-key": KEY},
                          files={"request": (None, json.dumps(req), "application/json"),
                                 "fileContent": (os.path.basename(path), f, "model/fbx")}, timeout=120)
    r.raise_for_status()
    op = r.json()
    name = op.get("path") or ("operations/" + op["operationId"])
    for _ in range(60):
        if op.get("done"):
            break
        time.sleep(2)
        op = requests.get("https://apis.roblox.com/assets/v1/" + name, headers={"x-api-key": KEY}, timeout=60).json()
    if not op.get("done") or "response" not in op:
        return {"error": json.dumps(op)[:300]}
    return op["response"]["assetId"]


if __name__ == "__main__":
    print(json.dumps({k: upload(k) for k in sys.argv[1:]}))
