import bpy, sys, os
from mathutils import Vector
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','aconite')+'/'
OUT=sys.argv[sys.argv.index('--')+1]
PREV=sys.argv[sys.argv.index('--')+2]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
col=bpy.data.collections.new('ACONITE'); sc.collection.children.link(col)

def hexc(h,a=1):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return (*c,a)

def imp(name,fn):
    before=set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=D+fn)
    objs=[o for o in bpy.data.objects if o not in before]
    for o in objs:
        for c in list(o.users_collection): c.objects.unlink(o)
        col.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    if len(objs)>1: bpy.ops.object.join()
    o=bpy.context.view_layer.objects.active; o.name=o.data.name=name
    for c in list(bpy.data.collections):
        if c!=col and not c.objects and c.name!='ACONITE': bpy.data.collections.remove(c)
    return o

L=imp('ACONITE_Letters','letters.svg')
V=imp('ACONITE_Vines','vines.svg')
O=imp('ACONITE_Outlines','outlines.svg')

# normalise: centre on letters, 6 m wide, standing upright (XZ plane, facing -Y)
pts=[L.matrix_world@p.co.xyz for s in L.data.splines for p in s.bezier_points]
mn=Vector([min(p[i] for p in pts) for i in range(3)]); mx=Vector([max(p[i] for p in pts) for i in range(3)])
ctr=(mn+mx)/2; s=6.0/(mx.x-mn.x)
root=bpy.data.objects.new('ACONITE_Logo',None); col.objects.link(root)
for o in (L,V,O):
    o.parent=root; o.location=(-ctr.x,-ctr.y,0)
    o.data.dimensions='2D'; o.data.fill_mode='BOTH'
root.scale=(s,s,s); root.rotation_euler=(1.5708,0,0)

ex=lambda m: m/s  # metres -> local units
L.data.extrude=ex(0.10); L.data.bevel_depth=ex(0.012); L.data.bevel_resolution=3
V.data.extrude=ex(0.012); V.location.z=ex(0.115)
O.data.extrude=ex(0.010); O.location.z=ex(0.13)

def mat(name):
    m=bpy.data.materials.new(name); m.use_nodes=True
    return m,m.node_tree.nodes,m.node_tree.links
# letters: vertical gradient #7a35d0 (top) -> #3a1478 (bottom) + fine grain
m,n,l=mat('ACONITE_Letters'); b=n['Principled BSDF']
tc=n.new('ShaderNodeNewGeometry'); sep=n.new('ShaderNodeSeparateXYZ'); mr=n.new('ShaderNodeMapRange')
ramp=n.new('ShaderNodeValToRGB'); noi=n.new('ShaderNodeTexNoise'); mix=n.new('ShaderNodeMix')
l.new(tc.outputs['Position'],sep.inputs[0]); l.new(sep.outputs['Z'],mr.inputs[0]); mr.inputs['From Min'].default_value=-1.5; mr.inputs['From Max'].default_value=1.4
ramp.color_ramp.elements[0].color=hexc('3a1478'); ramp.color_ramp.elements[1].color=hexc('7a35d0')
ramp.color_ramp.elements[0].position=0.0; ramp.color_ramp.elements[1].position=0.85
l.new(mr.outputs[0],ramp.inputs[0])
noi.inputs['Scale'].default_value=900; noi.inputs['Detail'].default_value=0
mix.data_type='RGBA'; mix.blend_type='MULTIPLY'; mix.inputs['Factor'].default_value=0.18
l.new(ramp.outputs[0],mix.inputs['A']); l.new(noi.outputs['Color'],mix.inputs['B'])
l.new(mix.outputs['Result'],b.inputs['Base Color'])
l.new(mix.outputs['Result'],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=0.8
b.inputs['Roughness'].default_value=0.35; b.inputs['Specular IOR Level'].default_value=0.6
L.data.materials.clear(); L.data.materials.append(m)
# vines: glowing pale green
m,n,l=mat('ACONITE_Vines'); b=n['Principled BSDF']
b.inputs['Base Color'].default_value=hexc('d8f5b0'); b.inputs['Emission Color'].default_value=hexc('d8f5b0')
b.inputs['Emission Strength'].default_value=1.2
V.data.materials.clear(); V.data.materials.append(m)
# outlines: dark purple ink
m,n,l=mat('ACONITE_Outlines'); b=n['Principled BSDF']
b.inputs['Base Color'].default_value=hexc('2b0a4c'); b.inputs['Roughness'].default_value=0.6
b.inputs['Emission Color'].default_value=hexc('2b0a4c'); b.inputs['Emission Strength'].default_value=0.0
O.data.materials.clear(); O.data.materials.append(m)

for mm in list(bpy.data.materials):
    if not mm.users: bpy.data.materials.remove(mm)
# preview scene (not part of the ACONITE collection)
pc=bpy.data.collections.new('Preview'); sc.collection.children.link(pc)
cam=bpy.data.objects.new('Cam',bpy.data.cameras.new('Cam')); pc.objects.link(cam)
cam.location=(0.4,-9,0); cam.rotation_euler=(1.5708,0,0.045); cam.data.lens=50
sc.camera=cam
for nm,loc,e in [('Key',(-3,-5,4),250),('Rim',(4,3,2),500)]:
    li=bpy.data.objects.new(nm,bpy.data.lights.new(nm,'AREA')); li.data.energy=e; li.data.size=4
    li.location=loc; pc.objects.link(li)
    li.rotation_euler=(Vector((0,0,0))-li.location).to_track_quat('-Z','Y').to_euler()
w=bpy.data.worlds.new('W'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1); sc.world=w
sc.render.resolution_x,sc.render.resolution_y=1500,1150
sc.view_settings.view_transform='Standard'
# glow in compositor
sc.render.use_compositing=False
try:
    tree=bpy.data.node_groups.new('Glow','CompositorNodeTree'); sc.compositing_node_group=tree
    i=tree.nodes.new('CompositorNodeRLayers'); g=tree.nodes.new('CompositorNodeGlare'); o=tree.nodes.new('NodeGroupOutput')
    tree.interface.new_socket('Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    g.inputs['Type'].default_value='Bloom' if 'Type' in g.inputs else None
    for k,v in (('Threshold',0.8),('Strength',1.0),('Size',0.8)):
        if k in g.inputs: g.inputs[k].default_value=v
    tree.links.new(i.outputs['Image'],g.inputs['Image']); tree.links.new(g.outputs['Image'],o.inputs[0])
except Exception as e: print('glare skipped',e)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
eng=os.environ.get('ENG','CYCLES')
sc.render.engine='BLENDER_EEVEE' if eng=='EEVEE' else 'CYCLES'
if eng!='EEVEE': sc.cycles.samples=48; sc.cycles.device='CPU'
sc.render.filepath=PREV; bpy.ops.render.render(write_still=True)
print('DONE')
