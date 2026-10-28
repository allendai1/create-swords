# notice_board.py: prepares FreeStylized's Notice Board 01 (https://freestylized.com/3d_models/notice_board_01_m18/,
# "Royalty Free License: Free to use for all Commercial and Non-Commercial purposes") for Roblox (2026-10-25). Allen:
# "Can we add this notice board ... to replace the delivery board we currently have."
# Applies the FBX's transforms, puts the origin at the bottom centre, exports a GLB, and shrinks the 2K maps to 1024
# (Roblox's limit; OpenGL normal map, Roblox's convention).
# Run: blender -b --factory-startup --python notice_board.py -- <unzipped NoticeBoard_01_M18 dir> <out dir>
import os, sys
import bpy
from mathutils import Vector

src, out = sys.argv[-2:]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=os.path.join(src, "Source", "notice_board_01_m18.fbx"))
ob = next(o for o in bpy.data.objects if o.type == "MESH")
bpy.context.view_layer.objects.active = ob
ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
lo = Vector([min(v.co[i] for v in ob.data.vertices) for i in range(3)])
hi = Vector([max(v.co[i] for v in ob.data.vertices) for i in range(3)])
shift = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
for v in ob.data.vertices:
    v.co -= shift
print("size (m)", tuple(round(c, 3) for c in hi - lo))
bpy.ops.export_scene.gltf(filepath=os.path.join(out, "NoticeBoard.glb"), export_format="GLB", use_selection=True,
                          export_materials="NONE")

for name, kind in (("Base_color", "color"), ("Normal_GL", "normal"), ("Roughness", "rough")):
    img = bpy.data.images.load(os.path.join(src, "Textures", f"notice_board_01_m18_{name}.png"))
    img.scale(1024, 1024)
    img.filepath_raw = os.path.join(out, f"NoticeBoard_{kind}.png")
    img.file_format = "PNG"
    img.save()
