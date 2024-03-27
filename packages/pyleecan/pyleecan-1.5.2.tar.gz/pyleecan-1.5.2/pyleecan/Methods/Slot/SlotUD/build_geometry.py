from ....Classes.Segment import Segment


def build_geometry(self):
    """Compute the curve (Line) needed to plot the object.
    The ending point of a curve is the starting point of the next curve
    in the list

    Parameters
    ----------
    self : SlotUD
        A SlotUD object

    Returns
    -------
    curve_list: list
        A list of Segments

    """

    return [line.copy() for line in self.line_list]
