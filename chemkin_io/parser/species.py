""" functions operating on the species block string
"""

import autoparse.find as apf


def names(block_str, exclude_names=()):
    """ Parses the names of species from the species block 
        of the mechanism input file.
        :param string block_str: string for species block
        :param exclude_names: names of species to ignore during parsing
        :return spc_names: names of species that were not excluded
        :rtype: tuple
    """
    spc_names = apf.split_words(block_str)
    spc_names = tuple(filter(lambda x: x not in exclude_names, spc_names))
    return spc_names
