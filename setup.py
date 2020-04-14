""" Install Interfaces to MESS and CHEMKIN 
"""

from distutils.core import setup

setup(name="interfaces",
      version="0.2.0",
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
      package_data={}
      ])
