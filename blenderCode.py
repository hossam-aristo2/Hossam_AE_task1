import bpy
import math
import random
from mathutils import Euler, Vector
from pathlib import Path
import bpy_extras


def randomly_position_upright_only(obj_to_change, plane_name='Plane'):
    plane = bpy.context.scene.objects[plane_name]
    plane_dimensions = plane.dimensions
    obj_dimensions = obj_to_change.dimensions

    random_x = random.uniform(-plane_dimensions.x/2, plane_dimensions.x/2)
    random_y = random.uniform(-plane_dimensions.y/2, plane_dimensions.y/2)
    random_z = obj_dimensions.z / 2  
    
    obj_to_change.location = plane.location + Vector((random_x, random_y, random_z))
    

    random_rot = (
        random.uniform(0, math.pi),      # X rotation
        random.uniform(0, math.pi/4),    # Y rotation
        random.uniform(0, 2 * math.pi)   # Z rotation
    )
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')

def get_yolo_bbox(obj, scene):
    coords_3d = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    coords_2d = [bpy_extras.object_utils.world_to_camera_view(scene, scene.camera, co) for co in coords_3d]

    min_x = max(min([c.x for c in coords_2d]), 0)
    max_x = min(max([c.x for c in coords_2d]), 1)
    min_y = max(min([c.y for c in coords_2d]), 0)
    max_y = min(max([c.y for c in coords_2d]), 1)

    x_center = (min_x + max_x) / 2
    y_center = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y

    return (x_center, y_center, width, height)

output_dir = Path('/Volumes/ELHOSS SSD/ALEXEAGLES/TASK1/renderdResults')
output_dir.mkdir(parents=True, exist_ok=True)
yolo_output_dir = Path('/Volumes/ELHOSS SSD/ALEXEAGLES/TASK1/yolo')
yolo_output_dir.mkdir(parents=True, exist_ok=True)
class_id = 0  


for i in range(50):
    if 'FinalBaseMesh' in bpy.context.scene.objects and 'Plane' in bpy.context.scene.objects:
        obj = bpy.context.scene.objects['FinalBaseMesh']
        randomly_position_upright_only(obj, 'Plane')
        
        render_path = output_dir / f"render_{i:03d}.png"
        bpy.context.scene.render.filepath = str(render_path)
        bpy.ops.render.render(write_still=True)
        
        yolo_path = yolo_output_dir / f"render_{i:03d}.txt"
        bbox = get_yolo_bbox(obj, bpy.context.scene)
        with open(yolo_path, 'w') as f:
            f.write(f"{class_id} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
        
        print(f"Render {i+1}/50 saved to: {render_path} and YOLO annotation: {yolo_path}")

print("All 50 renders and YOLO annotations completed!")
