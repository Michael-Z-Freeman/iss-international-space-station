import bpy
import bmesh

output_file = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/zvezda_fix_log.txt"

# Search for the Zvezda object
zvezda_obj = None
for obj in bpy.data.objects:
    if "Zvezda" in obj.name or "Service Module" in obj.name:
        zvezda_obj = obj
        break

with open(output_file, "w") as f:
    if not zvezda_obj:
        f.write("Error: Could not find Zvezda/Service Module object.")
    else:
        f.write(f"Fixing Object: {zvezda_obj.name}\n")
        
        # 1. Fix Material
        if zvezda_obj.active_material:
            mat = zvezda_obj.active_material
            f.write(f"Updating Material: {mat.name}\n")
            mat.blend_method = 'OPAQUE'
            mat.use_backface_culling = False
            f.write("Set Blend Mode to OPAQUE and disabled Backface Culling.\n")
        else:
            f.write("No material found to fix.\n")
            
        # 2. Recalculate Normals
        try:
            # Set as active and select
            bpy.context.view_layer.objects.active = zvezda_obj
            zvezda_obj.select_set(True)
            
            # Switch to edit mode to recalculate
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            f.write("Successfully recalculated normals (Outward).\n")
        except Exception as e:
            f.write(f"Error recalculating normals: {str(e)}\n")

