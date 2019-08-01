import bpy
from bpy.types import Operator
from bpy.props import (IntProperty, EnumProperty)

import mathutils
from mathutils import Vector

# Helper Function - return a Vector corresponding to a named axis
def str_to_axis(str):
	if(str == "X_AXIS"):
		return Vector((1, 0, 0))
	if(str == "Y_AXIS"):
		return Vector((0, 1, 0))
	if(str == "Z_AXIS"):
		return Vector((0, 0, 1))


# This class represents the whole duplication/shift operator.
class DupeAndShift(bpy.types.Operator):

	# Tooltip info
	bl_idname  = "mesh.dupe_and_shift"
	bl_label = "Duplicate and shift object"
	bl_options = {"REGISTER", "UNDO", "PRESET"}

	# Ensure exactly one object is be selected to use this operator
	@classmethod
	def poll(cls, context):
		return len(context.selected_objects) == 1

	# Number of duplications to perform
	n_iterations = IntProperty(
		name = "iterations",
		default = 1,
		min = 1,
		max = 999)

	# Axis to perform shift
	duplication_axis = EnumProperty(
		name="Axis",
		description = "Description",
		items = (("X_AXIS", "X", "x-axis"),
				("Y_AXIS", "Y", "y-axis"),
				("Z_AXIS", "Z", "z-axis"),
			),
			default = "X_AXIS")


	# Duplicate the selected object n times, shifting each one further along the duplication axis.
	def dupe_object(self):
		target_obj = bpy.context.selected_objects[0] # Get currently selected object.
		obj_list = [target_obj]

		# get the offset vector to move each new objects by.
		axis = str_to_axis(self.duplication_axis)
		offset_vec = Vector((target_obj.dimensions.x * axis.x,
							target_obj.dimensions.y * axis.y,
							target_obj.dimensions.z * axis.z))

		# loop through and duplicate the desigred amount of objects. Add each to the return list.
		for num_shifts in range(self.n_iterations):
			new_obj = target_obj.copy() # duplicate linked
			new_obj.data = target_obj.data.copy() # make this a real duplicate (not linked)
			bpy.context.collection.objects.link(new_obj) # add to scene collection

			new_obj.location += ((num_shifts + 1) * offset_vec)
			obj_list.append(new_obj)

		return obj_list

	def join_objects(self, obj_list):
		c = {}
		c["object"] = c["active_object"] = obj_list[0]
		c["selected_objects"] = c["selected_editable_objects"] = obj_list
		bpy.ops.object.join(c, "EXEC_DEFAULT")


	def remove_overlapping_verticies(self):
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_all(action="SELECT")
		bpy.ops.mesh.remove_doubles("EXEC_DEFAULT")
		bpy.ops.object.editmode_toggle()

	def execute(self, context):
		obj_list = self.dupe_object();
		self.join_objects(obj_list);
		self.remove_overlapping_verticies();
		return {"FINISHED"}


def menu_func(self, context):
	# Add the operator to the context menu
	self.layout.operator(
		DupeAndShift.bl_idname,
		text=DupeAndShift.__doc__,
		icon="PLUGIN")

def register():
	bpy.utils.register_class(DupeAndShift)
	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
	bpy.utils.unregister_class(DupeAndShift)
	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":  
	register()
