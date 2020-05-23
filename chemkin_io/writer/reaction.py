"""
Writes strings containing the rate parameters
"""


# Functions to write the parameters in the correct format
def troe(reaction, high_params, low_params, troe_params, colliders=()):
    """ Write the string containing the Lindemann fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param low_params: Arrhenius Fitting Parameters used for low-P
        :type low_params: list(float)
        :param troe_params: Troe alpha, T1, T2, and T3 fitting parameters
        :type troe_params: list(float)
        :param colliders: names and collision enhancement factors for bath spc
        :type colliders: list((str, float))
        :return troe_str: ChemKin reaction string with Troe parameters
        :rtype: str
    """

    assert len(high_params) == 3
    assert len(low_params) == 3
    assert len(troe_params) in (3, 4)

    [high_a, high_n, high_ea] = high_params

    # Write reaction header (with third body added) and high-pressure params
    reaction = _format_rxn_str_for_pdep(reaction, press='all')
    troe_str = '{0:<32s}{1:>10.3E}{2:>9.3f}{3:9.0f} /\n'.format(
        reaction, high_a, high_n, 1000*high_ea)

    # Write the collider efficiencies string
    if colliders:
        troe_str += _format_collider_string(colliders)

    # Now write the low-pressure and Troe params
    troe_str += _format_params_string('LOW', low_params, newline=True)
    troe_str += _format_params_string('TROE', troe_params, newline=False)

    return troe_str


def lindemann(reaction, high_params, low_params, colliders=()):
    """ Write the string containing the Lindemann fitting parameters
        formatted for ChemKin input files

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param low_params: Arrhenius Fitting Parameters used for low-P
        :type low_params: list(float)
        :param colliders: names and collision enhancement factors for bath spc
        :type colliders: list((str, float))
        :return lind_str: ChemKin reaction string with Lindemann parameters
        :rtype: str
    """
    [high_a, high_n, high_ea] = high_params

    # Write reaction header (with third body added) and high-pressure params
    reaction = _format_rxn_str_for_pdep(reaction, press='low')
    lind_str = '{0:<32s}{1:>10.3E}{2:>9.3f}{3:9.0f} /\n'.format(
        reaction, high_a, high_n, 1000*high_ea)

    # Write the collider efficiencies string
    if colliders:
        lind_str += _format_collider_string(colliders)

    # Now write the low-pressure and Troe params
    lind_str += _format_params_string('LOW', low_params, newline=False)

    return lind_str


def plog(reaction, rate_params_dct, temp_dct=None, err_dct=None):
    """ Write the string containing the PLOG fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param rate_params_dct: Arrhenius fitting parameters at each pressure
        :type rate_params_dct: dict[pressure: [rate params]]
        :param temp_dct: temperature ranges for fits at each pressure
        :type temp_dct: dict[pressure: [temps]]
        :param err_dct: mean and max ftting errors at each pressure
        :type err_dct: dict[pressure: [errs]]
        :return plog_str: ChemKin reaction string with PLOG parameters
        :rtype: str
    """

    # Find nparams and ensure there are correct num in each dct entry
    nparams = len(next(iter(rate_params_dct.values())))
    assert nparams in (3, 6)
    assert all(len(params) == nparams for params in rate_params_dct.values())

    # Obtain a list of the pressures and sort from low to high pressure
    pressures = [pressure for pressure in rate_params_dct.keys()
                 if pressure != 'high']
    pressures.sort()

    # Add fake high pressure parameters if they are not in the dictionary
    if 'high' not in rate_params_dct:
        if nparams == 3:
            rate_params_dct['high'] = [1.00, 0.00, 0.00]
        elif nparams == 6:
            rate_params_dct['high'] = [1.00, 0.00, 0.00, 1.00, 0.00, 0.00]

    # Build the reaction string with high-pressure params and any plog params
    # Loop will build second ('DUPLICATE') section if double fit performed
    p_str = ''
    for i in range(nparams // 3):
        if i == 1:
            p_str += 'DUPLICATE\n'

        # Build the initial string with the reaction and high-pressure params
        high_a, high_n, high_ea = rate_params_dct['high'][3*i:3*i+3]
        p_str += '{0:<32s}{1:>10.3E}{2:>9.3f}{3:9.0f} /\n'.format(
            reaction, high_a, high_n, 1000*high_ea)

        # Build the PLOG string for each pressure, other than the HighP Limit
        for pressure in pressures:
            pdep_a, pdep_n, pdep_ea = rate_params_dct[pressure][3*i:3*i+3]
            p_str += '{0:>18s} /{1:>10.3f}  '.format(
                'PLOG', float(pressure))
            p_str += '{0:>10.3E}{1:>9.3f}{2:9.0f} /\n'.format(
                pdep_a, pdep_n, 1000*pdep_ea)

    # Write string showing the temp fit range and fit errors
    if temp_dct or err_dct:
        p_str += _fit_info_str(pressures, temp_dct, err_dct)

    return p_str


def chebyshev(reaction, high_params, alpha, tmin, tmax, pmin, pmax):
    """ Write the string containing the Chebyshev fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param alpha: Chebyshev coefficient matrix
        :type alpha: numpy.ndarray
        :param tmin: minimum temperature Chebyshev model is defined
        :type tmin: float
        :param tmax: maximum temperature Chebyshev model is defined
        :type tmax: float
        :param pmin: minimum pressure Chebyshev model is defined
        :type pmin: float
        :return cheb_str: ChemKin reaction string with Chebyshev parameters
        :rtype: str
    """
    assert len(high_params) == 3
    # assert alpha mat is a 2d matrix

    [high_a, high_n, high_ea] = high_params

    # Write reaction header (with third body added) and high-pressure params
    reaction = _format_rxn_str_for_pdep(reaction, press='all')
    cheb_str = '{0:<32s}{1:>10.3E}{2:>9.3f}{3:9.0f} /\n'.format(
        reaction, high_a, high_n, 1000*high_ea)

    # Write the temperature and pressure ranges
    cheb_str += _format_params_string('TCHEB', (tmin, tmax), newline=True)
    cheb_str += _format_params_string('PCHEB', (pmin, pmax), newline=True)

    # Write the dimensions of the alpha matrix
    nrows = len(alpha)
    ncols = len(alpha[0])
    cheb_str += '{0:>10s}/    {1:d} {2:d}\n'.format('CHEB', nrows, ncols)

    # Write the parameters from the alpha matrix
    for idx, row in enumerate(alpha):
        newline = bool(idx+1 != nrows)
        cheb_str += _format_params_string('CHEB', row, newline=newline)

    return cheb_str


# Various formatting functions
def _fit_info_str(pressures, temp_dct, err_dct):
    """ Write the string detailing the temperature ranges and fitting errors
        associated with the rate-constant fits at each pressure.

        :param pressures: pressures the k(T,P)s were calculated at
        :type pressures: list(float)
        :param temp_dct: temperature ranges (K) fits were done at each pressure
        :type temp_dct: dict[pressure, [temp range]]
        :param err_dct: errors associated with the fits at each pressure
        :type err_dct: dict[pressure, [mean err, max err]]
        :return inf_str: string containing all of the fitting info
        :rtype: str
    """

    # Make temp, err dcts empty if fxn receives None; add 'high' to pressures
    temp_dct = temp_dct if temp_dct else {}
    err_dct = err_dct if err_dct else {}
    if 'high' in temp_dct or 'high' in err_dct:
        pressures += ['high']

    # Check the temp and err dcts have same presures as rate_dcts
    if temp_dct:
        assert set(pressures) == set(temp_dct.keys())
    err_dct = err_dct if err_dct else {}
    if err_dct:
        assert set(pressures) == set(err_dct.keys())

    # Write string showing the temp fit range and fit errors
    inf_str = '! Info Regarding Rate Constant Fits\n'
    for pressure in pressures:
        if temp_dct:
            [min_temp, max_temp] = temp_dct[pressure]
            temps_str = '{0:.0f}-{1:.0f} K'.format(
                min_temp, max_temp)
            temp_range_str = 'Temps: {0:>12s}, '.format(
                temps_str)
        else:
            temp_range_str = ''
        if err_dct:
            [mean_err, max_err] = err_dct[pressure]
            err_str = '{0:11s} {1:>5.1f}%,  {2:7s} {3:>5.1f}%'.format(
                'MeanAbsErr:', mean_err, 'MaxErr:', max_err)
        else:
            err_str = ''

        # Put together the who info string
        if pressure != 'high':
            pstr = '{0:<9.3f}'.format(pressure)
        else:
            pstr = '{0:<9s}'.format('High')
        inf_str += '! Pressure: {0} {1} {2}\n'.format(
            pstr, temp_range_str, err_str)

    return inf_str


def _format_rxn_str_for_pdep(reaction, pressure='all'):
    """ Add the bath gas M species to the reaction string for 
        pressure dependent reactions in the appropriate format.

        :param reaction: chemical equation for the reaction
        :type reaction: str
        :param pressure: signifies the level of pressure dependence
        :type pressure: str
        :return: three_body_reaction: chemical equation with M body
        :rtype: str
    """
    # Determine format of M string to be added to reaction string
    assert pressure in ('low', 'all')
    if pressure == 'all':
        m_str = ' (+M)'
    else:
        m_str = ' + M'

    # Add the M string to both sides of the reaction string
    [lhs, rhs] = reaction.split('=')
    three_body_reaction = lhs + m_str + ' = ' + rhs + m_str

    return three_body_reaction


def _format_collider_string(colliders):
    """ Write the string for the bath gas collider and their efficiencies
        for the Lindemann and Troe functional expressions:

        :param colliders:
        :type colliders: list(str)
        :return: collider_str: ChemKin-format string with colliders
        :rtype: str
    """

    collider_str = ''.join(
        ('{0:s}/{1:4.3f}/ '.format(collider[0], collider[1])
         for collider in colliders))
    collider_str += '\n'

    return collider_str


def _format_params_string(header, params, newline=False):
    """ Write a string containing fitting params used for several
        functional forms.

        :param header: name of functional form the parameters correspond to 
        :type header: str
        :param params: fitting parameters
        :type params: list(float)
        :param newline: signals whether to add a newline
        :type newline: bool
        :return: params_str: string containing the parameters
        :rtype: str
    """
    params_str = '{0:>10s}/ '.format(header.upper())
    params_str += ''.join(('{0:12.3E}'.format(param) for param in params))
    params_str += ' /'
    if newline:
        params_str += '\n'

    return params_str
