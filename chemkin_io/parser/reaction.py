""" functions operating on the reactions block string
"""


import itertools
import numpy
import autoparse.pattern as app
import autoparse.find as apf
from autoparse import cast as ap_cast
from ioformat import headlined_sections


# Various strings needed to parse the data sections of the Reaction block
CHEMKIN_ARROW = (app.maybe(app.escape('<')) + app.escape('=') +
                 app.maybe(app.escape('>')))
CHEMKIN_PLUS_EM = app.PLUS + 'M'
CHEMKIN_PAREN_PLUS_EM = app.escape('(') + app.PLUS + 'M' + app.escape(')')

SPECIES_NAME_PATTERN = (
    r'[^\s=+\-]' +
    app.zero_or_more(app.one_of_these(
        [app.LETTER, app.DIGIT, app.escape('(+)'), r'[#,()\-]',
         app.escape('['), app.escape(']')])) +
    app.zero_or_more(app.PLUS)
)
SPECIES_NAMES_PATTERN = app.series(
    app.padded(SPECIES_NAME_PATTERN), app.padded(app.PLUS))

REACTION_PATTERN = (SPECIES_NAMES_PATTERN + app.padded(CHEMKIN_ARROW) +
                    SPECIES_NAMES_PATTERN)
COEFF_PATTERN = (app.NUMBER + app.LINESPACES + app.NUMBER +
                 app.LINESPACES + app.NUMBER)

BAD_STRS = ['inf', 'INF', 'nan']


# Functions which use thermo parsers to collate the data
def data_block(block_str):
    """ Parses all of the chemical equations and corresponding fitting
        parameters in the reactions block of the mechanism input file
        and subsequently pulls all of the species names and fitting
        parameters from the data string; this information is stored in a list.

        :param block_str: string for reactions block
        :type block_str: str
        :return data_block: all the data from the data string for each reaction
        :rtype: list(list(str))
    """

    rxn_dstr_lst = data_strings(block_str)
    rxn_dat_lst = tuple(zip(
        map(reactant_names, rxn_dstr_lst),
        map(product_names, rxn_dstr_lst),
        map(high_p_parameters, rxn_dstr_lst),
        map(low_p_parameters, rxn_dstr_lst),
        map(troe_parameters, rxn_dstr_lst),
        map(chebyshev_parameters, rxn_dstr_lst),
        map(plog_parameters, rxn_dstr_lst),
        map(buffer_enhance_factors, rxn_dstr_lst)))

    return rxn_dat_lst


def data_dct(block_str, data_entry='strings', remove_bad_fits=False):
    """ Parses all of the chemical equations and corresponding fitting
        parameters in the reactions block of the mechanism input file
        and stores them in a dictionary.

        :param block_str: string for reactions block
        :type block_str: str
        :return data_dct: dictionary of all the reaction data strings
        :rtype: dict[reaction: data string]
    """

    rxn_dstr_lst = data_strings(block_str, remove_bad_fits=remove_bad_fits)
    if data_entry == 'strings':
        rxn_dct = {}
        for string in rxn_dstr_lst:
            # print(string)
            rct_names = reactant_names(string)
            prd_names = product_names(string)
            key = (rct_names, prd_names)
            if key not in rxn_dct:
                rxn_dct[key] = string
            else:
                rxn_dct[key] += '\n'+string
    # elif data_entry == 'block':
    #     rxn_dct = {}
    #     for block in rxn_block_lst:
    #         param_blocks = []
    #         rct_names = rxn_block_lst[0]
    #         prd_names = rxn_block_lst[1]
    #         key = (rct_names, prd_names)
    #         if key not in rxn_dct.keys():
    #             rxn_dct[key] = block[2:]
    #         else:
    #             rxn_dct[key]

    return rxn_dct


# Functions for parsing the reactuins block or single reaction string #
def data_strings(block_str, remove_bad_fits=False):
    """ Parses all of the chemical equations and corresponding fitting
        parameters in the reactions block of the mechanism input file
        and stores them in a list.

        :param block_str: string for reactions block
        :type block_str: str
        :param remove_bad_fits: remove reactions with bad fits
        :type remove_bad_fits: bool
        :return rxn_dstrs: strings containing eqns and params for all reactions
        :rtype: list(str)
    """

    rxn_dstrs = headlined_sections(
        string=block_str.strip(),
        headline_pattern=CHEMKIN_ARROW
    )

    if remove_bad_fits:
        rxn_dstrs = [dstr for dstr in rxn_dstrs
                     if not any(string in dstr for string in BAD_STRS)]
    return rxn_dstrs


def reactant_names(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the line containing the chemical equation in order to
        read the names of the reactant species.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return names: names of the reactants
        :rtype: list(str)
    """

    pattern = _first_line_pattern(
        rct_ptt=app.capturing(SPECIES_NAMES_PATTERN),
        prd_ptt=SPECIES_NAMES_PATTERN,
        param_ptt=COEFF_PATTERN
    )
    string = apf.first_capture(pattern, rxn_dstr)
    names = _split_reagent_string(string)

    return names


def product_names(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the line containing the chemical equation in order to
        read the names of the product species.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return names: names of the products
        :rtype: list(str)
    """

    pattern = _first_line_pattern(
        rct_ptt=SPECIES_NAMES_PATTERN,
        prd_ptt=app.capturing(SPECIES_NAMES_PATTERN),
        param_ptt=COEFF_PATTERN
    )
    string = apf.first_capture(pattern, rxn_dstr)
    names = _split_reagent_string(string)

    return names


def high_p_parameters(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the line containing the chemical equation in order to
        read the fitting parameters that are on the same line.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return params: Arrhenius fitting parameters for high-P rates
        :rtype: list(float)
    """

    pattern = _first_line_pattern(
        rct_ptt=SPECIES_NAMES_PATTERN,
        prd_ptt=SPECIES_NAMES_PATTERN,
        param_ptt=app.capturing(COEFF_PATTERN)
    )

    string_lst = apf.all_captures(pattern, rxn_dstr)
    if string_lst:
        params = []
        for string in string_lst:
            params.append(list(ap_cast(string.split())))
    else:
        params = None

    return params


def are_highp_fake(highp_params):
    """ Assess whether high-pressure parameters parsed out of a reac
        string are fake.
    """

    are_fake = False
    for params in highp_params:
        if numpy.allclose(params, [1.0, 0.0, 0.0], atol=0.0000001):
            are_fake = True

    return are_fake


def low_p_parameters(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for a line containing the low-pressure fitting parameters,
        then reads the parameters from this line.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return params: Arrhenius fitting parameters for low-P rates
        :rtype: list(float)
    """

    pattern = (
        'LOW' +
        app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    cap1 = apf.first_capture(pattern, rxn_dstr)
    if cap1 is not None:
        params = [[float(val) for val in cap1]]
    else:
        params = None

    return params


def troe_parameters(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for a line containing the Troe fitting parameters,
        then reads the parameters from this line.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return params: Troe fitting parameters
        :rtype: list(float)
    """

    pattern1 = (
        'TROE' +
        app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.maybe(app.capturing(app.NUMBER)) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    pattern2 = (
        'TROE' +
        app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.SPACES + app.capturing(app.NUMBER) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    cap1 = apf.first_capture(pattern1, rxn_dstr)
    cap2 = apf.first_capture(pattern2, rxn_dstr)
    if cap1 is not None:
        params = [float(val) for val in cap1]
    else:
        if cap2 is not None:
            params = [float(val) for val in cap2]
            params.append(None)
        else:
            params = None

    return params


def chebyshev_parameters(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the lines containing the Chebyshevs fitting parameters,
        then reads the parameters from these lines.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return params: Chebyshev fitting parameters
        :rtype: dict[param: value]
    """

    temp_pattern = (
        'TCHEB' + app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.FLOAT) +
        app.SPACES + app.capturing(app.FLOAT) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    pressure_pattern = (
        'PCHEB' + app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.FLOAT) +
        app.SPACES + app.capturing(app.FLOAT) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    alpha_dimension_pattern = (
        'CHEB' + app.zero_or_more(app.SPACE) + app.escape('/') +
        app.SPACES + app.capturing(app.INTEGER) +
        app.SPACES + app.capturing(app.INTEGER) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    alpha_elements_pattern = (
        'CHEB' + app.zero_or_more(app.SPACE) + app.escape('/') +
        app.series(
            app.capturing(app.SPACES + app.capturing(app.EXPONENTIAL_FLOAT)),
            app.SPACES
        ) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )

    cheb_temps = apf.first_capture(temp_pattern, rxn_dstr)
    cheb_pressures = apf.first_capture(pressure_pattern, rxn_dstr)
    alpha_dims = apf.first_capture(alpha_dimension_pattern, rxn_dstr)
    alpha_elm = apf.all_captures(alpha_elements_pattern, rxn_dstr)
    if not alpha_elm:
        alpha_elm = None

    params_dct = {}
    if all(vals is not None
           for vals in (cheb_temps, cheb_pressures, alpha_dims, alpha_elm)):
        params_dct['t_limits'] = [float(val) for val in cheb_temps]
        params_dct['p_limits'] = [float(val) for val in cheb_pressures]
        params_dct['alpha_dim'] = [int(val) for val in alpha_dims]
        params_dct['alpha_elm'] = [list(map(float, row)) for row in alpha_elm]
    else:
        params_dct = None

    return params_dct


def plog_parameters(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the lines containing the PLog fitting parameters,
        then reads the parameters from these lines.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return params: PLog fitting parameters
        :rtype: dict[pressure: params]
    """

    pattern = (
        'PLOG' +
        app.zero_or_more(app.SPACE) + app.escape('/') +
        app.zero_or_more(app.SPACE) + app.capturing(app.NUMBER) +
        app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
        app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
        app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
        app.zero_or_more(app.SPACE) + app.escape('/')
    )
    params_lst = apf.all_captures(pattern, rxn_dstr)

    # Build dictionary of parameters, indexed by parameter
    if params_lst:
        params_dct = {}
        for params in params_lst:
            pressure = float(params[0])
            vals = list(map(float, params[1:]))
            if pressure not in params_dct:
                params_dct[pressure] = [vals]
            else:
                params_dct[pressure].append(vals)
    else:
        params_dct = None

    return params_dct


def buffer_enhance_factors(rxn_dstr):
    """ Parses the data string for a reaction in the reactions block
        for the line containing the names of several bath gases and
        their corresponding collision enhancement factors.

        :param rxn_dstr: data string for species in reaction block
        :type rxn_dstr: str
        :return factors: Collision enhanncement factors for each bath gas
        :rtype: dict[bath name: enhancement factors]
    """

    first_str = _first_line_pattern(
        rct_ptt=SPECIES_NAMES_PATTERN,
        prd_ptt=SPECIES_NAMES_PATTERN,
        param_ptt=COEFF_PATTERN)
    bad_strings = ('DUP', 'LOW', 'TROE', 'CHEB', 'PLOG', first_str)

    species_char = app.one_of_these([
        app.LETTER, app.DIGIT,
        app.escape('('), app.escape(')'),
        app.UNDERSCORE])
    species_name = app.one_or_more(species_char)

    # Loop over the lines and search for string with collider facts
    factors = None
    if apf.has_match('LOW', rxn_dstr) or apf.has_match('TROE', rxn_dstr):
        for line in rxn_dstr.splitlines():
            if not any(apf.has_match(string, line) for string in bad_strings):
                factor_pattern = (
                    app.capturing(species_name) +
                    app.escape('/') + app.maybe(app.SPACE) +
                    app.capturing(app.NUMBER) +
                    app.escape('/')
                )
                baths = apf.all_captures(factor_pattern, line)
                if baths:
                    factors = {}
                    for bath in baths:
                        factors[bath[0]] = float(bath[1])

    return factors


def ratek_fit_info(rxn_dstr):
    """ Read the information describing features of the fits to the
        rate constants
    """

    # Read the temperatures and the Errors from the lines
    pressure_ptt = (
        'Pressure:' + app.SPACES +
        app.capturing(app.one_of_these([app.FLOAT, 'High']))
    )
    trange_ptt = (
        'Temps: ' + app.SPACES +
        app.capturing(app.INTEGER) + '-' + app.capturing(app.INTEGER) +
        app.SPACES + 'K'
    )
    mean_ptt = (
        'MeanAbsErr:' + app.SPACES +
        app.capturing(app.FLOAT) + app.escape('%') +
        ','
    )
    max_ptt = (
        'MaxErr:' + app.SPACES +
        app.capturing(app.FLOAT) + app.escape('%')
    )
    pressure_caps = apf.all_captures(pressure_ptt, rxn_dstr)
    trange_caps = apf.all_captures(trange_ptt, rxn_dstr)
    mean_caps = apf.all_captures(mean_ptt, rxn_dstr)
    max_caps = apf.all_captures(max_ptt, rxn_dstr)

    pressures = []
    for pressure in pressure_caps:
        if pressure != 'High':
            pressures.append(float(pressure))
        elif pressure == 'High':
            pressures.append(pressure)
    trange_vals = []
    for cap in trange_caps:
        temp1, temp2 = cap
        trange_vals.append([int(temp1), int(temp2)])
    if mean_caps is not None:
        mean_vals = [float(val) for val in mean_caps]
    else:
        mean_vals = []
    if max_caps is not None:
        max_vals = [float(val) for val in max_caps]
    else:
        max_vals = []

    # Build the inf_dct
    inf_dct = {}
    print(rxn_dstr)
    for idx, pressure in enumerate(pressures):
        print(pressure)
        inf_dct[pressure] = {'temps': trange_vals[idx]}
        if mean_vals:
            inf_dct[pressure].update({'mean_err': mean_vals[idx]})
        if max_vals:
            inf_dct[pressure].update({'max_err': max_vals[idx]})

    return inf_dct


# HELPER FUNCTIONS #
def _first_line_pattern(rct_ptt, prd_ptt, param_ptt):
    """ Defines the pattern for the first line in a reaction data
        string that contains the chemical equation and high-pressure
        fitting parameters for the reaction.

        :param rct_ptt: string pattern for the reactant species
        :type rct_ptt: str
        :param prd_ptt: string pattern for the product species
        :type prd_ptt: str
        :param param_ptt: string pattern for high-pressure parameters
        :type param_ptt: str
        :rtype: str
    """
    return (rct_ptt + app.padded(CHEMKIN_ARROW) + prd_ptt +
            app.LINESPACES + param_ptt)


def _split_reagent_string(rgt_str):
    """ Parses out the names of all the species given in a string with
        the chemical equation within the reactions block.

        :param rgt_str: string with the reaction chemical equation
        :type rgt_str: str
        :return rgts: names of the species in the reaction
        :type rgts: list(str)
    """

    def _interpret_reagent_count(rgt_cnt_str):
        """ Count the species in a string containing one side
            of a chemical rquation.

            :param rgt_cnt_str: string of one side of chemcial equation
            :type rgt_cnt_str: str
            :return: rgts: names of species from string
            :rtype: list(str)
        """
        _pattern = (app.STRING_START + app.capturing(app.maybe(app.DIGIT)) +
                    app.capturing(app.one_or_more(app.NONSPACE)))
        cnt, rgt = apf.first_capture(_pattern, rgt_cnt_str)
        cnt = int(cnt) if cnt else 1
        rgts = (rgt,) * cnt
        return rgts

    rgt_str = apf.remove(app.LINESPACES, rgt_str)
    rgt_str = apf.remove(CHEMKIN_PAREN_PLUS_EM, rgt_str)
    rgt_str = apf.remove(CHEMKIN_PLUS_EM, rgt_str)
    pattern = app.PLUS + app.not_followed_by(app.PLUS)
    rgt_cnt_strs = apf.split(pattern, rgt_str)
    rgts = tuple(itertools.chain(*map(_interpret_reagent_count, rgt_cnt_strs)))

    return rgts
