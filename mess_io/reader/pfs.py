"""
  Reads the output of a MESSPF calculation for the
  partition functions and their derivatives
  corresponding to one species.
"""


def partition_fxn(output_str):
    """ Parses the MESSPF output file string for the parition function
        and related information for a single species.


        :param output_str: string of lines for MESSPF output file
        :type output_str: str
        :return temps: List of temperatures
        :rtype: float(list)
        :return logq:  loq(Q) where Q is partition function
        :rtype: float(list)
        :return dq_dt: dQ/dT; 1st deriv. of Q w/r to temperature
        :rtype: float(list)
        :return dq2_dt2: d^2Q/dT^2; 2nd deriv. of Q w/r to temperature
        :rtype: float(list)
    """

    temps, logq, dq_dt, dq2_dt2 = [], [], [], []
    for i, line in enumerate(output_str.splitlines()):
        if i not in (0, 1):
            tmp = line.strip().split()
            temps.append(float(tmp[0]))
            logq.append(float(tmp[1]))
            dq_dt.append(float(tmp[2]))
            dq2_dt2.append(float(tmp[3]))

    return temps, logq, dq_dt, dq2_dt2
