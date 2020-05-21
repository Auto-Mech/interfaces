""" Library of functions for writing and formatting strings
    that are used by all of the interface modules
"""

from ioformat._format import build_mako_str
from ioformat._format import indent
from ioformat._format import remove_trail_whitespace


__all__ = [
    'build_mako_str',
    'indent',
    'remove_trail_whitespace'
]
