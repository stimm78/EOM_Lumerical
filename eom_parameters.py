import numpy as np
# UNIT CONVERSIONS
um = 1e-6
nm = 1e-9

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

material_et = [substrate_material_et, oxide_material_et, wg_material_et, contact_material_et, background_material_et]
material_o = [substrate_material_o, oxide_material_o, wg_material_o, contact_material_o, background_material_o]


'''
SUBSTRATE PARAMS:
substrate_length, substrate_width, substrate_thickness, substrate_z

BOX PARAMS:
box_thickness

WAVEGUIDE PARAMS:
waveguide_bar_thickness, waveguide_core_thickness, waveguide_core_length, waveguide_theta

CLADDING PARAMS:
cladding_thickness

METAL PARAMS:
metal_length, metal_spacing, metal_thickness
'''

''' -- START OF INPUT PARAMETERS -- '''
substrate_length = 50 * um
substrate_width = 20 * um
substrate_thickness = 9 * um 
substrate_z = -9.5 * um

box_thickness = 7 * um 

waveguide_bar_thickness = 700 * nm 
waveguide_core_thickness = 1000 * nm 
waveguide_core_length = 1.8 * um 
waveguide_theta = 30 # ask Ben

cladding_thickness = 900 * nm

metal_left_length = 9.5 * um
metal_center_length = 9.5 * um
metal_right_length = 9.5 * um
metal_spacing = 10 * um
metal_thickness = 1.8 * um

box_length = substrate_length
box_width = substrate_width
box_z = substrate_z + 0.5 * (substrate_thickness + box_thickness)


# CHARGE SIMULATION PARAMS
signal_voltage = 5 # V

# FEEM SIMULATION PARAMS
wavelength = 1.55 * um
num_modes = 20

''' -- END OF INPUT PARAMETERS -- '''

metal_center_x = 0
metal_left_x = metal_center_x - metal_spacing - 0.5 * (metal_center_length + metal_left_length)

waveguide_z = 0
waveguide_length = box_length
waveguide_width = box_width
waveguide_y = box_z + 0.5 * box_thickness # bottom y coordinate
waveguide_x1 = metal_center_x - 0.5 * (metal_center_length + metal_spacing - waveguide_core_length)# 0.5 * (metal_left_x + metal_center_x + waveguide_core_length) # -6.35 * um
waveguide_x2 = waveguide_x1 - waveguide_core_length # left corner of core
waveguide_vtx = np.array([
    [waveguide_x1, waveguide_y + waveguide_bar_thickness],
    [waveguide_x1, waveguide_y + waveguide_core_thickness],
    [waveguide_x2, waveguide_y + waveguide_core_thickness],
    [waveguide_x2, waveguide_y + waveguide_bar_thickness],
    [-waveguide_length * 0.5, waveguide_y + waveguide_bar_thickness],
    [-waveguide_length * 0.5, waveguide_y],
    [waveguide_length * 0.5, waveguide_y],
    [waveguide_length * 0.5, waveguide_y + waveguide_bar_thickness]
])

cladding_z = 0
cladding_length = waveguide_length
cladding_width = waveguide_width
cladding_core_thickness = waveguide_y + waveguide_core_thickness + cladding_thickness
cladding_core_length = waveguide_core_length + 2 * cladding_thickness # conformal
cladding_y = waveguide_y + waveguide_bar_thickness # bottom y coordinate
cladding_x1 = waveguide_x1 + cladding_thickness # right corner of core
cladding_x2 = cladding_x1 - cladding_core_length # left corner of core
cladding_vtx = np.array([
    [cladding_x1, cladding_y + cladding_thickness],
    [cladding_x1, waveguide_y + waveguide_core_thickness + cladding_thickness],
    [cladding_x2, waveguide_y + waveguide_core_thickness + cladding_thickness],
    [cladding_x2, cladding_y + cladding_thickness],
    [-cladding_length * 0.5, cladding_y + cladding_thickness],
    [-cladding_length * 0.5, cladding_y],
    [cladding_length * 0.5, cladding_y],
    [cladding_length * 0.5, cladding_y + cladding_thickness]
])

metal_width = cladding_width
metal_right_x = metal_center_x + metal_spacing + 0.5 * (metal_center_length + metal_right_length)
metal_z = cladding_y + cladding_thickness + 0.5 * metal_thickness

# -- Simulation Region --
simulation_x_span = metal_spacing + metal_center_length # assume centered
simulation_x = 0.5 * (waveguide_x1 + waveguide_x2) # center on waveguide
simulation_z = waveguide_y + waveguide_bar_thickness
simulation_z_span = metal_thickness * 5
