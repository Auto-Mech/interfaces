"""
 Functions which write useful strings for MESS
"""


def rxnchan_header_str():
    """ Write a string that separates various species
    """
    mstr = (
        '!+++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        '!  REACTION CHANNELS SECTION\n'
        '!+++++++++++++++++++++++++++++++++++++++++++++++++++'
    )
    return mstr


def species_separation_str():
    """ Write a string that separates various species
    """
    mstr = '!***************************************************'
    return mstr
