"""
  Tests the varecof_io.writer functions
"""

import os
import varecof_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'divsur.txt'
with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
    OUT_STR = datfile.read()


def test__divsur_frag_geoms_reader():
    """ tests varecof_io.reader.divsur.frag_geoms_divsur_frame
    """
    frag_geoms = varecof_io.reader.divsur.frag_geoms_divsur_frame(
        OUT_STR)
    print(frag_geoms)


if __name__ == '__main__':
    test__divsur_frag_geoms_reader()
