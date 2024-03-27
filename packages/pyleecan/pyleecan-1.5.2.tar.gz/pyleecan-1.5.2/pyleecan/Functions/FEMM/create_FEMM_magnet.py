def create_FEMM_magnet(femm, is_mmf, is_eddies, materials, mag_obj, T_mag):
    """Set the material of the magnet in FEMM

    Parameters
    ----------
    femm : FEMMHandler
        client to send command to a FEMM instance
    is_mmfr : bool
        1 to compute the lamination magnetomotive force / magnetic field
    is_eddies : bool
        1 to calculate eddy currents
    materials : list
        list of materials already created in FEMM
    mag_obj : Magnet
        Magnet object to set the material
    T_mag: float
        Permanent magnet temperature [deg Celsius]

    Returns
    -------
    (str, list)
        property, materials

    """

    rho = mag_obj.mat_type.elec.rho  # Resistivity
    Hcm = mag_obj.mat_type.mag.get_Hc(T_op=T_mag)  # Magnet coercitivity field
    mur = mag_obj.mat_type.mag.mur_lin

    mat_name = mag_obj.mat_type.name
    if mat_name not in materials:
        femm.mi_addmaterial(
            mat_name,
            mur,
            mur,
            is_mmf * Hcm,
            0,
            is_mmf * is_eddies * 1e-6 / rho,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
        )
        materials.append(mat_name)

    return mat_name, materials
