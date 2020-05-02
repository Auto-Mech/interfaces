""" Test writing files for ThermP
"""

import thermp_io


def test__input_file():
    """ test thermp_io.writer.input_file
    """
    temps = [100.0, 200.0, 300.0, 400.0, 500.0,
             600.0, 700.0, 800.0, 900.0, 1000.0]
    formula = 'CH4'
    h0form = -123.45
    enthalpyt = 0.
    breakt = 1000.
    thermp_str = thermp_io.writer.input_file(
        ntemps=len(temps),
        formula=formula,
        delta_h=h0form,
        enthalpy_temp=enthalpyt,
        break_temp=breakt)
    print(thermp_str)


if __name__ == '__main__':
    test__input_file()
