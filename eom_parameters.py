import numpy as np
# UNIT CONVERSIONS
um = 1e-6
nm = 1e-9

'''
SUBSTRATE PARAMS:
substrate_length, substrate_width, substrate_thickness, substrate_z
* Note that length = x axis, width = y axis
'''
substrate_length = 50 * um
substrate_width = 20 * um
substrate_thickness = 9 * um 
substrate_z = -9.5 * um

'''
BOX PARAMS:
box_thickness
'''
box_thickness = 7 * um 

box_length = substrate_length
box_width = substrate_width
box_z = substrate_z + 0.5 * (substrate_thickness + box_thickness)

'''
WAVEGUIDE PARAMS:
waveguide_bar_thickness, waveguide_core_thickness, waveguide_core_length, waveguide_x1 (right corner)
'''
waveguide_bar_thickness = 700 * nm 
waveguide_core_thickness = 1000 * nm 
waveguide_core_length = 1.8 * um 
waveguide_x1 = -6.35 * um

waveguide_z = 0
waveguide_length = box_length
waveguide_width = box_width
waveguide_y = box_z + 0.5 * box_thickness # bottom y coordinate
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

'''
CLADDING PARAMS:
cladding_thickness
'''
cladding_thickness = 900 * nm

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

'''
METAL PARAMS:
metal_length
metal_spacing
metal_thickness
'''
metal_length = 9.5 * um
metal_spacing = 5 * um
metal_thickness = 1.8 * um

metal_width = cladding_width
metal_center_x = 0
metal_right_x = metal_center_x + metal_spacing + metal_length
metal_left_x = metal_center_x - metal_spacing - metal_length
metal_z = cladding_y + cladding_thickness + 0.5 * metal_thickness

# XXTODO: Center waveguide in the middle of two electrodes