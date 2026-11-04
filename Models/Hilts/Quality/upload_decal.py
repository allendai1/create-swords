import json, os, sys, time, requests
KEY = os.environ["ROBLOX_API_KEY"]
path = sys.argv[1]
req = {"assetType": "Decal", "displayName": "Hilt reference strip", "description": "Sell Swords! review reference (private)",
       "creationContext": {"creator": {"userId": "14722022"}}}
with open(path, "rb") as f:
    r = requests.post("https://apis.roblox.com/assets/v1/assets", headers={"x-api-key": KEY},
                      files={"request": (None, json.dumps(req), "application/json"), "fileContent": (os.path.basename(path), f, "image/png")}, timeout=120)
r.raise_for_status()
op = r.json(); name = op.get("path") or ("operations/" + op["operationId"])
for _ in range(60):
    if op.get("done"): break
    time.sleep(2)
    op = requests.get("https://apis.roblox.com/assets/v1/" + name, headers={"x-api-key": KEY}, timeout=60).json()
print(json.dumps(op.get("response", op))[:400])
