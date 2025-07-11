import numpy as np
import math
# UNIT CONVERSIONS
um = 1e-6
nm = 1e-9

def sweep_geometry(cladding_thickness_val, metal_spacing_val):
    global substrate_length, substrate_width, substrate_thickness, substrate_z
    global box_thickness

    global waveguide_bar_thickness, waveguide_core_thickness
    global waveguide_core_length, waveguide_theta

    global cladding_thickness

    global metal_left_length, metal_center_length, metal_right_length
    global metal_spacing, metal_thickness

    global signal_voltage, signal_step

    global wavelength, num_modes, n

    global box_length, box_width, box_z
    global waveguide_length, waveguide_width, waveguide_z
    global waveguide_x_center, waveguide_x1, waveguide_x2
    global waveguide_y_bottom, waveguide_y_bar_top, waveguide_y_core_top
    global waveguide_vtx, delta_x

    global cladding_z, cladding_core_length, cladding_x1, cladding_x2
    global cladding_length, cladding_width
    global cladding_y_bar_top, cladding_y_bar_bottom, cladding_y_core_top
    global cladding_vtx, delta_x_clad

    global metal_center_x, metal_left_x, metal_right_x, metal_z, metal_width

    global simulation_x_span, simulation_x, simulation_z, simulation_z_span
    # SUBSTRATE PARAMS: substrate_length, substrate_width, substrate_thickness, substrate_z
    substrate_length = 50 * um
    substrate_width = 20 * um
    substrate_thickness = 9 * um 
    substrate_z = -9.5 * um

    # BOX PARAMS: box_thickness
    box_thickness = 4.7 * um 

    # WAVEGUIDE PARAMS: waveguide_bar_thickness, waveguide_core_thickness, waveguide_core_length, waveguide_theta
    waveguide_bar_thickness = 300 * nm 
    waveguide_core_thickness = 600 * nm 
    waveguide_theta = 60 * (math.pi / 180)
    waveguide_core_length = 2 * (waveguide_core_thickness - waveguide_bar_thickness) / math.tan(waveguide_theta) + 1 * um

    # CLADDING PARAMS: cladding_thickness
    cladding_thickness = cladding_thickness_val

    # METAL PARAMS: metal_length, metal_spacing, metal_thickness
    metal_left_length = 9.5 * um
    metal_center_length = 9.5 * um
    metal_right_length = 9.5 * um
    metal_spacing = metal_spacing_val
    metal_thickness = 0.3 * um

    # CHARGE SIMULATION PARAMS
    signal_voltage = 5 # V
    signal_step = 0.5

    # FEEM SIMULATION PARAMS
    wavelength = 1.550 * um # ** MUST CHANGE LiNbO3 INDEX ACCORDINGLY 
    num_modes = 20
    n = 2.02 # mode search near n

    ''' -- END OF INPUT PARAMETERS -- '''

    box_length = substrate_length
    box_width = substrate_width
    box_z = substrate_z + 0.5 * (substrate_thickness + box_thickness)

    metal_center_x = 0
    metal_left_x = metal_center_x - metal_spacing - 0.5 * (metal_center_length + metal_left_length)

    waveguide_z = 0
    waveguide_length = box_length
    waveguide_width = box_width

    # Waveguide core center under metal gap
    waveguide_x_center = metal_center_x - 0.5 * (metal_center_length + metal_spacing)

    # Core x edges
    waveguide_x1 = waveguide_x_center + 0.5 * waveguide_core_length  # right edge
    waveguide_x2 = waveguide_x_center - 0.5 * waveguide_core_length  # left edge

    # y positions
    waveguide_y_bottom = box_z + 0.5 * box_thickness
    waveguide_y_bar_top = waveguide_y_bottom + waveguide_bar_thickness
    waveguide_y_core_top = waveguide_y_bottom + waveguide_core_thickness

    # Slope compensation
    delta_x = (waveguide_core_thickness - waveguide_bar_thickness) / math.tan(waveguide_theta)

    # Vertex array
    waveguide_vtx = np.array([
        [waveguide_x1, waveguide_y_bar_top],
        [waveguide_x1 - delta_x, waveguide_y_core_top],
        [waveguide_x2 + delta_x, waveguide_y_core_top],
        [waveguide_x2, waveguide_y_bar_top],
        [-waveguide_length * 0.5, waveguide_y_bar_top],
        [-waveguide_length * 0.5, waveguide_y_bottom],
        [ waveguide_length * 0.5, waveguide_y_bottom],
        [ waveguide_length * 0.5, waveguide_y_bar_top]
    ])

    # Core dimensions
    cladding_z = waveguide_z
    cladding_core_length = waveguide_core_length + 2 * cladding_thickness
    cladding_x1 = waveguide_x_center + 0.5 * cladding_core_length
    cladding_x2 = waveguide_x_center - 0.5 * cladding_core_length
    cladding_length = waveguide_length
    cladding_width = waveguide_width

    # Y coordinates
    waveguide_y_bottom = box_z + 0.5 * box_thickness
    waveguide_y_bar_top = waveguide_y_bottom + waveguide_bar_thickness
    waveguide_y_core_top = waveguide_y_bottom + waveguide_core_thickness

    cladding_y_bar_top = waveguide_y_bar_top + cladding_thickness
    cladding_y_bar_bottom = waveguide_y_bar_top
    cladding_y_core_top = waveguide_y_core_top + cladding_thickness
    delta_x_clad = (cladding_y_core_top - cladding_y_bar_top) / np.tan(waveguide_theta)

    cladding_vtx = np.array([
        [cladding_x1, cladding_y_bar_top],
        [cladding_x1 - delta_x_clad, cladding_y_core_top],
        [cladding_x2 + delta_x_clad, cladding_y_core_top],
        [cladding_x2, cladding_y_bar_top],
        [-cladding_length * 0.5, cladding_y_bar_top],
        [-cladding_length * 0.5, cladding_y_bar_bottom],
        [ cladding_length * 0.5, cladding_y_bar_bottom],
        [ cladding_length * 0.5, cladding_y_bar_top]
    ])

    metal_right_x = metal_center_x + metal_spacing + 0.5 * (metal_center_length + metal_right_length)
    metal_z = cladding_y_bar_top + 0.5 * metal_thickness
    metal_width = cladding_width

    # metal_right_x = metal_center_x + metal_spacing + 0.5 * (metal_center_length + metal_right_length)
    # metal_z = waveguide_y_bar_top + 0.5 * metal_thickness

    # -- Simulation Region --
    simulation_x_span = 2.5 * metal_spacing + 2 * metal_center_length # assume centered
    simulation_x = 0.5 * (waveguide_x1 + waveguide_x2) # center on waveguide
    simulation_z = waveguide_y_core_top
    simulation_z_span = (waveguide_bar_thickness + cladding_thickness + metal_thickness) * 2

