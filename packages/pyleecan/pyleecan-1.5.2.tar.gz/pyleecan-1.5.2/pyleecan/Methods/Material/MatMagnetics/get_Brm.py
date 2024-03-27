from numpy import pi


def get_Brm(self, T_op=None, T_ref=20):
    """Get magnetic remanent flux density

    Parameters
    ----------
    self : MatMagnetics
        a MatMagnetics object
    T_op: float
        Material operational temperature [degC]
    T_ref: float
        Material reference temperature [degC]

    Returns
    -------
    Brm: float
        Magnetic remanent flux density

    """

    if T_op is None:
        T_op = T_ref

    # Get magnetic remanent flux density at 20 degC from excitation coercitivity
    if self.Brm20 is None:
        raise Exception("Cannot calculate Brm20 if Hc or mur_lin is None")
    else:
        Brm20 = self.Brm20

    # Update magnetic remanent flux density
    Brm = Brm20 * (1 + self.alpha_Br * (T_op - T_ref))

    return Brm
