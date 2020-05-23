""" Library of functions for writing and formatting strings
    that are used by all of the interface modules
"""

from ioformat._format import build_mako_str
from ioformat._format import indent
from ioformat._format import headlined_sections
from ioformat._format import remove_whitespace
from ioformat._format import remove_trail_whitespace
from ioformat._format import remove_comment_lines
from ioformat import phycon


__all__ = [
    'build_mako_str',
    'indent',
    'headlined_sections',
    'remove_whitespace',
    'remove_trail_whitespace',
    'remove_comment_lines',
    'phycon'
]
