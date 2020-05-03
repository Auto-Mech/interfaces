"""
 tests torsional mode reader
"""

import os
import mess_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'mess_log.txt'
with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
    OUT_STR = datfile.read()


def test__tors():
    """ Reads the output of a mess file.
    """

    # Read the freqs and zpves
    freqs = mess_io.reader.tors.freqs(OUT_STR)
    zpves = mess_io.reader.tors.zpves(OUT_STR)

    # Print the freqs and zpves
    for i, (freq, zpve) in enumerate(zip(freqs, zpves)):
        print('{0:4d}{1:10.4f}{2:10.4f}'.format(i+1, freq, zpve))


if __name__ == '__main__':
    test__tors()
