import importlib
import eom_parameters as param
importlib.reload(param)

def add_materials(device):
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

    device.addrect(name='substrate')
    device.addrect(name='box')
    device.addpoly(name='waveguide')
    device.addpoly(name='cladding')
    device.addrect(name='metal_left')
    device.addrect(name='metal_center')
    device.addrect(name='metal_right')

    '''
    GENERAL CONFIG
    '''
    configuration = {
    "substrate": (
        ("x", 0), ("x span", param.substrate_length),
        ("y", 0), ("y span", param.substrate_width),
        ("z", param.substrate_z), ("z span", param.substrate_thickness),
        ("material", param.substrate_material_et)
    ),
    "box": (
        ("x", 0), ("x span", param.box_length),
        ("y", 0), ("y span", param.box_width),
        ("z", param.box_z), ("z span", param.box_thickness),
        ("material", param.oxide_material_et)
    ),
    "waveguide": (
        ("z", param.waveguide_z), ("z span", param.waveguide_width),
        ("vertices", param.waveguide_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("material", param.wg_material_et)
    ),
    "cladding": (
        ("z", param.cladding_z), ("z span", param.cladding_width),
        ("vertices", param.cladding_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("material", param.oxide_material_et)
    ),
    "metal_left": (
        ("x", param.metal_left_x), ("x span", param.metal_left_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", param.contact_material_et)
    ),
    "metal_center": (
        ("x", 0), ("x span", param.metal_center_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", param.contact_material_et)
    ),
    "metal_right": (
        ("x", param.metal_right_x), ("x span", param.metal_right_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", param.contact_material_et)
    ),
}

    # Waveguide has higher priority when taking the union geometry
    device.setnamed("waveguide", "mesh order", 2)
    device.setnamed("cladding", "mesh order", 3)

    for obj in configuration:
        for key, val in configuration[obj]:
            device.setnamed(obj, key, val)
    
def simulation_region(device):
    pass

def delete_all(device):
    device.deleteall()