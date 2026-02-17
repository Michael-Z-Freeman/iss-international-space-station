import bpy

zvezda_obj = None
for obj in bpy.data.objects:
    if "Zvezda" in obj.name or "Service Module" in obj.name:
        zvezda_obj = obj
        break

output_file = "/Volumes/RecordBoxNVMe/ReturnToTheSource/iss-international-space-station/zvezda_all_mats.txt"

with open(output_file, "w") as f:
    if not zvezda_obj:
        f.write("Object not found.")
    else:
        f.write(f"Object: {zvezda_obj.name}\n")
        f.write(f"Materials found: {len(zvezda_obj.material_slots)}\n")
        for slot in zvezda_obj.material_slots:
            if slot.material:
                mat = slot.material
                f.write(f"--- Material: {mat.name} ---\n")
                f.write(f"  Blend Mode: {mat.blend_method}\n")
                f.write(f"  Backface Culling: {mat.use_backface_culling}\n")
            else:
                f.write("--- Empty Slot ---\n")
