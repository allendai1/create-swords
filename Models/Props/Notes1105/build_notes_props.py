# Props for the 2026-11-05 notes, Sell Swords! (low poly, flat shaded, the festival props' helpers and export):
#   StreetLantern - a round paper lantern (chochin) for the festival strings over the road: Paper body (recoloured red
#                   or white per copy), Dark top and bottom caps and a short cord. Origin at the top of the cord.
#   DeliveryBoard - the courier order board in the delivery bay: two posts, a plank Board in a dark frame, a little
#                   tiled roof, paper slips pinned on its front. ~5 wide, 6.4 tall.
#   AutoRoller    - the Auto Ore Roller's motor beside the ore lever: a stone plinth, a wooden cradle, an iron-banded
#                   drum, a shaft out to the lever (+X here, Roblox -X), a spoked flywheel at the far end (Flywheel and
#                   Hub turn about Axle), a round lamp on top. Same footprint as the part-built one.
#   SakuraTree    - a cherry tree for a planter in the road: a curved dark trunk with three limbs, clumped pink canopy
#                   in three shades, a stone kerb ring and soil.
#
# Run in Blender (MCP execute_blender_code: exec(open(<this file>).read())). Writes <Name>.fbx next to this file
# (blender-export-pipelines `roblox` preset). Units are studs, Z up, the front faces -Y (Roblox -Z), origin on the
# floor at the foot centre (the lantern: at the hanging point). One object per Studio material, named for its part.
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Notes1105"
FESTIVAL = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Festival/build_festival.py"
SKILLS = "C:/Users/Allen/.claude/plugins/cache/blender-agent-skills/blender-agent-skills/1.1.0/skills"

# the festival props' helpers (fresh_collection, box, cyl, lathe, join, gable), without running their builds
_src = open(FESTIVAL).read()
exec(_src[:_src.index("def export(name):")])
HERE = "C:/Users/Allen/Documents/Create Swords!/Models/Props/Notes1105"  # the festival file sets its own


def limb(p0, p1, r0, r1, verts=6):
    """A tapered log from p0 to p1 (a cone frustum along the segment)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = cyl(r0, d.length, (p0 + p1) / 2, verts=verts, r2=r1)
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.normalized().to_track_quat("Z", "Y")
    return o


def ring_x(r, width, x, z, verts=10):
    """A closed band about the X axis (a lathe turned onto X), centred at (x, 0, z)."""
    o = lathe([(0, -width / 2), (r, -width / 2), (r, width / 2), (0, width / 2)], (0, 0, 0), verts=verts)
    o.rotation_euler = (0, math.pi / 2, 0)
    o.location = (x, 0, z)
    return o


def build_lantern():
    coll = fresh_collection("StreetLantern")
    parts = {}
    top, h = -0.36, 0.9  # the paper's top, its height
    # faint ribs: every inner ring sits a hair proud, so the flat facets read as the bamboo ribs under the paper
    prof = [(0, 0), (0.42, 0.0), (0.6, 0.18), (0.655, 0.36), (0.65, 0.45), (0.655, 0.54), (0.6, 0.72), (0.42, 0.9), (0, 0.9)]
    parts["Paper"] = join([lathe(prof, (0, 0, top - h), verts=8)], "Paper", coll)
    parts["Dark"] = join([cyl(0.045, 0.34, (0, 0, -0.17), verts=4),
                          cyl(0.46, 0.1, (0, 0, top + 0.02), verts=8),
                          cyl(0.46, 0.1, (0, 0, top - h - 0.02), verts=8)], "Dark", coll)
    return coll, parts


def build_board():
    coll = fresh_collection("DeliveryBoard")
    parts = {}
    W, BZ0, BZ1 = 4.1, 1.75, 5.15  # board width, bottom, top
    parts["Board"] = join([box((W, 0.16, BZ1 - BZ0), (0, 0, (BZ0 + BZ1) / 2))] +
                          [box((W, 0.04, 0.05), (0, -0.09, BZ0 + (BZ1 - BZ0) * k / 4)) for k in (1, 2, 3)],  # plank seams
                          "Board", coll)
    dark = []
    for x in (-2.3, 2.3):
        dark.append(box((0.34, 0.34, 6.05), (x, 0, 3.025)))           # posts
        dark.append(box((0.5, 0.5, 0.2), (x, 0, 0.1)))                 # foot blocks
    dark.append(box((W + 0.3, 0.26, 0.2), (0, 0, BZ1 + 0.1)))          # frame top
    dark.append(box((W + 0.3, 0.26, 0.2), (0, 0, BZ0 - 0.1)))          # frame bottom
    dark.append(box((4.95, 0.3, 0.25), (0, 0, 5.86)))                  # top beam under the roof
    dark.append(box((4.6, 0.2, 0.2), (0, 0, 0.9)))                     # low rail
    parts["Dark"] = dark
    # paper slips, a little askew, pinned at their tops
    papers, pins = [], []
    for (x, z, w, hh, tilt) in ((-1.35, 4.15, 1.0, 1.25, 4), (-0.05, 4.3, 0.95, 1.05, -3), (1.25, 4.05, 1.1, 1.3, 2),
                                (-0.8, 2.65, 1.15, 1.0, -2), (0.75, 2.55, 0.9, 1.1, 5)):
        papers.append(box((w, 0.04, hh), (x, -0.13, z), rot=(0, math.radians(tilt), 0)))  # 0.04 proud of the plank seams
        pins.append(box((0.09, 0.06, 0.09), (x - math.sin(math.radians(tilt)) * hh * 0.42, -0.17,
                                             z + math.cos(math.radians(tilt)) * hh * 0.42)))
    parts["Paper"] = join(papers, "Paper", coll)
    parts["Dark"] = join(dark + pins, "Dark", coll)
    parts["Roof"] = join(gable(5.2, 0.75, 6.18, math.radians(30), 7, thick=0.16), "Roof", coll)
    return coll, parts


def build_roller():
    """Lever side +X (Roblox -X). Drum axis at z 2.0 (the old one's height over the paving)."""
    coll = fresh_collection("AutoRoller")
    parts = {}
    AZ = 2.0
    parts["Stone"] = join([box((2.7, 2.6, 0.24), (0, 0, 0.12)), box((2.5, 2.4, 0.1), (0, 0, 0.29))], "Stone", coll)
    wood = [box((0.32, 1.5, 1.2), (x, 0, 0.34 + 0.6)) for x in (-0.35, 0.85)]  # cradle under the drum
    wood += [box((0.4, 0.2, 0.7), (x, s * 0.72, 0.34 + 0.35), rot=(s * math.radians(18), 0, 0)) for x in (-0.35, 0.85) for s in (-1, 1)]
    drum = lathe([(0, -0.8), (0.8, -0.8), (0.9, -0.4), (0.93, 0), (0.9, 0.4), (0.8, 0.8), (0, 0.8)], (0, 0, 0), verts=10)
    drum.rotation_euler = (0, math.pi / 2, 0)
    drum.location = (0.25, 0, AZ)
    parts["Wood"] = join(wood + [drum], "Wood", coll)
    iron = [ring_x(0.95, 0.12, 0.25 + s * 0.42, AZ) for s in (-1, 1)]
    iron.append(cyl(0.14, 3.25, (1.05 + 3.25 / 2, 0, AZ), rot=(0, math.pi / 2, 0), verts=6))  # shaft out to the lever
    iron.append(cyl(0.25, 0.14, (1.12, 0, AZ), rot=(0, math.pi / 2, 0), verts=8))             # collar at the drum
    iron.append(cyl(0.25, 0.14, (4.23, 0, AZ), rot=(0, math.pi / 2, 0), verts=8))             # collar at the lever
    iron.append(box((0.44, 0.44, 0.1), (0.25, 0, AZ + 0.95)))                                 # lamp seat
    # (no lamp cap or finial since 2026-11-06, Allen: "remove the cap on top"; the lamp is a Roblox ball half sunk in the seat)
    parts["Iron"] = join(iron, "Iron", coll)
    parts["Axle"] = join([cyl(0.18, 0.62, (-0.84, 0, AZ), rot=(0, math.pi / 2, 0), verts=8)], "Axle", coll)
    # the flywheel: a ten-sided rim on four spokes
    fx, R, rim = -0.97, 1.2, 0.24
    wheel = []
    for k in range(10):
        a = 2 * math.pi * (k + 0.5) / 10
        rr = R - rim / 2
        wheel.append(box((0.24, 2 * R * math.tan(math.pi / 10) + 0.02, rim), (fx, rr * math.cos(a), AZ + rr * math.sin(a)), rot=(a - math.pi / 2, 0, 0)))
    wheel.append(box((0.16, 0.2, 2 * R - 0.2), (fx, 0, AZ)))
    wheel.append(box((0.16, 2 * R - 0.2, 0.2), (fx, 0, AZ)))
    parts["Flywheel"] = join(wheel, "Flywheel", coll)
    parts["Hub"] = join([cyl(0.3, 0.3, (-1.17, 0, AZ), rot=(0, math.pi / 2, 0), verts=8),
                         cyl(0.11, 0.4, (-1.3, 0, AZ + 0.8), rot=(0, math.pi / 2, 0), verts=6)], "Hub", coll)  # crank pin
    parts["Lamp"] = join([lathe([(0, 0), (0.2, 0.0), (0.33, 0.14), (0.33, 0.42), (0.2, 0.56), (0, 0.56)], (0.25, 0, 3.0), verts=8)], "Lamp", coll)
    return coll, parts


def build_sakura():
    coll = fresh_collection("SakuraTree")
    parts = {}
    rnd = random.Random(1105)
    # a gently curved trunk, then five limbs fanning out into the canopy
    spine = [(0, 0, -0.2), (0.3, 0.05, 2.3), (0.15, -0.1, 4.5), (-0.3, 0.1, 6.5)]
    radii = [0.75, 0.6, 0.5, 0.44]
    trunk = [limb(spine[i], spine[i + 1], radii[i], radii[i + 1] * 1.02) for i in range(3)]
    trunk.append(cyl(0.95, 0.5, (0, 0, 0.25), verts=6, r2=0.7))  # root flare
    fork = Vector(spine[-1])
    tips = []
    for (deg, reach, rise, r) in ((195, 4.0, 3.0, 0.34), (320, 3.9, 2.8, 0.32), (75, 3.7, 3.2, 0.32), (130, 3.6, 2.7, 0.28), (20, 3.6, 3.4, 0.3)):
        a = math.radians(deg)
        d = Vector((reach * math.cos(a), reach * math.sin(a), rise))
        mid = fork + Vector((d.x * 0.45, d.y * 0.45, d.z * 0.6))
        end = fork + d
        trunk.append(limb(fork - Vector((0, 0, 0.35)), mid, r, r * 0.75))
        trunk.append(limb(mid, end, r * 0.75, r * 0.4))
        tips.append(end)
    parts["Trunk"] = join(trunk, "Trunk", coll)
    # canopy clumps on the limb tips and over the crown, flattened; three shades
    clumps = [(t, 2.4) for t in tips] + [(fork + Vector((0, 0, 5.5)), 2.8), (fork + Vector((-1.6, -1.9, 4.4)), 2.2),
                                         (fork + Vector((1.7, 1.6, 4.7)), 2.2), (fork + Vector((2.0, -1.8, 4.1)), 2.0)]
    shades = {"Blossom": [], "BlossomLight": [], "BlossomDark": []}
    order = ["Blossom", "BlossomDark", "BlossomLight", "BlossomDark", "Blossom", "BlossomLight", "Blossom", "BlossomDark", "BlossomLight"]
    for (c, r), shade in zip(clumps, order):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=r, location=c)
        o = bpy.context.active_object
        o.scale = (1.0 + rnd.uniform(-0.08, 0.12), 1.0 + rnd.uniform(-0.08, 0.12), 0.66)
        o.rotation_euler = (rnd.uniform(0, 0.4), rnd.uniform(0, 0.4), rnd.uniform(0, math.pi))
        shades[shade].append(o)
    for n, objs in shades.items():
        parts[n] = join(objs, n, coll)
    # stone kerb ring (ten cut stones round a 5-stud circle) and soil inside
    stones = []
    for k in range(10):
        a = 2 * math.pi * k / 10
        h = 0.44 if k % 2 == 0 else 0.36  # tops 0.04 apart where neighbours overlap
        stones.append(box((0.5, 2 * 2.3 * math.tan(math.pi / 10) + 0.04, h), (2.3 * math.cos(a), 2.3 * math.sin(a), h / 2 - 0.02), rot=(0, 0, a)))
    parts["Stone"] = join(stones, "Stone", coll)
    parts["Soil"] = join([cyl(2.15, 0.2, (0, 0, 0.06), verts=10)], "Soil", coll)
    return coll, parts


def export(name):
    p = os.path.join(SKILLS, "blender-export-pipelines", "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import importlib
    exp = importlib.import_module("export_asset")
    return exp.run(preset="roblox", collection=name, out=os.path.join(HERE, name + ".fbx"), batch=False, no_anim=True)


BUILT = {}
for label, fn in (("StreetLantern", build_lantern), ("DeliveryBoard", build_board), ("AutoRoller", build_roller), ("SakuraTree", build_sakura)):
    coll, ps = fn()
    BUILT[label] = ps
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in ps.values())
    print(label, {n: len(o.data.polygons) for n, o in ps.items()}, "tris", tris)
