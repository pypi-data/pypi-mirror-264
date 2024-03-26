# En __init__.py del paquete que contiene AtomPositionManager
try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del syss

try:
    from sage_lib.IO.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys
    
try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import subprocess
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing subprocess: {str(e)}\n")
    del sys

try:
    import copy
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing copy: {str(e)}\n")
    del sys

class Blender_builder(PartitionManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Constructor method for initializing the beldenr  instance.
        """
        super().__init__(name=name, file_location=file_location)

    def get_blender_str(self, atomPositions, atomLabelsList, uniqueAtomLabels, 
                            atomCount, colors, radii, conection, fog, path,
                            samples, resolution_x, resolution_y, ):
        '''
        atomPositions = { atomPositions }
        atomLabelsList = { atomLabelsList }
        uniqueAtomLabels = {uniqueAtomLabels}
        atomCount = { atomCount }
        colors = { colors }
        radii = { radii }
        conection = {conection}
        '''
        self.blender_script = f"""
import bpy
import random
from mathutils import Vector

def create_object_instance(original, location=(0,0,0), rotation=(0,0,0), scale=(1,1,1)):
    # Create a new linked duplicate (instance) of the original object
    instance = bpy.data.objects.new(name=original.name + "_instance", object_data=original.data)
    instance.location = location
    instance.rotation_euler = rotation
    instance.scale = scale
    bpy.context.collection.objects.link(instance)

    return instance

def align_object_between_points(obj, start_point, end_point):
    # Calculate the direction vector from start to end point
    direction = end_point - start_point
    # Calculate the midpoint
    midpoint = start_point + direction / 2
    obj.location = midpoint
    # Calculate the rotation to align with the direction vector
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = direction.to_track_quat('Z', 'Y')
    # Scale the object to stretch between the two points
    obj.scale[2] = direction.length / 2 # Assuming the cylinder's length aligns with the Z-axis

def setup_scene():
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    sphere_original = {{}}
    cylinder_original = {{}}
    for label in uniqueAtomLabels:
        # Create original sphere and cylinder
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[label])
        sphere_original[label] = bpy.context.object
        bpy.ops.name = f'sphere {{label}}'
        bpy.ops.object.shade_smooth()

        bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=2)
        cylinder_original[label] = bpy.context.object
        bpy.ops.name = f'cylinder {{label}}'
        bpy.ops.object.shade_smooth()

    # Generate sphere instances at random positions
    for i, n in enumerate(atomPositions): # Number of spheres
        loc = (n[0], n[1], n[2])
        sphere_instance = create_object_instance(sphere_original[atomLabelsList[i]], location=loc)

    # Connect sphere instances with cylinder instances
    for [A, B] in conection:
        cylinder_instance_A = create_object_instance( cylinder_original[atomLabelsList[A]] )
        cylinder_instance_B = create_object_instance( cylinder_original[atomLabelsList[B]] )
        
        midpoint = Vector((np.array(atomPositions[A]) + np.array((atomPositions[B]))/2))
        
        align_object_between_points(cylinder_instance_A, Vector(atomPositions[A]), midpoint )
        align_object_between_points(cylinder_instance_B, midpoint, Vector(atomPositions[B]) )

def create_material(name,  base_color, metallic=0.5, specular=0.5, roughness=0.5 ):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = base_color + (1,)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Specular'].default_value = specular
    bsdf.inputs['Roughness'].default_value = roughness

    return material

def setup_lighting():
    # Remove existing lights
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Key light
    bpy.ops.object.light_add(type='AREA', radius=5, location=(0, 10, 10))
    bpy.context.object.data.energy = 1000
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', radius=5, location=(10, -10, 5))
    bpy.context.object.data.energy = 500
    
    # Back light
    bpy.ops.object.light_add(type='AREA', radius=5, location=(-10, -10, 10))
    bpy.context.object.data.energy = 750

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.object
    sun.data.energy = 5 # Adjust as needed

def setup_background(color=(0.05, 0.05, 0.05, 1)):
    # Set the background color
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = color
    bpy.context.scene.render.film_transparent = True

def _add_camera(name, location, look_at_point, scale:str='orthographic'):
    # Create the camera
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = name
    
    if scale == 'orthographic':
        camera.data.type = 'ORTHO'
        camera.data.ortho_scale = ortho_scale  # Controls the size of the orthographic view
    
    # Point the camera to the look_at_point
    direction = look_at_point - Vector(location)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

def setup_cameras(look_at_point):
    distance = 20 # Distance from the center to place cameras
    _add_camera('Camera_X', (distance, 0, 0), look_at_point)
    _add_camera('Camera_Y', (0, distance, 0), look_at_point)
    _add_camera('Camera_Z', (0, 0, distance), look_at_point)

def setup_orthographic_cameras(look_at_point):
    distance = 20  # Distance from the center to place cameras. Adjust based on model size
    # The ortho_scale might need adjustment depending on the size of your molecular model
    ortho_scale = 15
    add_orthographic_camera('Camera_X', (distance, 0, 0), look_at_point, ortho_scale)
    add_orthographic_camera('Camera_Y', (0, distance, 0), look_at_point, ortho_scale)
    add_orthographic_camera('Camera_Z', (0, 0, distance), look_at_point, ortho_scale)

def find_molecular_centroid():
    # Find the centroid of all sphere instances (assuming they represent atoms)
    return Vector((0,0,0))

def setup_compositing_nodes():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    # Clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
    
    # Create nodes for post-processing effects
    render_layers = tree.nodes.new('CompositorNodeRLayers')
    viewer = tree.nodes.new('CompositorNodeViewer') # To view the effect directly in Blender
    comp = tree.nodes.new('CompositorNodeComposite') # To ensure output is rendered

    # Example of adding a glare effect
    glare = tree.nodes.new('CompositorNodeGlare')
    glare.glare_type = 'FOG_GLOW' # Experiment with different types like 'FOG_GLOW', 'SIMPLE_STAR', etc.
    glare.mix = 0.1 # Blend with the original image
    glare.threshold = 0.8 # Intensity threshold for the glare effect
    
    # Connect the nodes
    tree.links.new(render_layers.outputs[0], glare.inputs[0]) # Connect Render Layers to Glare
    tree.links.new(glare.outputs[0], viewer.inputs[0]) # Connect Glare to Viewer
    tree.links.new(glare.outputs[0], comp.inputs[0]) # Ensure the output is connected to Composite for rendering

    # Add more effects as needed (e.g., color correction, depth of field, vignette)


def high_quality_render_settings(engine:str='CYCLES', samples:int={samples}, resolution_x:int={resolution_x}, resolution_y:int={resolution_y}, use_denoising:bool=True):
    bpy.context.scene.render.engine = str(engine) # Use Cycles for better quality
    bpy.context.scene.cycles.samples = samples # Increase for higher quality but longer render times
    bpy.context.scene.render.resolution_x = resolution_x # Increase resolution
    bpy.context.scene.render.resolution_y = resolution_y

    if use_denoising:
        bpy.context.scene.cycles.use_denoising = True # Enable denoising
        
        # Enable denoising
        bpy.context.scene.cycles.use_denoising = True
        
        # Advanced denoising settings for finer control
        bpy.context.scene.cycles.denoising_store_passes = True
        #bpy.context.scene.view_layers["View Layer"].cycles.use_denoising = True
        
        # Opt-in for AI-accelerated denoiser (requires NVIDIA OptiX)
        bpy.context.scene.cycles.denoiser = 'OPTIX'  # Alternatives: 'NLM', 'OPENIMAGEDENOISE'
    
        # Set denoising after rendering for more control
        #bpy.context.scene.view_layers["View Layer"].cycles.denoising_prefilter = 'ACCURATE'
        #bpy.context.scene.view_layers["View Layer"].cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        
        # Adjust as per the complexity of the scene; for detailed models, consider increasing samples further.
        #bpy.context.scene.cycles.preview_samples = 32  # Samples for viewport preview
        
        # Enable Adaptive Sampling for efficiency
        #bpy.context.scene.cycles.use_adaptive_sampling = True
        #bpy.context.scene.cycles.adaptive_threshold = 0.01  # Lower threshold for higher quality

def add_fog():
    # Crea un objeto de volumen para la neblina
    bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 0))  # Ajusta el tamaño según sea necesario
    cube = bpy.context.object
    cube.name = 'FogVolume'

    # Crea un nuevo material volumétrico
    mat_fog = bpy.data.materials.new(name="FogMaterial")
    cube.data.materials.append(mat_fog)
    mat_fog.use_nodes = True
    nodes = mat_fog.node_tree.nodes

    # Limpia los nodos predeterminados
    for node in nodes:
        nodes.remove(node)

    # Añade un nodo de Principled Volume
    volume_shader = nodes.new(type='ShaderNodeVolumePrincipled')
    volume_shader.location = 0, 0

    # Añade un nodo de salida de material
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = 200, 0

    # Añade un nodo de textura de ruido para variar la densidad de la neblina
    noise_tex = nodes.new(type='ShaderNodeTexNoise')
    noise_tex.location = -200, 0
    noise_tex.inputs['Scale'].default_value = 5.0  # Ajusta para más o menos detalle en la neblina

    # Conecta los nodos
    links = mat_fog.node_tree.links
    links.new(noise_tex.outputs['Fac'], volume_shader.inputs['Density'])
    links.new(volume_shader.outputs['Volume'], output_node.inputs['Volume'])

    # Ajusta la densidad de la neblina (baja para empezar, aumenta según sea necesario)
    volume_shader.inputs['Density'].default_value = 0.01

    # Añade un nodo Math para ajustar la influencia de la textura de ruido en la densidad
    math_node = nodes.new(type='ShaderNodeMath')
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 0.08  # Ajusta este valor para controlar la densidad general
    math_node.location = -400, 0

    # Conecta el nodo de ruido al nodo Math y luego al shader de volumen
    links.new(noise_tex.outputs['Fac'], math_node.inputs[0])
    links.new(math_node.outputs[0], volume_shader.inputs['Density'])

atomPositions = { atomPositions.tolist() }
atomLabelsList = { atomLabelsList.tolist() }
uniqueAtomLabels = { uniqueAtomLabels.tolist() }
atomCount = { atomCount }
colors = { colors }
radii = { radii }
conection = {conection}

setup_scene()

material_sphere = {{label: create_material('SphereMaterial', colors[label]) for label in uniqueAtomLabels }}# Red
material_cylinder = {{label: create_material('CylinderMaterial', colors[label]) for label in uniqueAtomLabels }}# Blue

for obj in bpy.context.scene.objects:
    for label in uniqueAtomLabels:
        if "sphere" in obj.name.lower() and 'label'+label.lower() in obj.name.lower():
            if obj.data.materials:
                obj.data.materials[0] = material_sphere[label]
            else:
                obj.data.materials.append( material_sphere[label] )
            break
        
        elif "cylinder" in obj.name.lower() and 'label'+label.lower() in obj.name.lower():
            if obj.data.materials:
                obj.data.materials[0] = material_cylinder[label]
            else:
                obj.data.materials.append(material_cylinder[label])
            break


for label in uniqueAtomLabels:
    sphere_original[label].hide_render = True
    sphere_original.hide_viewport[label] = True

    cylinder_original[label].hide_render = True
    cylinder_original.hide_viewport[label] = True

setup_lighting()
setup_background() # rgay by defoault 
setup_orthographic_cameras(find_molecular_centroid())
setup_compositing_nodes()

high_quality_render_settings()

if {fog}: add_fog()

def render_scene(camera_name, output_path)
    # Set the active camera
    bpy.context.scene.camera = bpy.data.objects[camera_name]

    # Set render settings
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # or any other format
    bpy.context.scene.render.filepath = output_path

    # Render the scene
    bpy.ops.render.render(write_still=True)

# Render and save the image from each camera
cameras = ['Camera_X', 'Camera_Y', 'Camera_Z']
for camera in cameras:
    output_path = f"{{{path}}}_{{camera}}.png"  # Update the output path
    render_scene(camera, output_path)

"""
        return self.blender_script

    def handleBLENDER(self, values:list ):
        """
        Handle molecular dynamics analysis based on specified values.

        Args:
            values (list): List of analysis types to perform.
        """
        MDA_data = {}

        for plot in values:

            for container_index, container in enumerate(self.containers):
                if plot.upper() == 'XYZ':
                    blender_str = self.get_blender_str(
                        atomPositions = container.AtomPositionManager.atomPositions, 
                        atomLabelsList =  container.AtomPositionManager.atomLabelsList, 
                        uniqueAtomLabels =  container.AtomPositionManager.uniqueAtomLabels, 
                        atomCount =  container.AtomPositionManager.atomCount, 
                        colors = container.AtomPositionManager.element_colors, 
                        radii = container.AtomPositionManager.covalent_radii, 
                        conection =  container.AtomPositionManager.get_connection_list(),
                        fog = values[plot]['fog'], 
                        path = 'blender_plot_',
                        resolution_x = values[plot]['resolution_x'], 
                        resolution_y = values[plot]['resolution_y'], 
                        samples = values[plot]['samples'], 
                        )
                    
                    blender_script_name = f'blender_script_{container_index}.py'
                    with open(blender_script_name, 'w') as file:
                        file.write(blender_str)

                    if values[plot]['verbose']:
                        print(f'>> Blender script save to {blender_script_name} ')

                    if values[plot]['render']:
                        command = f'blender -b -P {blender_script_name}'
                        process = subprocess.run(command, shell=True, check=True)

                        if values[plot]['verbose']:
                            print(f'>> DONE :: Render container {container_index} finish ')
