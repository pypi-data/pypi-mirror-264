from ....Classes.Segment import Segment
from ....Classes.Arc1 import Arc1


def _comp_line_dict(self):
    """Define a dictionnary of the lines to draw the slot
    If a line has begin==end, it is replaced by "None" (dict has always the same number of keys)

    Parameters
    ----------
    self : SlotW24
        A SlotW24 object

    Returns
    -------
    line_dict: dict
        Dictionnary of the slot lines (key: line name, value: line object)
    """

    point_dict = self._comp_point_coordinate()
    Z1 = point_dict["Z1"]
    Z2 = point_dict["Z2"]
    Z3 = point_dict["Z3"]
    Z4 = point_dict["Z4"]
    Zc = 0

    # Creation of curve
    line_dict = dict()
    line_dict["1-2"] = Segment(Z1, Z2)
    line_dict["2-3"] = Arc1(Z2, Z3, abs(Z2))
    line_dict["3-4"] = Segment(Z3, Z4)

    # Closing Arc (Rbo)
    line_dict["4-1"] = Arc1(Z4, Z1, -self.get_Rbo(), is_trigo_direction=False)

    # Closing Active part
    line_dict["1-4"] = Arc1(Z1, Z4, self.get_Rbo(), is_trigo_direction=True)

    return line_dict
