"""
Test the rate plotting functionality for comparing two mechanisms
"""

import numpy as np
import chemkin_io


from data_rates import KTP_DCT
TEMPS = np.array([500.0, 1000.0, 1500.0])


def test__plot_rates():
    """ test chemkin_io.plotter.rates
    """
    chemkin_io.plotter.rates.build(KTP_DCT, TEMPS)


if __name__ == '__main__':
    test__plot_rates()
