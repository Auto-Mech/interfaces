""" Install Interfaces to MESS, CHEMKIN, VaReCoF, ProjRot, and ThermP
"""

from distutils.core import setup

setup(name="interfaces",
      version="0.1.0",
      packages=['mess_io',
                'mess_io.writer',
                'mess_io.reader',
                'projrot_io',
                'varecof_io',
                'varecof_io.writer',
                'varecof_io.reader',
                'chemkin_io',
                'chemkin_io.writer',
                'chemkin_io.plotter',
                'chemkin_io.parser',
                'chemkin_io.calculator',
                'thermp_io'],
      package_dir={
          'mess_io': 'mess_io',
          'projrot_io': 'projrot_io',
          'varecof_io': 'varecof_io',
          'thermp_io': 'thermp_io',
          'chemkin_io': 'chemkin_io'},
      package_data={
          'mess_io': ['writer/templates/sections/*.mako',
                      'writer/templates/sections/monte_carlo/*.mako',
                      'writer/templates/sections/reaction_channel/*.mako',
                      'writer/templates/species/*.mako',
                      'writer/templates/species/info/*.mako',
                      'tests/data/*.txt'],
          'projrot_io': ['templates/*.mako',
                         'tests/data/*.txt'],
          'varecof_io': ['writer/templates/*.mako',
                         'tests/data/*.txt'],
          'thermp_io': ['templates/*.mako'],
          'chemkin_io': ['tests/data/*.txt', 'tests/data/*.csv']})
