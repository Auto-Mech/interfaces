"""
 writes the string for the chemkin
"""

import automol

# convert wavenumbers to Kelvin (check)
CM2K = 1.438776877


def lennard_jones(names, geos,
                  epsilons, sigmas,
                  dipole_moments, polarizabilities,
                  z_rots=None):
    """ writes the string for the transport
    """

    data_length = len(names)
    assert all(len(lst) == data_length
               for lst in [geos, epsilons, sigmas,
                           dipole_moments, polarizabilities])

    # Initialize string with common header
    chemkin_string = """! THEORETICAL TRANSPORT PROPERTIES
!
! (1) Shape, index denotes atom (0), linear molec. (1), nonlinear molec. (2);
! (2) Epsilon, the Lennard-Jones well depth, in K;
! (3) Sigma, the Lennard-Jones collision diameter, in Angstrom;
! (4) Mu, total dipole moment, in Debye;
! (5) Alpha, mean static polarizability, in Angstrom^3; and
! (6) Z_rot, rotational relaxation collision number at 298 K.\n"""

    # Find the length of the longest name string for formatting
    maxlen = 0
    for name in names:
        maxlen = max(maxlen, len(name))
    if maxlen <= 9:
        maxlen = 9
    nameslen = str(maxlen + 3)

    # get the shape index
    shape_idxs = []
    for geo in geos:
        if automol.geom.is_atom(geo):
            shape_idx = 0
        else:
            if automol.geom.is_linear(geo):
                shape_idx = 1
            else:
                shape_idx = 2
        shape_idxs.append(shape_idx)

    # Convert the cm-1 to K
    epsilons = [epsilon * CM2K for epsilon in epsilons]

    # if zrot empty make list of 1s as a defaults
    if z_rots is None:
        z_rots = [1.0 for i in range(data_length)]

    # Add the headers for each of the columns
    chemkin_string += ('{0:<'+nameslen+'}{1:>5s}{2:>12s}{3:>8s}' +
                       '{4:>8s}{5:>8s}{6:>8s}\n').format(
                           '! Species', 'Shape', 'Epsilon', 'Sigma',
                           'Mu', 'Alpha', 'Z_Rot')

    # Add the values to the string
    mol_data = zip(names, shape_idxs, epsilons,
                   sigmas, dipole_moments, polarizabilities, z_rots)
    for name, shape, eps, sig, dmom, polr, zrot in mol_data:
        chemkin_string += (
            '{0:<'+nameslen+'}{1:>5d}{2:>12.3f}{3:>8.3f}' +
            '{4:>8.3f}{5:>8.3f}{6:>8.3f}\n').format(
                name, shape, eps, sig, dmom, polr, zrot)

    return chemkin_string
