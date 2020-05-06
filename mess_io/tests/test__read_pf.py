"""
 tests pf reader
"""

import os
import numpy
import mess_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'pf.txt'
with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
    OUT_STR = datfile.read()


def test__pf():
    """ Reads the output of a messpf file.
    """

    # Read the MESSPF output and store temps and Q fxns
    temps, logq, dq_dt, dq2_dt2 = mess_io.reader.pfs.partition_fxn(OUT_STR)

    # Print the values from the MESSPF output
    for val1, val2, val3, val4 in zip(temps, logq, dq_dt, dq2_dt2):
        print('{0} {1} {2} {3}'.format(val1, val2, val3, val4))

    ref_temps = [
        100.0, 200.0, 300.0, 400.0, 500.0,
        600.0, 700.0, 800.0, 900.0, 1000.0,
        1100.0, 1200.0, 1300.0, 1400.0, 1500.0,
        1600.0, 1700.0, 1800.0, 1900.0, 2000.0,
        2100.0, 2200.0, 2300.0, 2400.0, 2500.0,
        2600.0, 2700.0, 2800.0, 2900.0, 3000.0, 298.2]
    assert numpy.allclose(temps, ref_temps)

    ref_logq = [
        68.1917, 70.2712, 71.4876, 72.3506, 73.02,
        73.567, 74.0295, 74.4301, 74.7834, 75.0995,
        75.3854, 75.6464, 75.8866, 76.1089, 76.3159,
        76.5095, 76.6914, 76.8628, 77.025, 77.1789,
        77.3253, 77.4649, 77.5982, 77.7259, 77.8484,
        77.966, 78.0792, 78.1883, 78.2936, 78.3953, 71.4695]
    assert numpy.allclose(logq, ref_logq)

    ref_dq_dt = [
        0.03, 0.015, 0.01, 0.0075, 0.006,
        0.005, 0.00428572, 0.00375, 0.00333333, 0.003,
        0.00272727, 0.0025, 0.00230769, 0.00214286, 0.002,
        0.001875, 0.00176471, 0.00166667, 0.00157895, 0.0015,
        0.00142857, 0.00136364, 0.00130435, 0.00125, 0.0012,
        0.00115385, 0.00111111, 0.00107143, 0.00103448, 0.001, 0.0100604]
    assert numpy.allclose(dq_dt, ref_dq_dt)

    ref_dq2_dt2 = [
        -0.0003, -7.5e-05, -3.33333e-05, -1.875e-05, -1.2e-05,
        -8.33334e-06, -6.12245e-06, -4.6875e-06, -3.70371e-06,
        -3e-06, -2.47934e-06, -2.08333e-06, -1.77515e-06, -1.53061e-06,
        -1.33333e-06, -1.17188e-06, -1.03806e-06, -9.25926e-07, -8.31025e-07,
        -7.5e-07, -6.80272e-07, -6.19835e-07, -5.67108e-07, -5.20834e-07,
        -4.8e-07, -4.43787e-07, -4.11523e-07, -3.82653e-07, -3.56718e-07,
        -3.33333e-07, -3.3737e-05]
    assert numpy.allclose(dq2_dt2, ref_dq2_dt2)


if __name__ == '__main__':
    test__pf()
