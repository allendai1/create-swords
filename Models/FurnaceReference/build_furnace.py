"""Build the user's furnace.png reference as a standalone, textured game prop.
Run: blender --background --python build_furnace.py
Front: -Y; bottom-centred origin; nominal dimensions in project modelling units.
"""
import bpy
import bmesh
import math
import random
import os
import json
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(3719)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.materials):
    bpy.data.materials.remove(block)

def lin(v):
    return ((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92

# A portable colour atlas: broad triangulated mottling plus fine mineral variation.
# Every face is explicitly mapped into a tile; no procedural nodes are needed at import.
palette = [
    (105, 100, 96), (134, 125, 115), (57, 51, 48), (92, 80, 69),
    (131, 117, 101), (24, 20, 18), (66, 52, 43), (40, 29, 23),
    (255, 76, 3), (255, 132, 4), (255, 192, 16), (255, 228, 73),
    (109, 97, 86), (77, 68, 61), (32, 27, 24), (191, 74, 9),
]
size = 1024
tile = size // 4
image = bpy.data.images.new('Furnace_Color', width=size, height=size, alpha=False)
pixels = [0.0] * (size * size * 4)
noise_rng = random.Random(820)
cells = 16
for tid,base in enumerate(palette):
    tx,ty=(tid%4)*tile,(tid//4)*tile
    points={}
    for j in range(cells+1):
        for i in range(cells+1):
            # Jitter shared vertices to break up a regular checkerboard pattern.
            points[i,j]=(i*tile/cells+(noise_rng.uniform(-.34,.34)*tile/cells if 0<i<cells else 0),j*tile/cells+(noise_rng.uniform(-.34,.34)*tile/cells if 0<j<cells else 0))
    for j in range(cells):
        for i in range(cells):
            a,b,c,d=[points[p] for p in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]]
            triangles=[(a,b,c),(a,c,d)] if noise_rng.random()<.5 else [(a,b,d),(b,c,d)]
            for tri in triangles:
                variation=noise_rng.uniform(-1,1)*(9 if tid in (0,1,12) else 3.5)
                (ax,ay),(bx,by),(cx,cy)=tri
                denominator=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
                for py in range(max(0,int(min(ay,by,cy))),min(tile,int(max(ay,by,cy))+1)):
                    for px in range(max(0,int(min(ax,bx,cx))),min(tile,int(max(ax,bx,cx))+1)):
                        u=((by-cy)*(px+.5-cx)+(cx-bx)*(py+.5-cy))/denominator
                        v=((cy-ay)*(px+.5-cx)+(ax-cx)*(py+.5-cy))/denominator
                        if u>=-.00001 and v>=-.00001 and u+v<=1.00001:
                            grain=noise_rng.uniform(-1,1)*1.2
                            rgb=[max(0,min(255,k+variation+grain))/255 for k in base]
                            pos=((ty+py)*size+tx+px)*4
                            pixels[pos:pos+4]=rgb+[1]
image.pixels.foreach_set(pixels)
image.filepath_raw = os.path.join(HERE, 'Furnace_Color.png')
image.file_format = 'PNG'
image.save()

def material(name, emission=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    bsdf = nodes.get('Principled BSDF')
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = image
    m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = .82
    if emission:
        m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = .9
    return m

surface = material('Furnace_Atlas')
emission = material('Furnace_Embers', True)
groups = {}

def finish(obj, group, tile_id, bevel=0, edge_tile=None):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new('Small forged edge chamfer', 'BEVEL')
        mod.width = bevel
        mod.segments = 1
        mod.affect = 'EDGES'
        bpy.ops.object.modifier_apply(modifier=mod.name)
    mesh = obj.data
    mesh.materials.append(emission if group == 'Embers' else surface)
    # Blender primitives already have a default UV set. Remove it so both
    # renderers and importers use the atlas UVs instead of the primitive layout.
    for old_uv in list(mesh.uv_layers):
        mesh.uv_layers.remove(old_uv)
    uv = mesh.uv_layers.new(name='UVMap')
    uv.active_render = True
    for face in mesh.polygons:
        n = face.normal
        dominant = max(abs(n.x), abs(n.y), abs(n.z))
        tid = edge_tile if edge_tile is not None and dominant < .99 else tile_id
        axes = sorted(range(3), key=lambda k: abs(n[k]))[:2]
        coords = [(mesh.vertices[mesh.loops[i].vertex_index].co[axes[0]], mesh.vertices[mesh.loops[i].vertex_index].co[axes[1]]) for i in face.loop_indices]
        lo = [min(p[k] for p in coords) for k in range(2)]
        span = [max(p[k] for p in coords)-lo[k] for k in range(2)]
        ou, ov = random.uniform(.035, .1), random.uniform(.035, .1)
        for i, p in zip(face.loop_indices, coords):
            # Same density on both axes, avoiding stretched grain on narrow beams.
            density = max(max(span), .0001)
            u = ou + (p[0]-lo[0]) / density * .81
            v = ov + (p[1]-lo[1]) / density * .81
            uv.data[i].uv = (((tid % 4)+u)/4, ((tid // 4)+v)/4)
        face.use_smooth = False
    groups.setdefault(group, []).append(obj)
    obj.select_set(False)
    return obj

def box(name, loc, dims, group='Stone', color=0, bevel=.045, edge=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    return finish(obj, group, color, bevel, edge)

def poly_prism(name, points, y_front, y_back, group='Stone', color=0, bevel=.025):
    # points in X/Z plane, ordered counterclockwise as seen from front.
    count = len(points)
    verts = [(x,y_front,z) for x,z in points] + [(x,y_back,z) for x,z in points]
    faces = [tuple(reversed(range(count))), tuple(range(count,2*count))]
    faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    # Recalculate to guarantee outward winding regardless of polygon ordering.
    bm = bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh); bm.free()
    return finish(obj, group, color, bevel, 1 if group=='Stone' else 3)

def stud(name, center, normal):
    n = Vector(normal)
    side = Vector((1,0,0)) if abs(n.x) < .8 else Vector((0,1,0))
    up = n.cross(side).normalized()
    c = Vector(center)
    r = .17
    verts = [c+side*a*r+up*b*r for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    verts.append(c+n*.125)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],[(3,2,1,0),(0,1,4),(1,2,4),(2,3,4),(3,0,4)])
    mesh.update()
    ob = bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(ob)
    return finish(ob,'Rivets',4,.008,1)

# Main body. All openings are actual geometry gaps with dark interior surfaces.
box('Stone hearth slab',(0,0,.58),(5.9,4.9,1.0),bevel=.13,edge=1)
box('Back masonry',(0,2.13,3.7),(5.65,.58,5.05),bevel=.12,edge=1)
box('Left masonry',(-2.55,0,3.6),(.65,4.3,4.95),bevel=.12,edge=1)
# Right-hand wall is split around the side air vent.
box('Right front jamb',(2.55,-1.65,3.62),(.65,1.05,4.95),bevel=.10,edge=1)
box('Right rear jamb',(2.55,1.60,3.62),(.65,1.15,4.95),bevel=.10,edge=1)
box('Right below vent',(2.55,-.02,1.88),(.65,2.25,1.57),bevel=.07,edge=1)
box('Right above vent',(2.55,-.02,5.27),(.65,2.25,1.57),bevel=.07,edge=1)
box('Interior floor',(0,-.05,1.14),(4.6,3.9,.18),'Interior',6,.035)
box('Interior back',(0,1.78,2.6),(4.6,.13,3.05),'Interior',5,.02)
box('Interior left',(-2.17,0,2.65),(.12,3.6,3.1),'Interior',5,.02)
box('Interior right',(2.17,0,2.65),(.12,3.6,3.1),'Interior',5,.02)
box('Fire mouth sill',(0,-2.18,1.03),(5.15,.8,.38),bevel=.065,edge=1)
# Upper shoulders form the clipped corners of the main chamber mouth.
poly_prism('Mouth left shoulder',[(-2.6,1.12),(-2.13,1.12),(-2.13,3.28),(-1.72,3.76),(-1.72,4.24),(-2.6,4.24)],-2.27,-1.61)
poly_prism('Mouth right shoulder',[(2.13,1.12),(2.6,1.12),(2.6,4.24),(1.72,4.24),(1.72,3.76),(2.13,3.28)],-2.27,-1.61)
box('Mouth lintel',(0,-1.96,4.00),(3.53,.63,.52),bevel=.065,edge=1)
box('Front separator stone',(0,-1.98,4.48),(5.15,.57,.50),bevel=.07,edge=1)
# Narrow upper slit, bounded by four solid bars and a recessed backing.
box('Upper slit darkness',(0,-1.51,5.12),(3.9,.11,.66),'Interior',5,.01)
box('Slit left stone',(-2.29,-1.99,5.17),(.65,.57,1.02),bevel=.06,edge=1)
box('Slit right stone',(2.29,-1.99,5.17),(.65,.57,1.02),bevel=.06,edge=1)
box('Slit sill',(0,-2.06,4.88),(3.95,.62,.16),'Iron',2,.025,3)
box('Slit top frame',(0,-2.08,5.52),(4.12,.58,.18),'Iron',2,.025,3)
for x in [-1.94,1.94]:
    box('Slit iron jamb',(x,-2.27,5.19),(.24,.19,.72),'Iron',2,.04,3)

# Heavy top ring surrounding a recessed three-slot grate, no chimney in this reference.
box('Top front masonry',(0,-1.90,6.04),(5.8,.78,.96),bevel=.15,edge=1)
box('Top rear masonry',(0,1.86,6.04),(5.8,.78,.96),bevel=.15,edge=1)
box('Top left masonry',(-2.49,0,6.04),(.82,3.15,.96),bevel=.15,edge=1)
box('Top right masonry',(2.49,0,6.04),(.82,3.15,.96),bevel=.15,edge=1)
box('Recessed roof cavity',(0,0,5.76),(4.13,3.12,.16),'Interior',5,.02)
for y in [-1.37,1.37]:
    box('Grate perimeter',(0,y,6.38),(4.24,.26,.20),'Iron',2,.035,3)
for x in [-2.0,2.0]:
    box('Grate perimeter',(x,0,6.38),(.26,2.52,.20),'Iron',2,.035,3)
for x in [-.65,.65]:
    box('Grate crossbar',(x,0,6.38),(.29,2.53,.20),'Iron',2,.035,3)

# Corner uprights, three massive forged collars apiece, pyramid-headed studs.
for x in [-2.87,2.87]:
    for y in [-2.12,2.12]:
        box('Corner upright',(x,y,3.39),(.53,.61,5.96),'Iron',2,.07,3)
        for z,h in [(.56,1.1),(3.16,.88),(6.08,1.12)]:
            box('Forged corner collar',(x,y,z),(.96,1.0,h),'Iron',2,.15,3)
            sign = -1 if y<0 else 1
            stud('Corner face stud',(x,y+sign*.505,z),(0,sign,0))
            sx = -1 if x<0 else 1
            stud('Corner side stud',(x+sx*.485,y,z),(sx,0,0))
box('Front bottom iron rail',(0,-2.42,.47),(4.89,.22,.70),'Iron',2,.07,3)
for x in [-1.65,0,1.65]:
    stud('Lower rail stud',(x,-2.545,.47),(0,-1,0))
for side in [-1,1]:
    for z in [.51,6.10]:
        box('Side frame rail',(side*2.91,0,z),(.22,3.65,.39),'Iron',2,.045,3)
    box('Rear frame rail',(0,2.46,3.18),(4.9,.19,.23),'Iron',2,.03,3)

# Four front grille bars match the large fire opening in the supplied image.
for i,x in enumerate([-1.42,-.47,.47,1.42]):
    box('Fire grille bar %d'%i,(x,-2.31,2.37),(.25,.29,2.39),'Grilles',2,.035,3)
# Side vent is a real aperture with a dark inner wall and shallow framed grille.
box('Side vent backing',(2.22,-.03,3.59),(.10,2.05,1.86),'Interior',5,.01)
for y in [-1.05,1.02]:
    box('Side vent jamb',(2.94,y,3.59),(.20,.18,2.02),'Grilles',2,.035,3)
for z in [2.64,4.54]:
    box('Side vent horizontal',(2.94,-.015,z),(.20,2.25,.18),'Grilles',2,.035,3)
for y in [-.51,.01,.53]:
    box('Side vent rib',(2.97,y,3.59),(.22,.15,1.75),'Grilles',2,.025,3)

# Original faceted fire meshes, removable as a group for runtime fire effects.
def flame(name, center, radius, height, tid):
    x,y,z = center
    count=7
    verts=[]
    for level,fac in [(0,1),(.42,.84),(.76,.45)]:
        for i in range(count):
            angle=i*math.tau/count
            verts.append((x+math.cos(angle)*radius*fac+level*.12,y+math.sin(angle)*radius*fac,z+height*level))
    verts.append((x+.11,y-.08,z+height))
    faces=[]
    for ring in range(2):
        for i in range(count):
            a=ring*count+i;b=ring*count+(i+1)%count;c=b+count;d=a+count
            faces += [(a,b,c),(a,c,d)]
    faces += [(14+i,14+(i+1)%count,21) for i in range(count)]
    faces.append(tuple(reversed(range(count))))
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
    finish(ob,'Embers',tid)

for i in range(13):
    x=random.uniform(-1.90,1.90);y=random.uniform(-1.35,.3)
    flame('Low poly ember tongue',(x,y,1.24),random.uniform(.25,.48),random.uniform(.6,2.0),random.choice([8,8,9,10]))
for i,x in enumerate([-1.45,-.73,0,.73,1.45]):
    flame('Yellow fire core',(x,-1.28,1.23),.35,random.uniform(.7,1.4),random.choice([10,11]))
for i in range(15):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(random.uniform(-1.85,1.85),random.uniform(-1.4,.7),1.25))
    ob=bpy.context.object;ob.name='Ember coal';ob.scale=(.29,.25,.16)
    finish(ob,'Embers',random.choice([8,9,15]))

# Join by function: six portable mesh objects rather than hundreds of loose parts.
final=[]
for group,objects in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join()
    obj=bpy.context.object;obj.name='Furnace_'+group
    bpy.context.scene.cursor.location=(0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    mod=obj.modifiers.new('Export triangulation','TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Repair tiny bevel artefacts and certify consistent normals.
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm,verts=bm.verts[:],dist=.000001)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(obj.data);bm.free()
    obj.data.update()
    final.append(obj)

root=bpy.data.objects.new('Furnace_Reference',None)
bpy.context.collection.objects.link(root)
root['reference']='References/Concept Art/furnace.png'
root['front']='-Y in Blender; base centred at origin'
root['nominal_units']='Project modelling units; verify desired dimensions in Studio import preview.'
for obj in final:obj.parent=root

# Export selected art only. Studio fire lights and particles are intentionally runtime setup.
bpy.ops.object.select_all(action='DESELECT')
for obj in final+[root]:obj.select_set(True)
bpy.context.view_layer.objects.active=final[0]
bpy.ops.export_scene.fbx(filepath=os.path.join(HERE,'Furnace_Reference.fbx'),use_selection=True,object_types={'MESH','EMPTY'},global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_mesh_modifiers=True,mesh_smooth_type='FACE',use_tspace=False,path_mode='COPY',embed_textures=True,bake_anim=False,add_leaf_bones=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE,'Furnace_Reference.glb'),export_format='GLB',use_selection=True,export_texcoords=True,export_normals=True,export_materials='EXPORT')

report={'reference':'References/Concept Art/furnace.png','meshes':[]}
for ob in final:
    bm=bmesh.new();bm.from_mesh(ob.data)
    bad=[v for v in ob.data.vertices if not all(math.isfinite(c) for c in v.co)]
    entry={'name':ob.name,'vertices':len(ob.data.vertices),'triangles':sum(len(p.vertices)-2 for p in ob.data.polygons),'uv_layers':len(ob.data.uv_layers),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'degenerate_faces':sum(f.calc_area()<1e-9 for f in bm.faces),'non_finite_vertices':len(bad)}
    bm.free();report['meshes'].append(entry)
    assert not bad and not entry['degenerate_faces'] and entry['uv_layers']==1 and not entry['non_manifold_edges'],entry
coords=[o.matrix_world@Vector(c) for o in final for c in o.bound_box]
report['bounds']={axis:[min(v[k] for v in coords),max(v[k] for v in coords)] for k,axis in enumerate('xyz')}
report['total_triangles']=sum(e['triangles'] for e in report['meshes'])
with open(os.path.join(HERE,'mesh-report.json'),'w') as f:json.dump(report,f,indent=2)
print('FURNACE_MESH_REPORT',json.dumps(report))

# Neutral studio presentation, lit from the same three-quarter angle as the reference.
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=40
scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.world.color=(.28,.28,.28)
scene.view_settings.view_transform='AgX'
floor_mat=bpy.data.materials.new('Preview ground');floor_mat.diffuse_color=(.28,.25,.23,1)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.035))
floor=bpy.context.object;floor.name='PREVIEW_Ground';floor.data.materials.append(floor_mat)
def light(name,loc,energy,color,size=4):
    data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.color=color;data.shape='DISK';data.size=size
    ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);ob.location=loc
    ob.rotation_euler=(Vector((0,0,3))-ob.location).to_track_quat('-Z','Y').to_euler()
light('PREVIEW_Key',(1,-8,12),1750,(1,.88,.76),7)
light('PREVIEW_Fill',(-7,-3,6),900,(.78,.85,1),6)
light('PREVIEW_Rim',(5,6,9),1550,(1,.87,.72),5)
data=bpy.data.lights.new('PREVIEW_EmberGlow','POINT');data.energy=100;data.color=(1,.22,.025);data.shadow_soft_size=.7
ob=bpy.data.objects.new('PREVIEW_EmberGlow',data);bpy.context.collection.objects.link(ob);ob.location=(0,-1.9,2.1)
data=bpy.data.cameras.new('PREVIEW_Camera');camera=bpy.data.objects.new('PREVIEW_Camera',data);bpy.context.collection.objects.link(camera)
camera.location=(10,-16,11)
camera.rotation_euler=(Vector((0,0,3.2))-camera.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO';data.ortho_scale=10.6;scene.camera=camera
image.pack()
bpy.context.preferences.filepaths.save_version=0
bpy.context.preferences.filepaths.file_preview_type='NONE'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE,'Furnace_Reference.blend'))
scene.render.filepath=os.path.join(HERE,'Furnace_Preview.png')
bpy.ops.render.render(write_still=True)
camera.location=(-10,14,10)
camera.rotation_euler=(Vector((0,0,3.1))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=850;scene.render.resolution_y=850
scene.render.filepath=os.path.join(HERE,'Furnace_Rear_Preview.png')
bpy.ops.render.render(write_still=True)
print('FURNACE_BUILD_COMPLETE')
