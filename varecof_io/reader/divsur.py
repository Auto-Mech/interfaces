"""
  Functions to parse information out of the divsur input and output files
"""


def frag_geoms_divsur_frame(divsur_str):
    """ Read the geometries of the fragments out of divsur.out file string
        which are in the coord system defined in the divsur.inp frames.

        :param divsur_str: string with geoms made from divsur frames
        :type divsur_str: str
        :return fgeo1: geometry of fragment 1 in divsur frame
        :rtype: str
        :return fgeo2: geometry of fragment 2 in divsur frame
        :rtype: str
    """

    # Get where the fragment geometries are defined
    lines = divsur_str.splitlines()
    for i, line in enumerate(lines):
        if 'Fragment 1:' in line:
            f1_idx = i+1
        if 'Fragment 2:' in line:
            f2_idx = i+1
        if 'SURFACE INDEX' in line:
            end_idx = i
            break

    fgeo1 = ''.join(lines[f1_idx: f2_idx-2])
    fgeo2 = ''.join(lines[f2_idx: end_idx])

    return fgeo1, fgeo2
