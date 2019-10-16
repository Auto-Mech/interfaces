"""
Calculate rates with various fitting functions
"""

import numpy as np


def calc_sse_and_mae(calc_ks, fit_ks):
    """ (1) get the sum of square error (SSE) useful when determining
            which double plog routine will be used to initialize
            the nonlinear solver
        (2) also get the mean absolute error (MAE), which is written
            to the plog file
    """

    # Only run if there are more than 2 rate constants
    #sse = 0.0
    abs_err = []
    if len(calc_ks) > 2:
        for calc_k, fit_k in zip(calc_ks, fit_ks):
            #sse += (np.log(calc_k) - np.log(fit_k))**2.0
            abs_err.append(np.abs((calc_k - fit_k) / calc_k))
        abs_err = np.array(abs_err, dtype=np.float64)
        mean_abs_err = np.mean(abs_err) * 100.0
        max_abs_err = np.max(abs_err) * 100.0
    else:
        #sse = None
        mean_abs_err = None
        max_abs_err = None

    return mean_abs_err, max_abs_err


def assess_pressure_dependence(tk_dct, assess_pdep_temps,
                               tolerance=20.0, plow=None, phigh=None):
    """ Assess how much the rate constants change from
        a low-pressure to high-pressure regime

        tk_dct[pressure] = [temps, k(T, P)s]
        we assume the temps and pressures give all positive, defined rates
    """
    # Get list of the sorted pressures, ignoring the high-pressure limit rates
    pressures = [pressure for pressure in tk_dct
                 if pressure != 'high']
    pressures.sort()

    # Set the low- and high-pressure if not specified by user
    if plow is None:
        plow = min(pressures)
    if phigh is None:
        phigh = max(pressures)

    # Check % difference for k(T, P) vals
    is_pressure_dependent = False
    for temp_compare in assess_pdep_temps:
        # For the low- and high-P, find the idx for the temp in temp_compare
        temps_low = tk_dct[plow][0]
        temps_high = tk_dct[phigh][0]
        temp_low_idx = np.where(np.isclose(temps_low, temp_compare))[0][0]
        temp_high_idx = np.where(np.isclose(temps_high, temp_compare))[0][0]
        # Grab the k(T, P) vale for the approprite temp and pressure
        ktp_low = tk_dct[plow][1][temp_low_idx]
        ktp_high = tk_dct[phigh][1][temp_high_idx]
        # Calculate the % difference and see if above threshold
        ktp_dif = (abs(ktp_low - ktp_high) / ktp_low) * 100.0
        if ktp_dif > tolerance:
            is_pressure_dependent = True

    return is_pressure_dependent
