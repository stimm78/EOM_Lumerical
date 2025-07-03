import importlib
import eom_parameters as param
importlib.reload(param)
'''
FEEM solves for TE0 mode at all voltages and evaluates modulator performance metrics (mode profile, modulator loss and efficiency)
'''
def add_feem_solver(device):
    device.addfeemsolver()
    device.addfeemmesh()
    device.addpec()
    device.addpml()
    device.addimportnk()

    configuration = {
        "FEEM": (
            ("edges per wavelength", 2),
            ("wavelength", param.wavelength),
            ("number of trial modes", param.num_modes),
            ("polynomial order", 2),
            ("simulation region", "simulation region")
        ),
        "FEEM::mesh": (
            ("geometry type", "volume"), 
            ("volume type", "solid"),
            ("volume solid", "waveguide"),
            ("max edge length", 0.01 * param.um)
        ),
        "simulation region": (
            ("dimension", "2D Y-Normal"),
            ("x", param.simulation_x), ("y", 0), ("z", param.simulation_z),
            ("x span", param.simulation_x_span), ("z span", param.simulation_z_span),
            # ("background material", param.background_material_o)
        ),
        "FEEM::boundary conditions::PEC": (
            ("surface type", "simulation region"),
            ("x min", 1),
            ("x max", 1),
            ("y min", 1),
            ("y max", 1),
            ("z min", 1),
            ("z max", 1)
        ),
        "FEEM::boundary conditions::PML": (
            ("sigma", 5),
        ),
        # "FEEM::nk import": (
        #     ("enabled", True),
        #     ("volume type", "solid"),
        #     ("volume solid", "waveguide"),
        #     ("selected attribute", "nk")
        # )
    }
    
    for obj in configuration:
        for key, val in configuration[obj]:
            device.setnamed(obj, key, val) 