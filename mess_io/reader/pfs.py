"""
  Reads the output of a MESSPF calculation for the
  partition functions and their derivatives
"""


def partition_fxn(output_string):
    """ Reads the parition function from the MESSPF output
        :param str output_string: string of lines for MESSPF output file
        :return temps: List of temperatures
        :rtype: list: float
        :return logq:  loq(Q) where Q is partition function
        :rtype: list: float
        :return dq_dt: dQ/dT; 1st deriv. of Q w/r to temperature
        :rtype: list: float
        :return dq2_dt2: d^2Q/dT^2; 2nd deriv. of Q w/r to temperature
        :rtype: list: float
    """

    # Read the partition function and derivatives
    temps, logq, dq_dt, dq2_dt2 = [], [], [], []
    for i, line in enumerate(output_string.splitlines()):
        if i not in (0, 1):
            tmp = line.strip().split()
            temps.append(float(tmp[0]))
            logq.append(float(tmp[1]))
            dq_dt.append(float(tmp[2]))
            dq2_dt2.append(float(tmp[3]))

    return temps, logq, dq_dt, dq2_dt2
