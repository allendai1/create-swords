# Export the mine shaft for Studio (Allen 2026-10-20: "Export and upload the mine shaft, lever, track and carts").
# Run headless after build_mine_shaft.py:  blender --background MineShaft.blend --python export_mine_shaft.py
# Each model is joined into one mesh per colour, named after its palette key (FBX colours don't import, so Studio
# colours each MeshPart by name). The lever keeps Arm and Knob apart so they can swing. One cart is exported and
# cloned in Studio. Writes Mine_<model>.fbx and parts.json (each part's world bounding-box centre, Blender axes).
import json
import os
import sys
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # noqa: E402

KEEP = {"Lever": {"Arm", "Knob"}}  # parts left unjoined, by object name


def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    o.name = o.data.name = name
    return o


def centre(o):
    vs = [o.matrix_world @ v.co for v in o.data.vertices]
    return [(min(v[k] for v in vs) + max(v[k] for v in vs)) / 2 for k in range(3)]


parts = {}
for cname in ("MineShaft", "Lever", "Track", "Cart1"):
    coll = bpy.data.collections[cname]
    groups = {}
    for o in [o for o in coll.objects if o.type == "MESH"]:
        key = o.name if o.name in KEEP.get(cname, ()) else o.data.materials[0].name.removeprefix("LP_")
        groups.setdefault(key, []).append(o)
    parts[cname] = {}
    for key, objs in groups.items():
        o = join(objs, key)
        parts[cname][key] = centre(o)
    root = next(o for o in coll.objects if o.type == "EMPTY")
    parts[cname]["_root"] = list(root.location)

for c in ("Cart2", "Cart3", "OrePreview"):
    bpy.data.collections[c].hide_render = True
res = bs.export_fbx(HERE, names=("MineShaft", "Lever", "Track", "Cart1"))
for n in ("MineShaft", "Lever", "Track", "Cart1"):
    os.replace(os.path.join(HERE, n + ".fbx"), os.path.join(HERE, f"Mine_{n}.fbx"))
json.dump(parts, open(os.path.join(HERE, "parts.json"), "w"), indent=1)
print("EXPORTED", {k: sorted(v) for k, v in parts.items()})
