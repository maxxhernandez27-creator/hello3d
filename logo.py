


import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Materials
def make_material(name, color, metallic=0.5):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.25
    return mat

blue = make_material("Python Blue", (0.05, 0.25, 0.85), 0.7)
yellow = make_material("Python Yellow", (1.0, 0.65, 0.02), 0.7)
white = make_material("White Text", (0.9, 0.95, 1), 0.4)
black = make_material("Dark Background", (0.015, 0.02, 0.06))

# Create 3D spheres
def create_snake_part(name, location, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=32,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj

# Python-inspired logo shapes
create_snake_part("Blue Python Head", (-0.8, 0, 0.5), (1.2, 0.65, 0.65), blue)
create_snake_part("Yellow Python Head", (0.8, 0, -0.5), (1.2, 0.65, 0.65), yellow)

# Eyes
create_snake_part("Blue Eye", (-1.0, -0.58, 0.8), (0.13, 0.08, 0.13), white)
create_snake_part("Yellow Eye", (0.6, -0.58, -0.2), (0.13, 0.08, 0.13), white)

# 3D Text
bpy.ops.object.text_add(location=(-1.65, -0.2, -2))
text_obj = bpy.context.object
text_obj.data.body = "PYTHON"
text_obj.data.extrude = 0.12
text_obj.data.bevel_depth = 0.025
text_obj.data.align_x = 'CENTER'
text_obj.data.size = 0.75
text_obj.data.materials.append(white)

# Background
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -2.8))
bpy.context.object.data.materials.append(black)

# Lighting
def add_light(location, energy, color, size):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.data.energy = energy
    light.data.color = color
    light.data.shape = 'DISK'
    light.data.size = size
    light.rotation_euler = (0, 0, 0)

add_light((0, -5, 6), 1200, (0.3, 0.5, 1), 5)
add_light((4, 2, 3), 1000, (1, 0.6, 0.1), 4)
add_light((-4, -2, 1), 900, (0.1, 0.3, 1), 3)

# Camera
bpy.ops.object.camera_add(location=(0, -10, 1))
camera = bpy.context.object
camera.rotation_euler = (math.radians(85), 0, 0)
bpy.context.scene.camera = camera

# Render settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100

# Save image
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "//python_3d_logo.png"

bpy.ops.render.render(write_still=True)

print("3D PYTHON LOGO CREATED!")
