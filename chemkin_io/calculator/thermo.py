""" Calculates thermodynamic quantities using thermo data strings
"""


import numpy as np
from chemkin_io.parser import thermo as thm_parser


RC = 1.98720425864083e-3  # in kcal/mol.K


# functions which calculate quantiies using data from the thermo section #
def mechanism(block_str, temps):
    """ Loop over a dictionary of NASA polynomials for a mechanism
        :param string block_str: String of Reaction block of CHEMKIN input
        :param list temps: Temperatures to calculate Thermo quantities (K)
        :return mech_thermo_dct: dct of thermo data [H(T), Cp(T), S(T), G(T)]
        :rtype: dct
    """

    nasa_dct = thm_parser.data_dct(block_str)

    mech_thermo_dct = {}
    for name, thermo_dstr in nasa_dct.items():
        h_t, cp_t, s_t, g_t, = [], [], [], []
        for temp in temps:
            h_t.append(enthalpy(thermo_dstr, temp))
            cp_t.append(heat_capacity(thermo_dstr, temp))
            s_t.append(entropy(thermo_dstr, temp))
            g_t.append(gibbs(thermo_dstr, temp))

        mech_thermo_dct[name] = [h_t, cp_t, s_t, g_t]

    return mech_thermo_dct


def enthalpy(thm_dstr, temp):
    """ Calculate the Enthalpy [H(T)] of a species using the
        coefficients of its NASA polynomial
        :param string thm_dstr: String containing NASA polynomial of species
        :param float temp: Temperature to calculate Enthalpy
        :return h_t: Value for the Enthalpy
        :rtype: float
    """

    cfts = _coefficients_for_specific_temperature(thm_dstr, temp)

    if cfts is not None:
        h_t = (
            cfts[0] +
            ((cfts[1] * temp) / 2.0) +
            ((cfts[2] * temp**2) / 3.0) +
            ((cfts[3] * temp**3) / 4.0) +
            ((cfts[4] * temp**4) / 5.0) +
            (cfts[5] / temp)
        )
        h_t *= (RC * temp)
    else:
        h_t = None

    return h_t


def heat_capacity(thm_dstr, temp):
    """ Calculate the Heat Capacity [Cp(T)] of a species using the
        coefficients of its NASA polynomial
        :param string thm_dstr: String containing NASA polynomial of species
        :param float temp: Temperature to calculate Heat Capacity
        :return cp_t: Value for the Heat Capacity
        :rtype: float
    """
    cfts = _coefficients_for_specific_temperature(thm_dstr, temp)

    if cfts is not None:
        cp_t = (
            cfts[0] +
            (cfts[1] * temp) +
            (cfts[2] * temp**2) +
            (cfts[3] * temp**3) +
            (cfts[4] * temp**4)
        )
        cp_t *= RC
    else:
        cp_t = None

    return cp_t


def entropy(thm_dstr, temp):
    """ Calculate the Entropy [S(T)] of a species using the
        coefficients of its NASA polynomial
        :param string thm_dstr: String containing NASA polynomial of species
        :param float temp: Temperature to calculate Entropy
        :return s_t: Value for the Entropy
        :rtype: float
    """
    cfts = _coefficients_for_specific_temperature(thm_dstr, temp)

    if cfts is not None:
        s_t = (
            (cfts[0] * np.log(temp)) +
            (cfts[1] * temp) +
            ((cfts[2] * temp**2) / 2.0) +
            ((cfts[3] * temp**3) / 3.0) +
            ((cfts[4] * temp**4) / 4.0) +
            (cfts[6])
        )
        s_t *= RC
    else:
        s_t = None

    return s_t


def gibbs(thm_dstr, temp):
    """ Calculate the Gibbs Free Energy [H(T)] of a species using the
        coefficients of its NASA polynomial
        :param string thm_dstr: String containing NASA polynomial of species
        :param float temp: Temperature to calculate Gibbs Free Energy
        :return g_t: Value for the Gibbs Free Energy
        :rtype: float
    """

    h_t = enthalpy(thm_dstr, temp)
    s_t = entropy(thm_dstr, temp)
    if enthalpy is not None and entropy is not None:
        g_t = h_t - (s_t * temp)
    else:
        g_t = None

    return g_t


def _coefficients_for_specific_temperature(thm_dstr, temp):
    """ Parse out the coefficients of a NASA polynomial from 
        a CHEMKIN-formatted string. The input temperature value
        determines whether the low- or high-temperature coefficients
        are read from the string
        :param string thm_dstr: String containing NASA polynomial of species
        :param float temp: Temperature used to read the coefficients
        :return cfts: low- or high-temperature coefficients of NASA polynomial
        :rtype: list
    """

    temps = thm_parser.temperatures(thm_dstr)
    if temps[0] < temp < temps[1]:
        cfts = thm_parser.low_coefficients(thm_dstr)
    elif temps[1] < temp < temps[2]:
        cfts = thm_parser.high_coefficients(thm_dstr)
    else:
        cfts = None

    return cfts
