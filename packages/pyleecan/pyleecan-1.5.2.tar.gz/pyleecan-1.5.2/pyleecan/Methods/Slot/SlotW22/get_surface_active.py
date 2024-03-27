from ....Functions.labels import WIND_LAB, DRAW_PROP_LAB
from ....Classes.SurfLine import SurfLine


def get_surface_active(self, alpha=0, delta=0):
    """Return the full winding surface

    Parameters
    ----------
    self : SlotW22
        A SlotW22 object
    alpha : float
        float number for rotation (Default value = 0) [rad]
    delta : complex
        complex number for translation (Default value = 0)

    Returns
    -------
    surf_wind: Surface
        Surface corresponding to the Winding Area
    """

    # Create curve list
    line_dict = self._comp_line_dict()
    curve_list = [
        line_dict["2-3"],
        line_dict["3-4"],
        line_dict["4-5"],
        line_dict["5-6"],
        line_dict["6-7"],
        line_dict["7-2"],
    ]
    curve_list = [line for line in curve_list if line is not None]

    # Only the closing arc (7-2) needs to be drawn (in FEMM)
    for curve in curve_list[:-1]:
        if curve.prop_dict is None:
            curve.prop_dict = dict()
        curve.prop_dict.update({DRAW_PROP_LAB: False})

    # Create surface
    label = self.parent.get_label() + "_" + WIND_LAB + "_R0-T0-S0"
    if self.is_outwards():
        Zmid = self.get_Rbo() + self.H0 + self.H2 / 2
    else:
        Zmid = self.get_Rbo() - self.H0 - self.H2 / 2
    surface = SurfLine(line_list=curve_list, label=label, point_ref=Zmid)

    # Apply transformation
    surface.rotate(alpha)
    surface.translate(delta)

    return surface
