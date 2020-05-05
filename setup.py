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
      package_dir={},
      package_data={
          'mess_io': ['tests/data/*.txt'],
          'projrot_io': ['tests/data/*.txt'],
          'varecof_io': ['tests/data/*.txt'],
          'chemkin_io': ['tests/data/*.txt', 'tests/data/*.csv']})
