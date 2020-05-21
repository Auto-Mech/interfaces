""" Various formatting functions used by each I/O module
"""

import os
from mako.template import Template
import autoparse.pattern as app
import autoparse.find as apf


def build_mako_str(template_file_name, template_src_path, template_keys):
    """ Uses an input dictionary to fill in Mako template file containing the
        keys of the dictionary, then writes a string corresponding to the
        filled-in Mako template.
        :param string template_file_name: Name of the Mako template file
        :param string template_src_path: Path where Mako template file resides
        :param dct template_keys: keys and values used to fill Mako template
        :return mako_str: filled-in Mako template
        :rtype: string
    """
    template_file_path = os.path.join(template_src_path, template_file_name)
    mess_str = Template(filename=template_file_path).render(**template_keys)

    return remove_trail_whitespace(mess_str)


def indent(string, nspaces):
    """ Indents each of the lines of a multiline string.
        :param string string: Input string to indent
        :param nspaces: number of spaces to indent the lines of the string
        :return indented_string: string indented by nspaces
        :rtype string
    """
    pad = nspaces * ' '
    indented_string = ''.join(pad+line for line in string.splitlines(True))

    return indented_string


def remove_trail_whitespace(string):
    """ Removes trailing spaces and empty lines from a input string.
        :param string string: Input string to clean up
        :return cleaned string
        :rtype: string
    """
    empty_line = app.LINE_START + app.maybe(app.LINESPACES) + app.NEWLINE
    trailing_spaces = app.LINESPACES + app.LINE_END
    pattern = app.one_of_these([empty_line, trailing_spaces])
    return apf.remove(pattern, string)
