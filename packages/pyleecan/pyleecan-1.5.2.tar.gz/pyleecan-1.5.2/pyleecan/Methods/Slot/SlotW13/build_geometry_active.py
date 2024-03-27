from numpy import linspace, zeros

from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine
from ....Functions.labels import WIND_LAB, DRAW_PROP_LAB


def build_geometry_active(self, Nrad, Ntan, alpha=0, delta=0):
    """Split the slot winding area in several zone

    Parameters
    ----------
    self : SlotW13
        A SlotW13 object
    Nrad : int
        Number of radial layer
    Ntan : int
        Number of tangentiel layer
    alpha : float
        Angle for rotation (Default value = 0) [rad]
    delta : Complex
        complex for translation (Default value = 0)

    Returns
    -------
    surf_list:
        List of surface delimiting the winding zone

    """
    # get the name of the lamination
    lam_label = self.parent.get_label()

    point_dict = self._comp_point_coordinate()
    Z4 = point_dict["Z4"]
    Z5 = point_dict["Z5"]
    Z6 = point_dict["Z6"]
    Z7 = point_dict["Z7"]

    X = linspace(Z4, Z5, Nrad + 1)
    # Nrad+1 and Ntan+1 because 3 points => 2 zones
    Z = zeros((Nrad + 1, Ntan + 1), dtype=complex)
    for ii in range(Nrad + 1):
        Z[ii][:] = linspace(X[ii], X[ii].conjugate(), Ntan + 1)

    assert Z[0][0] == Z4
    assert Z[Nrad][0] == Z5
    assert Z[0][Ntan] == Z7
    assert Z[Nrad][Ntan] == Z6

    # We go thought the surface by Rad then Tan, starting by (0,0)
    surf_list = list()
    for jj in range(Ntan):  # jj from 0 to Ntan-1
        for ii in range(Nrad):  # ii from 0 to Nrad-1
            point_ref = (
                Z[ii][jj] + Z[ii][jj + 1] + Z[ii + 1][jj + 1] + Z[ii + 1][jj]
            ) / 4  # tre reference point of the surface
            # With one zone the order would be [Z7,Z4,Z5,Z6]
            curve_list = list()
            curve_list.append(Segment(Z[ii][jj], Z[ii][jj + 1]))
            curve_list.append(
                Segment(
                    Z[ii][jj + 1],
                    Z[ii + 1][jj + 1],
                    prop_dict={DRAW_PROP_LAB: False},
                )
            )
            curve_list.append(
                Segment(
                    Z[ii + 1][jj + 1],
                    Z[ii + 1][jj],
                    prop_dict={DRAW_PROP_LAB: False},
                )
            )
            curve_list.append(
                Segment(
                    Z[ii + 1][jj],
                    Z[ii][jj],
                    prop_dict={DRAW_PROP_LAB: jj != 0},
                )
            )
            surface = SurfLine(
                line_list=curve_list,
                label=lam_label
                + "_"
                + WIND_LAB
                + "_R"
                + str(ii)
                + "-T"
                + str(jj)
                + "-S0",
                point_ref=point_ref,
            )  # surface in the winding area
            surf_list.append(surface)

    for surf in surf_list:
        surf.rotate(alpha)  # rotation of each surface
        surf.translate(delta)  # translation of each surface

    return surf_list
