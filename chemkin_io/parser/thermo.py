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
    """ thermo strings
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
    """ get the species name from a thermo data string
    """
    pattern = app.STRING_START + app.capturing(app.one_or_more(app.NONSPACE))
    spc = apf.first_capture(pattern, thm_dstr)
    return spc


def temperatures(thm_dstr):
    """ get the common temperature from a thermo data string
    """
    headline = apf.split_lines(thm_dstr)[0]
    pattern = (app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT) +
               app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT) +
               app.LINESPACES + app.capturing(app.UNSIGNED_FLOAT))
    captures = apf.first_capture(pattern, headline)
    assert captures
    tmps = tuple(map(float, captures))
    return tmps


def low_coefficients(thm_dstr):
    """ get the low temperature thermo coefficients
    """
    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15)
    cfts = tuple(map(float, capture_lst[7:14]))
    return cfts


def high_coefficients(thm_dstr):
    """ get the high temperature thermo coefficients
    """
    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15)
    cfts = tuple(map(float, capture_lst[:7]))
    return cfts


def temp_common_default(block_str):
    """ temperature defaults from the thermo block
    """
    pattern = (app.UNSIGNED_FLOAT + app.LINESPACES +
               app.capturing(app.UNSIGNED_FLOAT) + app.LINESPACES +
               app.UNSIGNED_FLOAT)
    capture = apf.first_capture(pattern, block_str)
    assert capture
    tmp_com_def = float(capture)
    return tmp_com_def
