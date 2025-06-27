import importlib
from collections import defaultdict
import eom_parameters as param
importlib.reload(param)

# Global materials
substrate_material_et = "Si (Silicon)"
substrate_material_o = "Si (Silicon) - Palik"
oxide_material_et = "SiO2 (Glass) - Sze"
oxide_material_o = "SiO2 (Glass) - Palik"
wg_material_et = "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)"
wg_material_o = "Dielectric"
wg_index = 2
contact_material_et = "Au (Gold) - CRC"
contact_material_o = "Au (Gold) - CRC"
background_material_et = "Air"
background_material_o = "etch"

material_et = [substrate_material_et, oxide_material_et, wg_material_et, contact_material_et]
material_o = [substrate_material_o, oxide_material_o, wg_material_o, contact_material_o]

# Color depends on ordering in the list
def add_materials(device):
    for i, material in enumerate(material_et):    
        device.addmodelmaterial()
        device.setnamed("materials::New Material","name", material)
        device.addmaterialproperties("CT", material)
        device.select("materials::" + material);
        device.addmaterialproperties("EM", material_o[i])

        if(material_o[i] == wg_material_o):
            device.setnamed("materials::" + material + "::"+ wg_material_o,
                            "refractive index",wg_index)

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
        ("material", substrate_material_et)
    ),
    "box": (
        ("x", 0), ("x span", param.box_length),
        ("y", 0), ("y span", param.box_width),
        ("z", param.box_z), ("z span", param.box_thickness),
        ("material", oxide_material_et)
    ),
    "waveguide": (
        ("z", param.waveguide_z), ("z span", param.waveguide_width),
        ("vertices", param.waveguide_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("material", wg_material_et)
    ),
    "cladding": (
        ("z", param.cladding_z), ("z span", param.cladding_width),
        ("vertices", param.cladding_vtx),
        ("first axis", "x"), ("rotation 1", 90),
        ("material", oxide_material_et)
    ),
    "metal_left": (
        ("x", param.metal_left_x), ("x span", param.metal_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", contact_material_et)
    ),
    "metal_center": (
        ("x", 0), ("x span", param.metal_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", contact_material_et)
    ),
    "metal_right": (
        ("x", param.metal_right_x), ("x span", param.metal_length),
        ("y", 0), ("y span", param.metal_width),
        ("z", param.metal_z), ("z span", param.metal_thickness),
        ("material", contact_material_et)
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