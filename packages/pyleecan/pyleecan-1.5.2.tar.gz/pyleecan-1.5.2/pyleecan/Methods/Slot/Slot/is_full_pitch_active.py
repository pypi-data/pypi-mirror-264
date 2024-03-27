def is_full_pitch_active(self):
    """Returns True if the active surface angular width
    matches the slot pitch (like SlotM17 or SlotM18)
    (used to set Boundary conditions in FEMM airgap)

    Parameters
    ----------
    self : Slot
        A Slot object

    Returns
    -------
    is_full_pitch_active : bool
        True if the active surface angular width matches the slot pitch
    """

    return False
