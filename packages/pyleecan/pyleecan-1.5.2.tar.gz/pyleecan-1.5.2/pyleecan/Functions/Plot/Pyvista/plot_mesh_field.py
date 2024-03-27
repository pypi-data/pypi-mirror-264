from numpy import real

from ....definitions import config_dict

COLOR_MAP = config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"]


def plot_mesh_field(
    pv_plotter,
    sargs,
    field_name,
    clim=None,
    mesh_pv=None,
    field=None,
    phase=1,
    colormap=COLOR_MAP,
):
    mesh_pv[field_name] = real(field * phase)
    mesh_field = mesh_pv

    pv_plotter.add_mesh(
        mesh_field,
        scalars=field_name,
        show_edges=False,
        cmap=colormap,
        clim=clim,
        scalar_bar_args=sargs,
    )
