"""Export the aconite models to Blender (.blend + .glb).  python tools/export_blender.py
Pixel-perfect: nearest-neighbour textures, alpha clip for the 2D plants. 1 Blender unit = 1 block."""
import json, math, os, sys
import bpy
sys.path.insert(0, os.path.dirname(__file__))
from mclib import FACES, rotmat
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "resourcepack", "assets", "aconite")
OUT = os.path.join(ROOT, "exports")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
mats = {}

def material(png):
    if png in mats:
        return mats[png]
    m = bpy.data.materials.new(os.path.basename(png)[:-4]); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(png); tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    bsdf.inputs["Roughness"].default_value = 0.9
    if hasattr(m, "blend_method"):
        m.blend_method = "CLIP"
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "DITHERED"
    mats[png] = m
    return m

def to_bl(p):  # MC (x, y, z) pixels, y up -> Blender metres, z up; block centred on origin
    return ((p[0] - 8) / 16, (p[2] - 8) / 16 * -1, p[1] / 16)

def build(name, quads, png, coll, loc=(0, 0, 0)):
    """quads: list of (4 corners in MC px, uv [u0,v0,u1,v1] in 0..16)"""
    verts, faces, uvs = [], [], []
    for corners, uv in quads:
        i = len(verts); verts += [to_bl(c) for c in corners]; faces.append((i, i + 1, i + 2, i + 3))
        u0, v0, u1, v1 = uv
        uvs += [(u0 / 16, 1 - v0 / 16), (u1 / 16, 1 - v0 / 16), (u1 / 16, 1 - v1 / 16), (u0 / 16, 1 - v1 / 16)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for li, loop in enumerate(me.loops):
        uvl.data[li].uv = uvs[loop.vertex_index]
    me.materials.append(material(png))
    ob = bpy.data.objects.new(name, me); ob.location = loc; coll.objects.link(ob)
    return ob

def element_quads(el):
    a, b = el["from"], el["to"]
    R, O = (rotmat(el["rotation"]["axis"], el["rotation"]["angle"]), np.array(el["rotation"]["origin"], float)) \
        if "rotation" in el else (np.eye(3), np.zeros(3))
    out = []
    for d, (n, geo) in FACES.items():
        if d not in el["faces"]:
            continue
        o, du, dv = (np.array(v, float) for v in geo(a, b))
        cs = [o, o + du, o + du + dv, o + dv]
        out.append(([R @ (c - O) + O for c in cs], el["faces"][d]["uv"]))
    return out

def cross_quads(y0=0):
    out = []
    for ang in (45, -45):
        R = rotmat("y", ang); O = np.array([8, 8, 8.0])
        for flip in (False, True):  # two-sided
            o, du, dv = np.array([0.8, y0 + 16, 8.0]), np.array([14.4, 0, 0]), np.array([0, -16, 0.0])
            cs = [o, o + du, o + du + dv, o + dv]
            uv = [0, 0, 16, 16]
            if flip:
                cs = [cs[1], cs[0], cs[3], cs[2]]; uv = [16, 0, 0, 16]
            out.append(([R @ (c - O) + O for c in cs], uv))
    return out

def coll(name):
    c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c

# 3D chunky aconite
c3d = coll("Aconite_3D")
j = json.load(open(os.path.join(A, "models/item/aconite_3d.json")))
q = [qq for el in j["elements"] for qq in element_quads(el)]
build("Aconite_3D", q, os.path.join(A, "textures/item/aconite_3d.png"), c3d)

# 2D cross-plant growth stages (+ full flower and wolfsbane), lined up along X
c2d = coll("Aconite_2D_Growth")
T = os.path.join(A, "textures/block")
plants = [("Stage1_Sprout", ["aconite_stage0"]), ("Stage2_Leaves", ["aconite_stage1"]),
          ("Stage3_YellowBuds", ["aconite_stage2"]), ("Stage4_BudsTurning", ["aconite_stage3"]),
          ("Stage5_TwoBlocks", ["aconite_stage4_bottom", "aconite_stage4_top"]),
          ("Stage6_FullBloom", ["aconite_stage5_bottom", "aconite_stage5_top"]),
          ("Wolfsbane_Yellow", ["wolfsbane_bottom", "wolfsbane_top"])]
for i, (name, texs) in enumerate(plants):
    for k, t in enumerate(texs):
        build(f"{name}_{'top' if k else 'bottom'}" if len(texs) > 1 else name, cross_quads(16 * k),
              os.path.join(T, t + ".png"), c2d, loc=(1.5 * (i + 1), 0, 0))

bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "aconite_models.blend"))
# glb of just the 3D aconite, and one of everything
for ob in bpy.data.objects:
    ob.select_set(ob.name == "Aconite_3D")
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "aconite_3d.glb"), use_selection=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "aconite_all.glb"), use_selection=False)
print("exported", [o.name for o in bpy.data.objects])
