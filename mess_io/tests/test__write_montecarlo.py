"""
Tests writing the input for a Monte Carlo sampling routine
"""

import mess_io


GEOM = (('C', (2.3369630270, 2.6603645819, -0.0002949975)),
        ('O', (4.9791531078, 2.6863483093, 0.0032931188)),
        ('H', (1.5983237149, 3.8235373073, -1.5858750908)),
        ('H', (1.5983208663, 3.3506042568, 1.8410631867)),
        ('H', (1.6779634212, 0.6888161696, -0.2723782755)),
        ('H', (5.4770534286, 4.4773038573, 0.2504520555)))
FORMULA = 'CH3OH'
DATA_FILE_NAME = 'tau.out'
GROUND_ENERGY = 32.724
REF_ENERGY = 0.00
FLUX_IDX = (6, 2, 1, 3)
FLUX_SPAN = 120.0


def test__monte_carlo_writer():
    """ write input string
    """

    # Write the fluxional mode string
    flux_mode_str = mess_io.writer.fluxional_mode(
        FLUX_IDX, span=FLUX_SPAN)

    # Write the monte carlo species section with flux mode string
    monte_carlo_str = mess_io.writer.mc_species(
        GEOM, FORMULA,
        flux_mode_str, DATA_FILE_NAME,
        GROUND_ENERGY, REF_ENERGY,
        freqs=(), no_qc_corr=False, use_cm_shift=False)

    # Print the monte carlo string
    print(monte_carlo_str)


if __name__ == '__main__':
    test__monte_carlo_writer()
