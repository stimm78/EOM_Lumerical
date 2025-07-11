import numpy as np
import math

# -------------------------
# UNIT CONVERSIONS
# -------------------------
um = 1e-6
nm = 1e-9

''' -- START OF INPUT PARAMETERS -- '''
# -------------------------
# MATERIAL DEFINITIONS
# -------------------------
# "et" refers to electrical/thermal, "o" refers to optical
substrate_material_et = "Si (Silicon)"
substrate_material_o = "Si (Silicon) - Palik"
oxide_material_et = "SiO2 (Glass) - Sze"
oxide_material_o = "SiO2 (Glass) - Palik"
wg_material_et = "LiNbO3 semiconductor - X/Y cut (Lithium Niobate)"
wg_material_o = "Dielectric" # Custom input for LiNbO3
wg_index = 2.21 # Sets dielectric (LiNbO3) index
contact_material_et = "Au (Gold) - CRC"
contact_material_o = "Au (Gold) - CRC"
background_material_et = "Air"
background_material_o = "etch"
material_et = [substrate_material_et, oxide_material_et, wg_material_et, contact_material_et, background_material_et]
material_o = [substrate_material_o, oxide_material_o, wg_material_o, contact_material_o, background_material_o]

# -------------------------
# SUBSTRATE AND BOX
# -------------------------
substrate_length = 50 * um
substrate_width = 20 * um
substrate_thickness = 9 * um 
substrate_z = -9.5 * um
box_thickness = 4.7 * um # Box is the oxide layer above the bottom layer substrate

# -------------------------
# WAVEGUIDE
# -------------------------
waveguide_bar_thickness = 350 * nm 
waveguide_core_thickness = 700 * nm 
waveguide_theta = math.radians(60)

# -------------------------
# CLADDING
# -------------------------
cladding_thickness = 800 * nm

# -------------------------
# METAL
# -------------------------
metal_left_length = 9.5 * um
metal_center_length = 9.5 * um
metal_right_length = 9.5 * um
metal_spacing = 3 * um
metal_thickness = 0.3 * um

# -------------------------
# SIMULATION SETTINGS
# -------------------------
signal_voltage = 5      
signal_step = 0.5       # Voltage sweep 0 to signal_voltage with step size signal_step
wavelength = 1.55 * um  # Optical simulation wavelength
num_modes = 20          # FEEM setting to search for TE mode
n = 2.02                # Index near which to search for modes

''' -- END OF INPUT PARAMETERS -- '''

# -------------------------
# GEOMETRY DERIVED VALUES
# -------------------------
box_length = substrate_length
box_width = substrate_width
box_z = substrate_z + 0.5 * (substrate_thickness + box_thickness)

metal_center_x = 0
metal_left_x = metal_center_x - metal_spacing - 0.5 * (metal_center_length + metal_left_length)

waveguide_z = 0
waveguide_length = box_length
waveguide_width = box_width
waveguide_core_length = 2 * (waveguide_core_thickness - waveguide_bar_thickness) / math.tan(waveguide_theta) + 1 * um

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

# -- Simulation Region --
simulation_x_span = 2.5 * metal_spacing + 2 * metal_center_length # assume centered
simulation_x = 0.5 * (waveguide_x1 + waveguide_x2) # center on waveguide
simulation_z = waveguide_y_core_top
simulation_z_span = (waveguide_bar_thickness + cladding_thickness + metal_thickness) * 2


def sweep_geometry(cladding_thickness_val, metal_spacing_val):
    """Return geometry based on cladding_thickness and metal_spacing while preserving global defaults."""
    cladding_thickness = cladding_thickness_val
    metal_spacing = metal_spacing_val

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

