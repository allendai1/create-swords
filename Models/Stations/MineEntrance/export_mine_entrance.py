# Export the mine entrance and its 6-stop track for Studio (Allen 2026-10-20: "Upload the mine entrance and the
# 6-stop track, swap them in for the mine shaft").
# Run headless after build_mine_entrance.py:  blender --background MineEntrance.blend --python export_mine_entrance.py
# Each model is joined into one mesh per colour, named after its palette key (Studio colours MeshParts by name).
# The lever and carts are already in Studio (from the mine shaft) and are reused. Writes Mine_Entrance.fbx,
# Mine_Track6.fbx and parts.json (each part's world bounding-box centre, Blender axes).
import json
import os
import sys
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_stations as bs  # noqa: E402


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
for cname in ("MineEntrance", "Track"):
    groups = {}
    for o in [o for o in bpy.data.collections[cname].objects if o.type == "MESH"]:
        groups.setdefault(o.data.materials[0].name.removeprefix("LP_"), []).append(o)
    parts[cname] = {key: centre(join(objs, key)) for key, objs in groups.items()}

bs.export_fbx(HERE, names=("MineEntrance", "Track"))
os.replace(os.path.join(HERE, "MineEntrance.fbx"), os.path.join(HERE, "Mine_Entrance.fbx"))
os.replace(os.path.join(HERE, "Track.fbx"), os.path.join(HERE, "Mine_Track6.fbx"))
json.dump(parts, open(os.path.join(HERE, "parts.json"), "w"), indent=1)
print("EXPORTED", {k: sorted(v) for k, v in parts.items()})
