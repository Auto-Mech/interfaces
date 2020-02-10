"""
Take data dictionaries from mechanisms and combine them under a common index
"""

import itertools
import numpy as np
import chemkin_io.parser
from chemkin_io.calculator import thermo
from chemkin_io.calculator import rates
from chemkin_io.parser.mechanism import reaction_units


RC = 1.98720425864083e-3  # in kcal/mol.K


def mechanism_thermo(mech1_thermo_dct, mech2_thermo_dct):
    """ Loop over the the Mech1 thermo entries
    """

    total_thermo_dct = {}

    # Build full thermo dictionary with common index
    # First loop through mech1: add common and mech1-unique species
    for mech1_name, mech1_vals in mech1_thermo_dct.items():
        mech2_vals = mech2_thermo_dct.get(mech1_name, [None, None, None, None])
        total_thermo_dct[mech1_name] = {
            'mech1': mech1_vals,
            'mech2': mech2_vals
        }

    # Now add the entries where mech2 exists, but mech1 does not
    uni_mech2_names = [name
                       for name in mech2_thermo_dct.keys()
                       if name not in mech1_thermo_dct]

    for mech2_name in uni_mech2_names:
        total_thermo_dct[mech2_name] = {
            'mech1': [None, None, None, None],
            'mech2': mech2_thermo_dct[mech2_name]
        }

    return total_thermo_dct


def mechanism_rates(mech1_ktp_dct, mech2_ktp_dct, temps,
                    mech2_thermo_dct=None):
    """ calculate the reactions rates for two mech files
    """

    total_ktp_dct = {}

    # Build full rates dictionary with common index
    # First loop through mech1: add common and mech1-unique species
    for mech1_name, mech1_ktp in mech1_ktp_dct.items():

        # Check what (if/any) combination of mech2 matches with mech1
        mech2_name_match, reverse_rates = _assess_reaction_match(
            mech1_name, mech2_ktp_dct)

        # Calculate reaction rates, reverse if needed
        if mech2_name_match:
            if not reverse_rates:
                mech2_ktp = mech2_ktp_dct[mech1_name]
            else:
                assert mech2_thermo_dct is not None
                mech2_ktp = _reverse_reaction_rates(
                    mech2_ktp_dct, mech2_thermo_dct, mech2_name_match, temps)
        else:
            mech2_ktp = {}

        # Add data_entry to overal thermo dictionary
        total_ktp_dct[mech1_name] = {
            'mech1': mech1_ktp,
            'mech2': mech2_ktp
        }

        # Now add the entries where mech2 exists, but mech1 does not
        # add the code to do this

    return total_ktp_dct


# Thermo functions
def build_thermo_name_dcts(mech1_str, mech2_str, temps):
    """ builds the thermo dictionaries indexed by names
    """

    mech1_thermo_block = chemkin_io.parser.mechanism.thermo_block(mech1_str)
    if mech1_thermo_block is not None:
        mech1_thermo_block = chemkin_io.parser.util.clean_up_whitespace(
            mech1_thermo_block)
        mech1_thermo_dct = thermo.mechanism(
            mech1_thermo_block, temps)
    else:
        mech1_thermo_dct = None

    mech2_thermo_block = chemkin_io.parser.mechanism.thermo_block(mech2_str)
    if mech2_thermo_block is not None:
        mech2_thermo_block = chemkin_io.parser.util.clean_up_whitespace(
            mech2_thermo_block)
        mech2_thermo_dct = thermo.mechanism(
            mech2_thermo_block, temps)
    else:
        mech2_thermo_dct = None

    return mech1_thermo_dct, mech2_thermo_dct


def build_thermo_inchi_dcts(mech1_str, mech2_str,
                            mech1_csv_str, mech2_csv_str,
                            temps):
    """ builds new thermo dictionaries indexed by inchis
    """
    # Get dicts: dict[name] = thm_dstr
    mech1_thermo_dct, mech2_thermo_dct = build_thermo_name_dcts(
        mech1_str, mech2_str, temps)

    # Build the inchi dicts where:
    # Get dicts: dict[name] = inchi
    # Convert name dict to get: dict[inchi] = name
    if mech1_thermo_dct is not None:
        mech1_name_inchi_dct = chemkin_io.parser.mechanism.spc_name_dct(
            mech1_csv_str, 'inchi')
        mech1_thermo_ich_dct = {}
        for name, data in mech1_thermo_dct.items():
            ich = mech1_name_inchi_dct[name]
            mech1_thermo_ich_dct[ich] = data
    else:
        mech1_thermo_ich_dct = None

    if mech2_thermo_dct is not None:
        mech2_name_inchi_dct = chemkin_io.parser.mechanism.spc_name_dct(
            mech2_csv_str, 'inchi')
        mech2_thermo_ich_dct = {}
        for name, data in mech2_thermo_dct.items():
            ich = mech2_name_inchi_dct[name]
            mech2_thermo_ich_dct[ich] = data
    else:
        mech2_thermo_ich_dct = None

    return mech1_thermo_ich_dct, mech2_thermo_ich_dct


def spc_name_from_inchi(mech1_csv_str, mech2_csv_str, ich):
    """ uses dict[inchi]=name dicts to get
        the mechanism name for a given InChI string
    """

    mech1_inchi_dct = chemkin_io.parser.mechanism.spc_inchi_dct(mech1_csv_str)
    mech2_inchi_dct = chemkin_io.parser.mechanism.spc_inchi_dct(mech2_csv_str)

    if ich in mech1_inchi_dct:
        mech_name = mech1_inchi_dct[ich]
    else:
        mech_name = mech2_inchi_dct[ich]

    return mech_name


# Rate functions
def _assess_reaction_match(mech1_names, mech2_dct):
    """ assess whether the reaction should be flipped
    """

    [mech1_rcts, mech1_prds] = mech1_names
    mech1_rct_comb = list(itertools.combinations(mech1_rcts, len(mech1_rcts)))
    mech1_prd_comb = list(itertools.combinations(mech1_prds, len(mech1_prds)))

    for rxn in mech2_dct:
        [mech2_rcts, mech2_prds] = rxn
        if mech2_rcts in mech1_rct_comb and mech2_prds in mech1_prd_comb:
            flip_rxn = False
            mech2_key = rxn
            break
        elif mech2_rcts in mech1_prd_comb and mech2_prds in mech1_rct_comb:
            mech2_key = rxn
            flip_rxn = True
            break
        else:
            mech2_key = ()
            flip_rxn = None

    ret = mech2_key, flip_rxn

    return ret


def _reverse_reaction_rates(mech_dct, thermo_dct, rxn, temps):
    """ use the equilibrium constant to reverse the reaction rates
    """

    [rct_idxs, prd_idxs] = rxn
    k_equils = _calculate_equilibrium_constant(
        thermo_dct, rct_idxs, prd_idxs, temps)

    ktp_dct = mech_dct[rxn]
    rev_ktp_dct = {}
    for pressure, rate_ks in ktp_dct.items():
        rev_rates = []
        for rate_k, k_equil in zip(rate_ks, k_equils):
            rev_rates.append(rate_k / k_equil)
        rev_ktp_dct[pressure] = rev_rates

    return rev_ktp_dct


def _calculate_equilibrium_constant(thermo_dct, rct_idxs, prd_idxs, temps):
    """ use the thermo parameters to obtain the equilibrium
        constant
    """

    k_equils = []
    for temp_idx, temp in enumerate(temps):
        rct_gibbs = 0.0
        for rct in rct_idxs:
            rct_gibbs += _grab_gibbs(thermo_dct[rct], temp_idx)
        prd_gibbs = 0.0
        for prd in prd_idxs:
            prd_gibbs += _grab_gibbs(thermo_dct[prd], temp_idx)

        rxn_gibbs = prd_gibbs - rct_gibbs

        k_equils.append(
            np.exp(-rxn_gibbs / (RC * temp)))

    return k_equils


def _grab_gibbs(thermo_vals, temp_idx):
    """ calculate the Gibbs Free energy value
    """
    gibbs = thermo_vals[3][temp_idx]
    return gibbs


# Functions to build dictionaries
def build_reaction_name_dcts(mech1_str, mech2_str, t_ref, temps, pressures):
    """ builds the reaction dictionaries indexed by names
    """

    mech1_reaction_block = chemkin_io.parser.util.clean_up_whitespace(
        chemkin_io.parser.mechanism.reaction_block(mech1_str))
    mech1_units = reaction_units(mech1_str)
    mech1_ktp_dct = rates.mechanism(
        mech1_reaction_block, mech1_units, t_ref, temps, pressures)

    mech2_reaction_block = chemkin_io.parser.util.clean_up_whitespace(
        chemkin_io.parser.mechanism.reaction_block(mech2_str))
    mech2_units = reaction_units(mech2_str)
    mech2_ktp_dct = rates.mechanism(
        mech2_reaction_block, mech2_units, t_ref, temps, pressures)

    return mech1_ktp_dct, mech2_ktp_dct


def build_reaction_inchi_dcts(mech1_str, mech2_str,
                              mech1_csv_str, mech2_csv_str,
                              t_ref, temps, pressures):
    """ builds new reaction dictionaries indexed by inchis
    """
    # Get dicts: dict[name] = rxn_dstr
    mech1_reaction_dct, mech2_reaction_dct = build_reaction_name_dcts(
        mech1_str, mech2_str, t_ref, temps, pressures)

    # Get dicts: dict[name] = inchi
    mech1_name_inchi_dct = chemkin_io.parser.mechanism.spc_name_dct(
        mech1_csv_str, 'inchi')
    mech2_name_inchi_dct = chemkin_io.parser.mechanism.spc_name_dct(
        mech2_csv_str, 'inchi')

    # Convert name dict to get: dict[inchi] = rxn_data
    mech1_reaction_ich_dct = {}
    for names, data in mech1_reaction_dct.items():
        [rct_names, prd_names] = names
        rct_ichs, prd_ichs = (), ()
        for rcts in rct_names:
            rct_ichs += ((mech1_name_inchi_dct[rcts]),)
        for prds in prd_names:
            prd_ichs += ((mech1_name_inchi_dct[prds]),)
        mech1_reaction_ich_dct[(rct_ichs, prd_ichs)] = data

    mech2_reaction_ich_dct = {}
    for names, data in mech2_reaction_dct.items():
        [rct_names, prd_names] = names
        rct_ichs, prd_ichs = (), ()
        for rcts in rct_names:
            rct_ichs += ((mech2_name_inchi_dct[rcts]),)
        for prds in prd_names:
            prd_ichs += ((mech2_name_inchi_dct[prds]),)
        mech2_reaction_ich_dct[(rct_ichs, prd_ichs)] = data

    return mech1_reaction_ich_dct, mech2_reaction_ich_dct


def conv_ich_to_name_ktp_dct(ktp_ich_dct, csv_str):
    """ convert ktp dct from using ichs to using names
    """
    # Get dicts: dict[name] = inchi
    mech1_inchi_name_dct = chemkin_io.parser.mechanism.spc_inchi_dct(
        csv_str)

    # Convert name dict to get: dict[inchi] = rxn_data
    ktp_name_dct = {}
    for ichs, params in ktp_ich_dct.items():
        [rct_ichs, prd_ichs] = ichs
        rct_names, prd_names = (), ()
        for rcts in rct_ichs:
            rct_names += ((mech1_inchi_name_dct[rcts]),)
        for prds in prd_ichs:
            prd_names += ((mech1_inchi_name_dct[prds]),)
        ktp_name_dct[(rct_names, prd_names)] = params

    return ktp_name_dct

# def spc_name_from_inchi(mech1_csv_str, mech2_csv_str, ich_pair):
#     """ uses dict[inchi]=name dicts to get
#         the mechanism name for a given InChI string
#     """
#    mech1_inchi_dct = chemkin_io.parser.mechanism.spc_inchi_dct(mech1_csv_str)
#    mech2_inchi_dct = chemkin_io.parser.mechanism.spc_inchi_dct(mech2_csv_str)
#
#     if ich in mech1_inchi_dct:
#        mech_name = mech1_inchi_dct[ich]
#     else:
#         mech_name = mech2_inchi_dct[ich]
#
#     return mech_name
