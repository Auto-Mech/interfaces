"""
 Functions which write useful strings for MESS.
"""


def rxnchan_header_str():
    """ Returns a string that is a header for species in the MESS input file.

        :rtype: str
    """
    mstr = (
        '!===================================================\n'
        '!  REACTION CHANNELS SECTION\n'
        '!==================================================='
    )

    return mstr


def species_separation_str():
    """ Returns a string used to separate species in the MESS input file.

        :rtype: str
    """
    mstr = '!***************************************************'

    return mstr
