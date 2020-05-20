""" functions operating on the mechanism string
"""

from io import StringIO
import pandas
import autoparse.pattern as app
import autoparse.find as apf
from automol.smiles import inchi as _inchi
from automol.inchi import smiles as _smiles
from chemkin_io.parser import util


def species_block(mech_str):
    """ Parses the species block out of the mechanism input file.
        :param string mech_str: string of mechanism input file
        :return block_str: string containing species block
        :rtype: string
    """
    block_str = util.block(
        string=_clean_up(mech_str),
        start_pattern=app.one_of_these(['SPECIES', 'SPEC']),
        end_pattern='END'
    )
    return block_str


def reaction_block(mech_str, remove_comments=True):
    """ Parses the reaction block out of the mechanism input file.
        :param string mech_str: string of mechanism input file
        :return block_str: string containing reaction block
        :rtype: string
    """
    block_str = util.block(
        string=_clean_up(mech_str, remove_comments=remove_comments),
        start_pattern=app.one_of_these(['REACTIONS', 'REAC']),
        end_pattern='END'
    )
    return block_str


def thermo_block(mech_str):
    """ Parses the thermo block out of the mechanism input file.
        :param string mech_str: string of mechanism input file
        :return block_str: string containing thermo block
        :rtype: string
    """
    block_str = util.block(
        string=_clean_up(mech_str),
        start_pattern=app.one_of_these(['THERMO ALL', 'THERM ALL', 'THER ALL',
                                        'THERMO', 'THERM', 'THER']),
        end_pattern='END'
    )
    return block_str


def reaction_units(mech_str):
    """ Parses from the mechanism input file, the units of the 
        pre-exponential (A) and activation enery (Ea) fitting parameter.
        :param string mech_str: string of mechanism input file
        :return units: units for fitiing parameters (A unit, Ea unit)
        :rtype: list
    """

    def _reaction_units(string, start_pattern, units_pattern):
        """ Helper function used to parse the units at the head of 
            the reaction block of the mechanism file string.
            :param string string: mechanism string to parse
            :param string start_pattern: start pattern at line at head
            :param string units_pattern: patterns for various unit strings
            :return units: units for fitiing parameters (A unit, Ea unit)
            :rtype: list
        """
        rxn_line_pattern = start_pattern + app.capturing(app.LINE_FILL)
        units_string = apf.first_capture(rxn_line_pattern, string)
        units_lst = apf.all_captures(units_pattern, units_string)

        ckin_ea_units = ['CAL/MOLE', 'KCAL/MOLE',
                         'JOULES/MOLE', 'KJOULES/MOLE',
                         'KELVINS']
        ckin_a_units = ['MOLES', 'MOLECULES']

        if units_lst:
            if any(unit in ckin_ea_units for unit in units_lst):
                for unit in ckin_ea_units:
                    if unit in units_lst:
                        ea_unit = unit.lower()
            else:
                ea_unit = 'cal/mole'
            if any(unit in ckin_a_units for unit in units_lst):
                for unit in ckin_a_units:
                    if unit in units_lst:
                        a_unit = unit.lower()
            else:
                a_unit = 'moles'
            units = (ea_unit, a_unit)
        else:
            units = ('cal/mole', 'moles')

        return units

    units = _reaction_units(
        string=_clean_up(mech_str),
        start_pattern=app.one_of_these(['REACTIONS', 'REAC']),
        units_pattern=app.one_or_more(
            app.one_of_these([app.LETTER, app.escape('/')])),
    )

    return units


def spc_name_dct(csv_str, entry):
    """ build a dictionary of name idx and inchi entry
    """
    data = _read_csv(csv_str)

    if entry == 'inchi':
        spc_dct = _read_name_inchi(data)
    elif entry == 'smiles':
        spc_dct = _read_name_smiles(data)
    elif entry == 'mult':
        spc_dct = _read_name_mult(data)
    elif entry == 'charge':
        spc_dct = _read_name_charge(data)
    elif entry == 'sens':
        spc_dct = _read_name_sensitivity(data)
    else:
        raise NotImplementedError

    return spc_dct


def _read_name_inchi(data):
    """ get dct[name]=inchi """

    if hasattr(data, 'inchi'):
        spc_dct = dict(zip(data.name, data.inchi))
    elif hasattr(data, 'smiles'):
        print('No inchi column in csv file, getting inchi from SMILES')
        ichs = [_inchi(smiles) for smiles in data.smiles]
        spc_dct = dict(zip(data.name, ichs))
    else:
        spc_dct = {}
        print('No "inchi" or "SMILES" column in csv file')

    return spc_dct


def _read_name_smiles(data):
    """ get dct[name]=smiles """

    spc_dct = {}
    if hasattr(data, 'smiles'):
        spc_dct = dict(zip(data.name, data.smiles))
    elif hasattr(data, 'inchi'):
        smiles = [_smiles(ich) for ich in data.inchi]
        spc_dct = dict(zip(data.name, smiles))
    else:
        spc_dct = {}
        print('No "SMILES" or "InChI" column in csv file')

    return spc_dct


def _read_name_mult(data):
    """ get dct[name]=mult """

    if hasattr(data, 'mult'):
        spc_dct = dict(zip(data.name, data.mult))
    else:
        spc_dct = {}
        print('No "mult" column in csv file')

    return spc_dct


def _read_name_charge(data):
    """ get dct[name]=charge """
    fill = 0
    if hasattr(data, 'charge'):
        spc_dct = dict(zip(data.name, data.charge))
    else:
        if fill is not None:
            spc_dct = dict(zip(data.name, [fill for name in data.name]))
        else:
            spc_dct = {}

    return spc_dct


def _read_name_sensitivity(data):
    """ get dct[name]=sensitivity """
    fill = 0.
    if hasattr(data, 'sens'):
        spc_dct = dict(zip(data.name, data.sens))
    else:
        if fill is not None:
            spc_dct = dict(zip(data.name, [fill for name in data.name]))
        else:
            spc_dct = {}

    return spc_dct


def spc_inchi_dct(csv_str):
    """ build a dictionary of inchi idx and name entry
    """
    data = _read_csv(csv_str)

    spc_dct = {}
    if hasattr(data, 'inchi'):
        spc_dct = dict(zip(data.name, data.inchi))
    elif hasattr(data, 'smiles'):
        ichs = [_inchi(smiles) for smiles in data.smiles]
        spc_dct = dict(zip(ichs, data.name))
    else:
        spc_dct = {}

    return spc_dct


def _read_csv(csv_str):
    """ read the csv file; removes whitespace and makes everything lower
    """
    csv_file = StringIO(csv_str)
    data = pandas.read_csv(csv_file, comment='!', quotechar="'")
    data.columns = data.columns.str.strip()
    data.columns = map(str.lower, data.columns)
    return data


def _clean_up(mech_str, remove_comments=True):
    """ Cleans up mechanism input string by converting specific comment
        lines that are used later and removes other comments and 
        whitespace from mech string.
        :param string mech_str: string of mechanism input file
        :return mech_str: string with altered comment lines
        :rtype: string
    """
    mech_str = _convert_comment_lines(mech_str)
    if remove_comments:
        mech_str = util.remove_line_comments(
            mech_str, delim_pattern=app.escape('!'))
    mech_str = util.clean_up_whitespace(mech_str)
    return mech_str


def _convert_comment_lines(mech_str):
    """ alter based on above...
        Reads a string for the mechanism input file and alters certain
        comment lines, by removing the comment symbols. This is so they 
        are not removed later by functions which remove comments from string.
        :param string mech_str: string of mechanism input file
        :return mech_str: string with altered comment lines
        :rtype: string
    """

    # Set the lines in the file (in_lines) and their replacements (out_lines)
    inlines = [
        app.escape('!') + app.SPACES + app.escape('Pressure:')
    ]
    outlines = [
        app.escape('Pressure:')
    ]

    # Loop over lines and make all the replacements in the mech string
    for inline, outline in zip(inlines, outlines):
        mech_str = apf.replace(inline, outline, mech_str, case=True)

    return mech_str
