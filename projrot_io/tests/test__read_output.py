"""
 tests reading of projrot output
"""

import os
import numpy
import projrot_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME1 = 'min.txt'
DATA_NAME2 = 'one_imag.txt'
DATA_NAME3 = 'two_imag.txt'
with open(os.path.join(DATA_PATH, DATA_NAME1), 'r') as datfile:
    OUT_STR1 = datfile.read()
with open(os.path.join(DATA_PATH, DATA_NAME2), 'r') as datfile:
    OUT_STR2 = datfile.read()
with open(os.path.join(DATA_PATH, DATA_NAME3), 'r') as datfile:
    OUT_STR3 = datfile.read()


def test__reader():
    """ test projrot_io.reader.rpht_output
    """

    # Obtain the real and imaginary frequencies from each file
    real1, imag1 = projrot_io.reader.rpht_output(OUT_STR1)
    real2, imag2 = projrot_io.reader.rpht_output(OUT_STR2)
    real3, imag3 = projrot_io.reader.rpht_output(OUT_STR3)

    assert numpy.allclose(real1, [5000.0, 4000.0, 3000.0, 2000.0, 1000.0])
    assert not imag1
    assert numpy.allclose(real2, [5000.0, 4000.0, 3000.0, 2000.0])
    assert numpy.allclose(imag2, [1111.11])
    assert numpy.allclose(real3, [5000.0, 4000.0, 3000.0])
    assert numpy.allclose(imag3, [2222.22, 1111.11])


if __name__ == '__main__':
    test__reader()
