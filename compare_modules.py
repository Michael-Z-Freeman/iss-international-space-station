import bpy

def get_obj_info(search_name):
    obj = None
    for o in bpy.data.objects:
        if search_name in o.name:
            obj = o
            break
    if not obj:
        return f"Object '{search_name}' not found.\n"
    
    info = f"--- Comparison for: {obj.name} ---\n"
    info += f"Type: {obj.type}\n"
    
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                mat = slot.material
                info += f"  Material: {mat.name}\n"
                info += f"    Blend Mode: {mat.blend_method}\n"
                info += f"    Backface Culling: {mat.use_backface_culling}\n"
                if mat.use_nodes:
                    principled = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                    if principled:
                        alpha = principled.inputs['Alpha']
                        info += f"    Alpha Val: {alpha.default_value}\n"
                        info += f"    Alpha Linked: {alpha.is_linked}\n"
                        if alpha.is_linked:
                             info += f"      From Node: {alpha.links[0].from_node.type}\n"
                info += f"    Show Backface: {getattr(mat, 'show_backface', 'N/A')}\n"
    
    # Check normals orientation on a sample
    mesh = obj.data
    inward = 0
    check_cnt = min(50, len(mesh.polygons))
    for i in range(check_cnt):
        poly = mesh.polygons[i]
        if poly.normal.dot(poly.center) < 0:
            inward += 1
    info += f"  Normals Sample: {inward}/{check_cnt} point inward.\n"
    return info

output_file = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/module_comparison.txt"
with open(output_file, "w") as f:
    f.write(get_obj_info("US Laboratory"))
    f.write("\n")
    f.write(get_obj_info("Zvezda Service Module"))
