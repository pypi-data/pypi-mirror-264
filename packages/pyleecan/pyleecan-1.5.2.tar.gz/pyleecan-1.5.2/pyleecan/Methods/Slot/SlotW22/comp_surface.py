# -*- coding: utf-8 -*-

from numpy import pi


def comp_surface(self):
    """Compute the Slot total surface (by analytical computation).
    Caution, the bottom of the Slot is an Arc

    Parameters
    ----------
    self : SlotW22
        A SlotW22 object

    Returns
    -------
    S: float
        Slot total surface [m**2]

    """
    return self.comp_surface_active() + self.comp_surface_opening()
