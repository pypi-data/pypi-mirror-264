import matplotlib.pyplot as plt
from numpy import pi, exp

from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.LamSlot import LamSlot
from pyleecan.Classes.Segment import Segment
from pyleecan.definitions import config_dict
from pyleecan.Functions.Plot import (
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
from pyleecan.Methods import ParentMissingError

MAGNET_COLOR = config_dict["PLOT"]["COLOR_DICT"]["MAGNET_COLOR"]


def plot_schematics(
    self,
    is_default=False,
    is_return_default=False,
    is_add_point_label=False,
    is_add_schematics=True,
    is_add_main_line=True,
    type_add_active=True,
    save_path=None,
    is_show_fig=True,
    fig=None,
    ax=None,
):
    """Plot the schematics of the slot

    Parameters
    ----------
    self : SlotM19
        A SlotM19 object
    is_default : bool
        True: plot default schematics, else use current slot values
    is_return_default : bool
        True: return the default lamination used for the schematics (skip plot)
    is_add_point_label : bool
        True to display the name of the points (Z1, Z2....)
    is_add_schematics : bool
        True to display the schematics information (W0, H0...)
    is_add_main_line : bool
        True to display "main lines" (slot opening and 0x axis)
    type_add_active : int
        0: No active surface, 1: active surface as winding, 2: active surface as magnet
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
        Figure containing the schematics
    ax : Matplotlib.axes.Axes object
        Axis containing the schematics
    -------
    lam : LamSlot
        Default lamination used for the schematics
    """

    # Use some default parameter
    if is_default:
        # definir paramètre par défault
        slot = type(self)(Zs=4, W0=30e-3, H0=17.5e-3, W1=20e-3)
        if is_default == 1:  # Internal Rotor schematics
            lam = LamSlot(
                Rint=0.1, Rext=0.135, is_internal=True, is_stator=False, slot=slot
            )
            if is_return_default:
                return lam

        else:  # External Stator schematics
            lam = LamSlot(
                Rint=0.1, Rext=0.135, is_internal=False, is_stator=True, slot=slot
            )
            if is_return_default:
                return lam

        return slot.plot_schematics(
            is_default=False,
            is_return_default=False,
            is_add_point_label=is_add_point_label,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            type_add_active=type_add_active,
            save_path=save_path,
            is_show_fig=is_show_fig,
            fig=fig,
            ax=ax,
        )
    else:
        # Getting the main plot
        if self.parent is None:
            raise ParentMissingError("Error: The slot is not inside a Lamination")
        lam = self.parent
        fig, ax = lam.plot(
            alpha=pi / self.Zs, is_show_fig=False, fig=fig, ax=ax
        )  # center slot on Ox axis
        point_dict = self._comp_point_coordinate()
        if self.is_outwards():
            sign = +1
        else:
            sign = -1

        # Adding point label
        if is_add_point_label:
            for name, Z in point_dict.items():
                ax.text(
                    Z.real,
                    Z.imag,
                    name,
                    fontsize=P_FONT_SIZE,
                    bbox=TEXT_BOX,
                )

        # Adding schematics
        if is_add_schematics:
            # W0
            line = Segment(point_dict["Z3"], point_dict["Z2"])
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W0",
                offset_label=sign * self.H0 * 0.4,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W1
            plot_quote(
                Z1=point_dict["Z1"],
                Zlim1=point_dict["Z1"] - sign * 0.5 * self.H0,
                Zlim2=point_dict["Z4"] - sign * 0.5 * self.H0,
                Z2=point_dict["Z4"],
                offset_label=0.25 * self.H0,
                fig=fig,
                ax=ax,
                label="W1",
            )
            if lam.is_internal == False and lam.is_stator == True:
                # Hkey
                mid = point_dict["Zmid"]
                line = Segment(mid, mid - sign * self.H0)
                line.plot(
                    fig=fig,
                    ax=ax,
                    color=ARROW_COLOR,
                    linewidth=ARROW_WIDTH,
                    label="H0",
                    offset_label=1j * 0.1 * self.H0 - 0.0025,
                    is_arrow=True,
                    fontsize=SC_FONT_SIZE,
                )

            # H0
            mid = point_dict["Zmid"]
            line = Segment(mid, mid - sign * self.H0)
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H0",
                offset_label=1j * 0.1 * self.H0 - 0.0025,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

        if is_add_main_line:
            # Ox axis
            line = Segment(0, lam.Rext * 1.5)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # Magnet Arc
            line = Arc1(
                begin=point_dict["Z1"],
                end=point_dict["Z4"],
                radius=abs(point_dict["Z1"]),
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )

        if type_add_active == 1:
            self.plot_active(fig=fig, ax=ax, is_show_fig=False)
        elif type_add_active == 2:
            self.plot_active(
                fig=fig, ax=ax, is_show_fig=False, enforced_default_color=MAGNET_COLOR
            )

        # Zooming and cleaning
        W = self.W0 / 2 * 1.4
        Rint, Rext = self.comp_radius()

        ax.axis("equal")
        ax.set_xlim(Rint, Rext)
        ax.set_ylim(-W, W)
        manager = plt.get_current_fig_manager()
        if manager is not None:
            manager.set_window_title(type(self).__name__ + " Schematics")
        ax.set_title("")
        ax.get_legend().remove()
        ax.set_axis_off()
        fig.tight_layout()

        # Save / Show
        if save_path is not None:
            fig.savefig(save_path)
            plt.close(fig=fig)

        if is_show_fig:
            fig.show()
        return fig, ax
