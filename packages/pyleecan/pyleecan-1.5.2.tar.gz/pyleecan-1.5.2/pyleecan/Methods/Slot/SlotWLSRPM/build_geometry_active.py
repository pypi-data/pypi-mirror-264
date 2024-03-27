# -*- coding: utf-8 -*-

from numpy import angle
from scipy.optimize import fsolve

from ....Classes.Arc1 import Arc1
from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine
from ....Functions.labels import WIND_LAB


def build_geometry_active(self, Nrad, Ntan, is_simplified=False, alpha=0, delta=0):
    """Split the slot active area in several zone

    Parameters
    ----------
    self : SlotWLSRPM
        A SlotWLSRPM object
    Nrad : int
        Number of radial layer
    Ntan : int
        Number of tangentiel layer
    is_simplified : bool
        boolean to specify if coincident lines are considered as one or different lines (Default value = False)
    alpha : float
        Angle for rotation (Default value = 0) [rad]
    delta : Complex
        complex for translation (Default value = 0)

    Returns
    -------
    surf_list:
        List of surface delimiting the active zone

    """

    lam_label = self.parent.get_label()
    Rbo = self.get_Rbo()

    point_dict = self._comp_point_coordinate()
    Z1 = point_dict["Z1"]
    Z2 = point_dict["Z2"]
    Z3 = point_dict["Z3"]
    Z4 = point_dict["Z4"]
    Z5 = point_dict["Z5"]
    Z6 = point_dict["Z6"]
    Z7 = point_dict["Z7"]
    Z8 = point_dict["Z8"]
    Z9 = point_dict["Z9"]
    Z10 = point_dict["Z10"]

    Zcl = point_dict["Zcl"]
    Zcm = point_dict["Zcm"]
    Zch = point_dict["Zch"]
    Zmid = point_dict["Zmid"]

    # Creation of curve
    surf_list = list()
    if Nrad == 1 and Ntan == 2:
        # Part 1 (0,0)
        line1 = Segment(Z3, Z4)
        line2 = Segment(Z4, Zch)
        line3 = Segment(Zch, Zcl)
        line4 = Arc1(Zcl, Z1, -Rbo, is_trigo_direction=False)
        line5 = Segment(Z1, Z2)
        line6 = Arc1(Z2, Z3, self.R1, is_trigo_direction=True)
        point_ref = (Z3 + Z4 + Zch + Zcl + Z1 + Z2) / 6

        surface = SurfLine(
            line_list=[line1, line2, line3, line4, line5, line6],
            label=(lam_label + "_" + WIND_LAB + "_R0-T0-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

        # Part2 (0,1)
        line1 = Segment(Zch, Z5)
        line2 = Segment(Z5, Z6)
        line3 = Arc1(Z6, Z7, self.R1, is_trigo_direction=True)
        line4 = Segment(Z7, Z8)
        line5 = Arc1(Z8, Zcl, -Rbo, is_trigo_direction=False)
        line6 = Segment(Zcl, Zch)
        point_ref = (Zch + Z5 + Z6 + Z7 + Z8 + Zcl) / 6
        surface = SurfLine(
            line_list=[line1, line2, line3, line4, line5, line6],
            label=(lam_label + "_" + WIND_LAB + "_R0-T1-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

    if Nrad == 2 and Ntan == 2:
        # Part 1 (0,0)
        line1 = Segment(Z3, Z4)
        line2 = Segment(Z4, Zch)
        line3 = Segment(Zch, Zcm)
        line4 = Arc1(Zcm, Z9, -(Rbo + self.H3), is_trigo_direction=False)
        line5 = Segment(Z9, Z2)
        line6 = Arc1(Z2, Z3, self.R1, is_trigo_direction=True)
        point_ref = (Z3 + Z4 + Zch + Zcm + Z9 + Z2) / 6

        surface = SurfLine(
            line_list=[line1, line2, line3, line4, line5, line6],
            label=(lam_label + "_" + WIND_LAB + "_R0-T0-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

        # Part2 (0,1)
        line1 = Segment(Zch, Z5)
        line2 = Segment(Z5, Z6)
        line3 = Arc1(Z6, Z7, self.R1, is_trigo_direction=True)
        line4 = Segment(Z7, Z10)
        line5 = Arc1(Z10, Zcm, -(Rbo + self.H3), is_trigo_direction=False)
        line6 = Segment(Zcm, Zch)
        point_ref = (Zch + Z5 + Z6 + Z7 + Z10 + Zcm) / 6
        surface = SurfLine(
            line_list=[line1, line2, line3, line4, line5, line6],
            label=(lam_label + "_" + WIND_LAB + "_R0-T1-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

        # Part3 (1,1)
        line1 = Arc1(Zcm, Z10, Rbo + self.H3, is_trigo_direction=True)
        line2 = Segment(Z10, Z8)
        line3 = Arc1(Z8, Zcl, -Rbo, is_trigo_direction=False)
        line4 = Segment(Zcl, Zcm)
        point_ref = (Zcm + Z10 + Z8 + Zcl) / 4
        surface = SurfLine(
            line_list=[line1, line2, line3, line4],
            label=(lam_label + "_" + WIND_LAB + "_R1-T1-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

        # Part4 (1,0)
        line1 = Arc1(Z9, Zcm, Rbo + self.H3, is_trigo_direction=True)
        line2 = Segment(Zcm, Zcl)
        line3 = Arc1(Zcl, Z1, -Rbo, is_trigo_direction=False)
        line4 = Segment(Z1, Z9)
        point_ref = (Z9 + Zcm + Zcl + Z1) / 4
        surface = SurfLine(
            line_list=[line1, line2, line3, line4],
            label=(lam_label + "_" + WIND_LAB + "_R1-T0-S0"),
            point_ref=point_ref,
        )
        surf_list.append(surface)

    else:  # Default : only one zone
        curve_list = self.build_geometry()

        # Add a line to close the winding area
        lines = [
            Arc1(
                curve_list[-1].end,
                curve_list[0].begin,
                -Rbo,
                is_trigo_direction=False,
            )
        ]
        lines.extend(curve_list)
        surface = SurfLine(
            line_list=lines,
            label=lam_label + "_" + WIND_LAB + "_R0-T0-S0",
            point_ref=Zmid,
        )
        surf_list.append(surface)

    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)
    return surf_list
