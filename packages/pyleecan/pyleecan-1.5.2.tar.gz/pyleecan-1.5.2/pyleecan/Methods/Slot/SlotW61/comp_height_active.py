# -*- coding: utf-8 -*-

from numpy import pi, exp


def comp_height_active(self):
    """Compute the height of the winding area

    Parameters
    ----------
    self : SlotW61
        A SlotW61 object

    Returns
    -------
    Hwind: float
        Height of the winding area [m]

    """

    point_dict = self._comp_point_coordinate()
    Z4 = point_dict["Z4"]
    Z5 = point_dict["Z5"]

    # Compute the point in the tooth ref
    hsp = pi / self.Zs
    Z4t = Z4 * exp(1j * hsp)
    Z5t = Z5 * exp(1j * hsp)
    Zw4t = Z4t - self.H3 + 1j * ((self.W1 - self.W2) / 2 - self.W3)
    Zw2t = Z5t + self.H4

    return abs(Zw4t) - abs(Zw2t)
