import bpy
import os

output_file = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/zvezda_inspection.txt"

# Search for the Zvezda object (it might have been renamed)
zvezda_obj = None
for obj in bpy.data.objects:
    if "Zvezda" in obj.name or "Service Module" in obj.name:
        zvezda_obj = obj
        break

with open(output_file, "w") as f:
    if not zvezda_obj:
        f.write("Could not find Zvezda/Service Module object.")
    else:
        f.write(f"--- Inspection Result for: {zvezda_obj.name} ---\n")
        f.write(f"Type: {zvezda_obj.type}\n")
        
        if zvezda_obj.type == 'MESH':
            mesh = zvezda_obj.data
            
            # 1. Check Normals
            inward_count = 0
            total_check = min(100, len(mesh.polygons))
            for i in range(total_check):
                poly = mesh.polygons[i]
                if poly.normal.dot(poly.center) < 0:
                    inward_count += 1
            
            f.write(f"Normal Direction: {inward_count}/{total_check} faces point inward (local origin).\n")
            
            # 2. Check Material Properties
            if zvezda_obj.active_material:
                mat = zvezda_obj.active_material
                f.write(f"Material: {mat.name}\n")
                f.write(f"  Blend Mode: {mat.blend_method}\n")
                f.write(f"  Backface Culling: {mat.use_backface_culling}\n")
                
                # Check for Alpha/Transparency
                if mat.use_nodes:
                    principled = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                    if principled:
                        try:
                            alpha = principled.inputs['Alpha'].default_value
                            f.write(f"  Principled Alpha: {alpha}\n")
                        except Exception as e:
                            f.write(f"  Could not get alpha from node: {str(e)}\n")
            else:
                f.write("No material assigned.\n")
                
        # 3. Check for modifiers that might affect display
        for mod in zvezda_obj.modifiers:
            f.write(f"Modifier: {mod.name} ({mod.type}) - Show in Viewport: {mod.show_viewport}\n")
