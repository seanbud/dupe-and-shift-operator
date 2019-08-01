import bpy

## Assume that the selected object is half of what you need copied, 
##  The object should sit to the right of it's origin, (positive X)
##  ready for mirroring along the Z axis

# get selected object
obj = bpy.context.selected_objects[0]

# store the width of the object
width = obj.dimensions.z

# add mirror modifier z axis, clipping enabled.
mod = obj.modifiers.new(name="mirror_z", type='MIRROR')
mod.use_axis[0] = False
mod.use_axis[1] = False
mod.use_axis[2] = True
mod.use_clip = True

# apply the modifier
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="mirror_z")

# move the origin of the object over
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.translate(value=(width, 0, 0), constraint_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
bpy.ops.object.mode_set(mode='OBJECT')
