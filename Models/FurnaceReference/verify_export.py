"""Round-trip FBX and GLB exports; verify geometry, UVs, texture links and bounds."""
import bpy
import os
import json
import math
from mathutils import Vector

folder=os.path.dirname(os.path.abspath(__file__))
expected=json.load(open(os.path.join(folder,'mesh-report.json')))
reports={}
for ext in ['fbx','glb']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path=os.path.join(folder,'Furnace_Reference.'+ext)
    if ext=='fbx':bpy.ops.import_scene.fbx(filepath=path)
    else:bpy.ops.import_scene.gltf(filepath=path)
    bpy.context.view_layer.update()
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    assert len(meshes)==6,(ext,len(meshes))
    tris=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
    assert tris==expected['total_triangles'],(ext,tris)
    for o in meshes:
        assert len(o.data.uv_layers)==1,(ext,o.name,len(o.data.uv_layers))
        assert all(0<=v<=1 for l in o.data.uv_layers[0].data for v in l.uv)
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert o.data.materials
        for mat in o.data.materials:
            assert any(n.type=='TEX_IMAGE' and n.image and n.image.size[0]==1024 for n in mat.node_tree.nodes),(ext,o.name,mat.name)
    coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    bounds={a:[min(v[k] for v in coords),max(v[k] for v in coords)] for k,a in enumerate('xyz')}
    for a in 'xyz':
        assert max(abs(bounds[a][i]-expected['bounds'][a][i]) for i in [0,1])<.002,(ext,a,bounds[a],expected['bounds'][a])
    reports[ext]={'status':'PASS','mesh_count':len(meshes),'triangles':tris,'bounds':bounds,'single_uv_set_per_mesh':True,'texture_links_present':True}
with open(os.path.join(folder,'export-verification.json'),'w') as f:json.dump(reports,f,indent=2)
print('EXPORT_VERIFICATION',json.dumps(reports))
