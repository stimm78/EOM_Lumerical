import importlib
import eom_parameters as param
importlib.reload(param)

def add_charge_solver(device):
    device.addchargesolver()
    device.addchargemesh()
    device.addelectricalcontact(name = "metal_left")
    device.addelectricalcontact(name = "metal_center")
    device.addelectricalcontact(name = "metal_right")

    device.addefieldmonitor(name = "monitor")

    min_edge_length = 0.05 * param.um
    max_edge_length = 1 * param.um
    configuration = {
        "simulation region": (
            ("dimension", "2D Y-Normal"),
            ("x", param.simulation_x), ("y", 0), ("z", param.simulation_z),
            ("x span", param.simulation_x_span), ("z span", param.simulation_z_span),
            ("background material", param.background_material_et)
        ),
        "CHARGE": (
            ("min edge length", min_edge_length), ("max edge length", max_edge_length)
        ),
        "CHARGE::mesh": (
            ("geometry type", "volume"), 
            ("volume type", "solid"),
            ("volume solid", "waveguide"),
            ("max edge length", 0.01 * param.um)
        ),
        "CHARGE::boundary conditions::metal_left": (
            ("bc mode", "steady state"),
            ('sweep type', 'single'),
            ('voltage', 0),
            ("surface type", "solid"),
            ("solid", "metal_left")
        ),
        "CHARGE::boundary conditions::metal_center": (
            ("bc mode", "steady state"),
            ('sweep type', 'single'),
            ('voltage', param.signal_voltage),
            ("surface type", "solid"),
            ("solid", "metal_center")
        ),
        "CHARGE::boundary conditions::metal_right": (
            ("bc mode", "steady state"),
            ('sweep type', 'single'),
            ('voltage', 0),
            ("surface type", "solid"),
            ("solid", "metal_right")
        )

    }
    for obj in configuration:
            for key, val in configuration[obj]:
                device.setnamed(obj, key, val)