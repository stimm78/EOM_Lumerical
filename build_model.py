import importlib
import eom_parameters as param
importlib.reload(param)

def run_sweep(clad_val, space_val):
    param.sweep_geometry(clad_val, space_val)

def add_materials(device):
    '''
    Adds materials specified in eom_parameters.py to the model
    '''
    for i, material in enumerate(param.material_et):    
        device.addmodelmaterial()
        device.setnamed("materials::New Material","name", material)
        device.addmaterialproperties("CT", material)
        device.select("materials::" + material);
        device.addmaterialproperties("EM", param.material_o[i])

        if(param.material_o[i] == param.wg_material_o):
            device.setnamed("materials::" + material + "::"+ param.wg_material_o,
                            "refractive index", param.wg_index)

# Draws geometry of eom
def draw_eom(device):
    '''
    Draws geometry with parameters specified in eom_parameters.py
    '''
    device.addrect(name='LiNbO3 Handle')
    device.addrect(name='SiO2 Substrate')
    device.addpoly(name='LiNbO3 WG')
    device.addpoly(name='Cladding')
    device.addrect(name='Ground Electrode Left')
    device.addrect(name='Signal Electrode')
    device.addrect(name='Ground Electrode Right')
    configuration = {
    "LiNbO3 Handle": (
        ("x", 0), ("x span", param.substrate_length),
        ("y", 0), ("y span", param.substrate_width),
        ("z", param.substrate_z), ("z span", param.substrate_thickness),
        ("preserve surfaces", 1),
        ("material", param.substrate_material_et)
    ),
    "SiO2 Substrate": (
        ("x", 0), ("x span", param.box_length),
        ("y", 0), ("y span", param.box_width),
        ("z", param.box_z), ("z span", param.box_thickness),
        ("preserve surfaces", 1),
        ("material", param.oxide_material_et)
    ),
    "LiNbO3 WG": (
        ("z", param.waveguide_z), ("z span", param.waveguide_width),
        ("vertices", param.waveguide_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("preserve surfaces", 1),
        ("material", param.wg_material_et)
    ),
    "Cladding": (
        ("z", param.cladding_z), ("z span", param.cladding_width),
        ("vertices", param.cladding_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("material", param.oxide_material_et)
    ),
    "Ground Electrode Left": (
        ("x", param.metal_left_x), ("x span", param.metal_left_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("preserve surfaces", 1),
        ("material", param.contact_material_et)
    ),
    "Signal Electrode": (
        ("x", 0), ("x span", param.metal_center_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("preserve surfaces", 1),
        ("material", param.contact_material_et)
    ),
    "Ground Electrode Right": (
        ("x", param.metal_right_x), ("x span", param.metal_right_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("preserve surfaces", 1),
        ("material", param.contact_material_et)
    ),
}

    # Waveguide has higher priority when taking the union geometry, necessary for material settings
    device.setnamed("LiNbO3 WG", "mesh order", 2)
    device.setnamed("Cladding", "mesh order", 3)

    for obj in configuration:
        for key, val in configuration[obj]:
            device.setnamed(obj, key, val)