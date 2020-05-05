""" functions operating on the reactions block string
"""


import numpy as np
from qcelemental import constants as qcc
import ratefit
from chemkin_io.parser import reaction as rxn_parser

# Constants and Conversion factors
# NAVO = qcc.constants.avogadro_constant
NAVO = 6.0221409e+23
CAL2KCAL = qcc.conversion_factor('cal/mol', 'kcal/mol')
J2KCAL = qcc.conversion_factor('J/mol', 'kcal/mol')
KJ2KCAL = qcc.conversion_factor('kJ/mol', 'kcal/mol')
KEL2KCAL = qcc.conversion_factor('kelvin', 'kcal/mol')


def mechanism(rxn_block, rxn_units, t_ref, temps, pressures):
    """ calculate the reactions rates for a whole block via a dict
    """

    reaction_data_strings = rxn_parser.data_strings(rxn_block)
    mech_dct = {}
    for dstr in reaction_data_strings:
        rct_names = rxn_parser.reactant_names(dstr)
        prd_names = rxn_parser.product_names(dstr)
        rxn = (rct_names, prd_names)
        # rxn_rev = (prd_names, rct_names)
        if rxn not in mech_dct:
            mech_dct[rxn] = reaction(dstr, rxn_units,
                                     t_ref, temps, pressures=pressures)
        else:
            new_ktp_dct = reaction(dstr, rxn_units,
                                   t_ref, temps, pressures=pressures)
            mech_dct[rxn] = _add_rates(mech_dct[rxn], new_ktp_dct)
        # if rxn not in mech_dct and rxn_rev not in mech_dct:
        #     mech_dct[rxn] = reaction(dstr, rxn_units,
        #                              t_ref, temps, pressures=pressures)
        # elif rxn in mech_dct and rxn_rev not in mech_dct:
        #     new_ktp_dct = reaction(dstr, rxn_units,
        #                            t_ref, temps, pressures=pressures)
        #     mech_dct[rxn] = _add_rates(mech_dct[rxn], new_ktp_dct)
        # elif rxn not in mech_dct and rxn_rev in mech_dct:
        #     new_ktp_dct = reaction(dstr, rxn_units,
        #                            t_ref, temps, pressures=pressures)
        #     mech_dct[rxn_rev] = _add_rates(mech_dct[rxn_rev], new_ktp_dct)

    # ktp_dct = {}
    # for name, rxn_dstr in rxn_dct.items():
    #     ktp_dct[name] = reaction(
    #         rxn_dstr, rxn_units, t_ref, temps, pressures=pressures)

    return mech_dct


def reaction(rxn_str, rxn_units, t_ref, temps, pressures=None):
    """ calculate the rate constant using the rxn_string
    """
    rate_constants = {}

    # Accepts a params dictionary
    # Read the parameters from the reactions string
    highp_params = rxn_parser.high_p_parameters(rxn_str)
    lowp_params = rxn_parser.low_p_parameters(rxn_str)
    troe_params = rxn_parser.troe_parameters(rxn_str)
    chebyshev_params = rxn_parser.chebyshev_parameters(rxn_str)
    plog_params = rxn_parser.plog_parameters(rxn_str)

    print('\nplog', plog_params)
    print('cheb', chebyshev_params)
    print('lowp', lowp_params)

    # Calculate high_pressure rates
    highp_ks = _arrhenius(highp_params, temps, t_ref, rxn_units)
    rate_constants['high'] = highp_ks

    # Calculate pressure-dependent rate constants based on discovered params
    # Either (1) Plog, (2) Chebyshev, (3) Lindemann, or (4) Troe
    # Update units if necessary
    if any(params is not None
           for params in (plog_params, chebyshev_params, lowp_params)):
        assert pressures is not None

    pdep_dct = {}
    if plog_params is not None:
        pdep_dct = _plog(plog_params, pressures, temps, t_ref, rxn_units)

    elif chebyshev_params is not None:
        pdep_dct = _chebyshev(chebyshev_params, pressures, temps)

    elif lowp_params is not None:
        lowp_ks = _arrhenius(lowp_params, temps, t_ref, rxn_units)
        if troe_params is not None:
            pdep_dct = _troe(troe_params, highp_ks, lowp_ks,
                             pressures, temps)
        else:
            pdep_dct = ratefit.calc.lindemann(
                highp_ks, lowp_ks, pressures, temps)

    # Build the rate constants dictionary with the pdep dict
    if pdep_dct:
        rate_constants.update(pdep_dct)

    return rate_constants


def _add_rates(ktp_dct1, ktp_dct2):
    """ add the rates of two dictionaries together
    """
    for pressure in ktp_dct1:
        ktp_dct1[pressure] += ktp_dct2[pressure]
    return ktp_dct1


def _arrhenius(arr_params, temps, t_ref, rxn_units):
    """ calc arrhenius
    """
    arr_params = _update_params_units(arr_params, rxn_units)
    rate_ks = ratefit.calc.arrhenius(arr_params, t_ref, temps)
    return rate_ks


def _plog(plog_params, pressures, temps, t_ref, rxn_units):
    """ calc plog
    """
    for pressure, params in plog_params.items():
        plog_params[pressure] = _update_params_units(params, rxn_units)
    pdep_dct = ratefit.calc.plog(plog_params, t_ref, pressures, temps)
    return pdep_dct


def _chebyshev(chebyshev_params, pressures, temps):
    """ calc chebyshev
    """
    [tmin, tmax] = chebyshev_params['t_limits']
    [pmin, pmax] = chebyshev_params['p_limits']
    [arows, acols] = chebyshev_params['alpha_dim']
    alpha = np.array(chebyshev_params['alpha_elm'])
    assert alpha.shape == (arows, acols)
    pdep_dct = ratefit.calc.chebyshev(
        alpha, tmin, tmax, pmin, pmax, pressures, temps)
    return pdep_dct


def _troe(troe_params, highp_ks, lowp_ks, pressures, temps):
    """ calc troe
    """
    if len(troe_params) == 3:
        ts2 = None
    elif len(troe_params) == 4:
        ts2 = troe_params[3]
    pdep_dct = ratefit.calc.troe(
        highp_ks, lowp_ks, pressures, temps,
        troe_params[0], troe_params[1], troe_params[2], ts2=ts2)
    return pdep_dct


def _update_params_units(params, rxn_units):
    """ change the units if necessary
        only needed for highp, lowp, and plog
    """
    # Determine converstion factor for Ea Units
    ea_units = rxn_units[0]
    if ea_units == 'cal/mole':
        ea_conv_factor = CAL2KCAL
    elif ea_units == 'joules/mole':
        ea_conv_factor = J2KCAL
    elif ea_units == 'kjoules/mole':
        ea_conv_factor = KJ2KCAL
    elif ea_units == 'kelvin':
        ea_conv_factor = KEL2KCAL
    else:
        ea_conv_factor = 1.0

    # Determine converstion factor for A Units
    if rxn_units[1] == 'molecules':
        a_conv_factor = NAVO
    else:
        a_conv_factor = 1.0

    # update units of params
    if params is not None:
        params[0][0] *= a_conv_factor
        params[0][2] *= ea_conv_factor
        if len(params) > 1:
            params[1][0] *= a_conv_factor
            params[1][2] *= ea_conv_factor

    return params
