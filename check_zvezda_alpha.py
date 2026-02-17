import bpy

zvezda_obj = None
for obj in bpy.data.objects:
    if "Zvezda" in obj.name or "Service Module" in obj.name:
        zvezda_obj = obj
        break

output_file = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/zvezda_alpha_report.txt"

with open(output_file, "w") as f:
    if not zvezda_obj:
        f.write("Object not found.")
    else:
        f.write(f"Object: {zvezda_obj.name}\n")
        for slot in zvezda_obj.material_slots:
            if slot.material:
                mat = slot.material
                f.write(f"--- Material: {mat.name} ---\n")
                f.write(f"  Blend Mode (Viewport): {mat.blend_method}\n")
                f.write(f"  Backface Culling: {mat.use_backface_culling}\n")
                
                if mat.use_nodes:
                    # Find Principled BSDF
                    nodes = mat.node_tree.nodes
                    principled = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
                    if principled:
                        alpha_input = principled.inputs['Alpha']
                        f.write(f"  Alpha Value: {alpha_input.default_value}\n")
                        if alpha_input.is_linked:
                            f.write(f"  Alpha is LINKED to: {alpha_input.links[0].from_node.type}\n")
                    else:
                        f.write("  No Principled BSDF found.\n")
                else:
                    f.write(f"  Alpha (Non-Nodes): {mat.diffuse_color[3]}\n")
