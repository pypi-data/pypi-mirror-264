import matplotlib.pyplot as plt
from numpy import pi, exp

from ....Classes.Arc1 import Arc1
from ....Classes.SlotW22 import SlotW22
from ....Classes.Segment import Segment
from ....definitions import config_dict
from ....Functions.Plot import (
    ARROW_COLOR,
    ARROW_WIDTH,
    MAIN_LINE_COLOR,
    MAIN_LINE_STYLE,
    MAIN_LINE_WIDTH,
    P_FONT_SIZE,
    SC_FONT_SIZE,
    SC_LINE_COLOR,
    SC_LINE_STYLE,
    SC_LINE_WIDTH,
    TEXT_BOX,
    plot_quote,
)
from ....Methods import ParentMissingError

MAGNET_COLOR = config_dict["PLOT"]["COLOR_DICT"]["MAGNET_COLOR"]


def plot_schematics_scr(
    self,
    is_default=False,
    is_add_schematics=True,
    is_add_main_line=True,
    save_path=None,
    is_show_fig=True,
    fig=None,
    ax=None,
):
    """Plot the schematics of the short circuit ring

    Parameters
    ----------
    self : LamSquirrelCage
        A LamSquirrelCage object
    is_default : bool
        True: plot default schematics, else use current lamination values
    is_add_schematics : bool
        True to display the schematics information (Hscr, Lscr...)
    is_add_main_line : bool
        True to display "main lines" (dotted lines and Z axis)
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        To call show at the end of the method
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        Axis on which to plot the data

    Returns
    -------
    fig : Matplotlib.figure.Figure
        Figure containing the plot
    ax : Matplotlib.axes.Axes object
        Axis containing the plot
    """

    # Use some default parameter
    if is_default:
        lam = type(self)(
            is_stator=False,
            is_internal=True,
            Rint=0,
            Rext=0.25,
            L1=1,
            Hscr=0.15,
            Lscr=0.1,
        )
        lam.slot = SlotW22(Zs=12, H0=0.02, H2=0.05)
        lam.winding.Lewout = 0.1
        lam.plot_schematics_scr(
            is_default=False,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            save_path=save_path,
            is_show_fig=is_show_fig,
            fig=fig,
            ax=ax,
        )
    else:
        # Getting the main plot
        fig, ax = self.plot_side(is_show_fig=False, fig=fig, ax=ax)
        Lt = self.comp_length()
        Hs = self.slot.comp_height()
        Ha = self.slot.comp_height_active()
        Ho = Hs - Ha
        Le = self.winding.Lewout
        Lscr = self.Lscr
        Hscr = self.Hscr

        # Adding schematics
        if is_add_schematics:
            # Rext
            line = Segment(Lt / 2 - Lt / 5, Lt / 2 - Lt / 5 + 1j * self.Rext)
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="Rext",
                offset_label=-Le * 1.05,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # Lewout
            Zbar1 = Lt / 2 + 1j * (self.Rext - Hs + Ha)
            Zbar2 = Lt / 2 + Le + 1j * (self.Rext - Hs + Ha)
            Zlim1 = Zbar1 + 1j * Hs
            Zlim2 = Zbar2 + 1j * Hs
            plot_quote(
                Zbar1,
                Zlim1,
                Zlim2,
                Zbar2,
                offset_label=1j * Le * 0.4 - Le * 0.7,
                fig=fig,
                ax=ax,
                label="Lewout",
            )
            # Lscr
            ZL1 = Lt / 2 + Le + 1j * (self.Rext - Hs + Ha / 2 + Hscr / 2)
            ZL2 = Lt / 2 + Le + Lscr + 1j * (self.Rext - Hs + Ha / 2 + Hscr / 2)
            Zlim1 = ZL1 + 1j * Hs
            Zlim2 = ZL2 + 1j * Hs
            plot_quote(
                ZL1,
                Zlim1,
                Zlim2,
                ZL2,
                offset_label=1j * Le * 0.4 - Le * 0.3,
                fig=fig,
                ax=ax,
                label="Lscr",
            )
            # Hscr
            line = Segment(ZL2, ZL2 - 1j * Hscr)
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="Hscr",
                offset_label=Le * 0.3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

        if is_add_main_line:
            # Ox axis
            line = Segment(0, Lt + Le + Lscr)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Hscr lines
            line = Segment(ZL1 - 1j * Hscr, ZL2 - 1j * Hscr)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            line = Segment(ZL1.conjugate() + 1j * Hscr, ZL2.conjugate() + 1j * Hscr)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )

        ax.axis("equal")
        ax.set_xlim(Lt / 4, (Lt / 2 + Le + Lscr) * 1.1)
        # ax.set_ylim(-self.Rext, self.Rext)
        manager = plt.get_current_fig_manager()
        if manager is not None:
            manager.set_window_title(type(self).__name__ + " Schematics")
        ax.set_title("")
        ax.get_legend().remove()
        ax.set_axis_off()

        # Save / Show
        if save_path is not None:
            fig.savefig(save_path)
            plt.close(fig=fig)

        if is_show_fig:
            fig.show()
        return fig, ax
