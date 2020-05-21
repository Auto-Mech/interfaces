""" functions operating on the thermo block string
"""


import autoparse.pattern as app
import autoparse.find as apf
from chemkin_io.parser.util import headlined_sections


RC = 1.98720425864083e-3  # in kcal/mol.K


# Functions which use thermo parsers to collate the data
def data_block(block_str):
    """ find all thermo data
    """
    thm_dstr_lst = data_strings(block_str)
    thm_dat_lst = tuple(zip(
        map(species_name, thm_dstr_lst),
        map(temperatures, thm_dstr_lst),
        map(low_coefficients, thm_dstr_lst),
        map(high_coefficients, thm_dstr_lst)))
    return thm_dat_lst


def data_dct(block_str, data_entry='strings'):
    """ build a dictionary indexes by the species' CHEMKIN mechanism name
        contains block entry
    """

    if data_entry == 'strings':
        thm_data_lst = data_strings(block_str)
        names = map(species_name, thm_data_lst)
        therm_dct = dict(zip(names, thm_data_lst))
    elif data_entry == 'block':
        thm_data_lst = data_block(block_str)
        names = thm_data_lst[0]
        therm_dct = dict(zip(names, thm_data_lst))
    else:
        raise NotImplementedError

    return therm_dct


# Functions for parsing the thermo block or single polyn string #
def data_strings(block_str):
    """ Parse all of the NASA polynomials given in the thermo block
        of the mechanism input file.

        :param block_str: string for thermo block
        :type block_str: str
        :return thm_strs: strings containing NASA polynomials for all species
        :rtype: list(str)
    """

    headline_pattern = (
        app.LINE_START + app.not_followed_by(app.one_of_these(
            [app.DIGIT, app.PLUS, app.escape('=')])) +
        app.one_or_more(app.NONNEWLINE) +
        app.escape('1') + app.LINE_END
    )
    thm_strs = headlined_sections(
        string=block_str.strip(),
        headline_pattern=headline_pattern,
    )

    return thm_strs


def species_name(thm_dstr):
    """ Parses the name of the species from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: string species in thermo block
        :type thm_dstr: str
        :return name: name of the species
        :rtype: str
    """

    pattern = app.STRING_START + app.capturing(app.one_or_more(app.NONSPACE))
    name = apf.first_capture(pattern, thm_dstr)

    return name


def temperatures(thm_dstr):
    """ Parses the temperatures from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: string species in thermo block
        :type thm_dstr: str
        :return temps: temperatures (K)
        :rtype: tuple(float)
    """

    headline = apf.split_lines(thm_dstr)[0]
    pattern = (app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT) +
               app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT) +
               app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT))
    captures = apf.first_capture(pattern, headline)
    assert captures
    temps = tuple(map(float, captures))

    return temps


def low_coefficients(thm_dstr):
    """ Parses the low temperature coefficients from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: string species in thermo block
        :type thm_dstr: str
        :return cfts: low temperature coefficients
        :rtype: tuple(float)
    """

    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15)
    cfts = tuple(map(float, capture_lst[7:14]))

    return cfts


def high_coefficients(thm_dstr):
    """ Parses the high temperature coefficients from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: string species in thermo block
        :type thm_dstr: str
        :return cfts: high temperature coefficients
        :rtype: tuple(float)
    """

    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15)
    cfts = tuple(map(float, capture_lst[:7]))

    return cfts


def temp_common_default(block_str):
    """ Parses the common temperature defaults from the thermo block
        of the mechanism input file.

        :param block_str: string for thermo block
        :type block_str: str
        :return tmp_com_def: common temp defined in block
        :rtype: float
    """

    pattern = (app.UNSIGNED_FLOAT + app.LINESPACES +
               app.capturing(app.UNSIGNED_FLOAT) + app.LINESPACES +
               app.UNSIGNED_FLOAT)
    capture = apf.first_capture(pattern, block_str)
    assert capture
    tmp_com_def = float(capture)

    return tmp_com_def
