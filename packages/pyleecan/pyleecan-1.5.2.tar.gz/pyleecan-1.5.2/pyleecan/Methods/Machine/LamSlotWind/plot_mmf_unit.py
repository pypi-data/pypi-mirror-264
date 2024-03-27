import matplotlib.pyplot as plt
from numpy import min as np_min, max as np_max


from ....Functions.Plot import dict_2D
from ....definitions import config_dict
from ....Functions.Plot.set_plot_gui_icon import set_plot_gui_icon

PHASE_COLORS = config_dict["PLOT"]["COLOR_DICT"]["PHASE_COLORS"]


def plot_mmf_unit(self, save_path=None, is_show_fig=False):
    """Plot the winding unit mmf as a function of space

    Parameters
    ----------
    self : LamSlotWind
        an LamSlotWind object
    save_path : str
        File path to save the figure
    is_show_fig : bool
        To call show at the end of the method

    Returns
    -------
    fig : Matplotlib.figure.Figure
        Figure containing the plot
    """

    name = ""
    if self.parent is not None and self.parent.name not in [None, ""]:
        name += self.parent.name + " "
    if self.is_stator:
        name += "Stator "
    else:
        name += "Rotor "

    # Compute the winding function and mmf
    qs = self.winding.qs
    p = self.get_pole_pair_number()
    MMF_U, WF = self.comp_mmf_unit(Nt=1, Na=400 * p)

    color_list = config_dict["PLOT"]["COLOR_DICT"]["COLOR_LIST"][:qs]

    fig, axs = plt.subplots(2, 1, tight_layout=True, figsize=(8, 8))

    dict_2D_0 = dict_2D.copy()
    dict_2D_0["color_list"] = color_list + ["k"]

    WF.plot_2D_Data(
        "angle{°}",
        "phase[]",
        data_list=[MMF_U],
        fig=fig,
        ax=axs[0],
        is_show_fig=is_show_fig,
        win_title=name + "phase MMF",
        **dict_2D_0,
    )

    dict_2D_0["color_list"] = [color_list[0], "k"]

    r_max = 100
    WF.plot_2D_Data(
        "wavenumber=[0," + str(r_max) + "]",
        data_list=[MMF_U],
        fig=fig,
        ax=axs[1],
        is_show_fig=is_show_fig,
        win_title=name + "phase MMF FFT",
        save_path=save_path,
        **dict_2D_0,
    )
    set_plot_gui_icon()

    return fig
