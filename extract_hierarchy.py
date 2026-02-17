import bpy
import os

output_path = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/iss_hierarchy.txt"

def get_hierarchy(obj, level=0):
    # Basic info: Name, Type
    info = f"{obj.name} [{obj.type}]"
    
    # Add mesh details if applicable
    if obj.type == 'MESH' and obj.data:
        info += f" (Verts: {len(obj.data.vertices)}, Faces: {len(obj.data.polygons)})"
        
    result = "  " * level + info + "\n"
    
    # Sort children by name for consistent output
    children = sorted(obj.children, key=lambda x: x.name)
    for child in children:
        result += get_hierarchy(child, level + 1)
    return result

try:
    with open(output_path, "w") as f:
        f.write("Scene Hierarchy:\n")
        # Get all objects in the current scene
        scene = bpy.context.scene
        # Find root objects (no parent)
        roots = [obj for obj in scene.objects if obj.parent is None]
        # Sort roots by name for consistency
        roots.sort(key=lambda x: x.name)
        
        for root in roots:
            f.write(get_hierarchy(root))
            
    print(f"Hierarchy written to {output_path}")
except Exception as e:
    print(f"Error writing hierarchy: {e}")
