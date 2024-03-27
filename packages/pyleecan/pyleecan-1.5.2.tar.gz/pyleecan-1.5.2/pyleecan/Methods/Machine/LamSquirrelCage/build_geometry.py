# -*- coding: utf-8 -*-
from ....Functions.labels import WIND_LAB, BAR_LAB

from ....Classes.LamSlotWind import LamSlotWind


def build_geometry(self, sym=1, alpha=0, delta=0, is_circular_radius=False):
    """Build geometry of the LamSquirrelCage

    Parameters
    ----------
    self :
        LamSquirrelCage Object
    sym : int
        Symmetry factor (1= full machine, 2= half of the machine...)
    alpha : float
        Angle for rotation [rad]
    delta : complex
        Complex value for translation
    is_circular_radius : bool
        True to add surfaces to "close" the Lamination radii

    Returns
    -------
    surf_list: list
        list of surfaces

    """
    surf_list = LamSlotWind.build_geometry(
        self, sym=sym, is_circular_radius=is_circular_radius, alpha=alpha, delta=delta
    )

    # Adapt the label
    for surf in surf_list:
        if WIND_LAB in surf.label:
            surf.label = surf.label.replace(WIND_LAB, BAR_LAB)

    return surf_list
