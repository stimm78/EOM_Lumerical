import importlib
import eom_parameters as param
importlib.reload(param)
def add_charge_solver(device):
    """
    Adds CHARGE solver and sets simulation settings.
    CHARGE sweeps over voltage and calculates spatial E-fields -> Pockels effect perturbed index n(V,x,y)
    """
    device.addchargesolver()
    device.addchargemesh()
    device.addelectricalcontact(name = "Left_Ground")
    device.addelectricalcontact(name = "Signal")
    device.addelectricalcontact(name = "Right_Ground")
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
            ("volume solid", "LiNbO3 WG"),
            ("max edge length", 0.01 * param.um)
        ),
        "CHARGE::boundary conditions::Left_Ground": (
            ("bc mode", "steady state"),
            ('sweep type', 'single'),
            ('voltage', 0),
            ("surface type", "solid"),
            ("solid", "Ground Electrode Left")
        ),
        "CHARGE::boundary conditions::Signal": ( 
            ("bc mode", "steady state"),
            ('sweep type', 'range'),
            ('range start', 0),  ('range stop', param.signal_voltage),
            ('range interval', param.signal_step),
            ("surface type", "solid"),
            ("solid", "Signal Electrode"),
            ("outer surface only", 1)
        ),
        "CHARGE::boundary conditions::Right_Ground": (
            ("bc mode", "steady state"),
            ('sweep type', 'single'),
            ('voltage', 0),
            ("surface type", "solid"),
            ("solid", "Ground Electrode Right")
        ),
        "CHARGE::monitor": (
            ("monitor type", "2D Y-Normal"),
            ("x", param.simulation_x), ("y", 0), ("z", param.simulation_z),
            ("x span", param.simulation_x_span), ("z span", param.simulation_z_span)
        )
    }
    for obj in configuration:
        for key, val in configuration[obj]:
            device.setnamed(obj, key, val)