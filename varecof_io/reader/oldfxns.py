"""
various parser functions for varecof
"""

# import numpy as np
# import autoread as ar
# import autoparse.pattern as app
# import autoparse.find as apf
# import automol


# def dividing_surface_fluxes(divsur_outstring, flux_outstring):
#     """ finds the minimum energy fluxes for each pivot point
#  :param int idx_potential: index corresponding to which potential is desired
#         :return dist: distance between pivot points where div surface is (au)
#         :rtype list float
#         :return temp: temperatures for which flux is evaluated (K)
#         :rtype list float
#         :return flux: fluxes through the dividing surface (10^11 cm3/s)
#         :rtype list float
#     """
#
#     # Open the divsur.out file and get the pivot-point distance
#     dist = []
#     divsur_lines = divsur_outstring.splitlines()
#     for i, line in enumerate(divsur_lines):
#         if 'distances between pivot points' in line:
#             dist.append(float(divsur_lines[i+2].strip().split('=')[1]))
#
#     # Open the flux.out file and read in the contents
#     temperatures, fluxes = [], []
#     npot = 1
#     with open('flux.out', 'r') as fluxfile:
#         for line in fluxfile:
#             if 'T, K:' in line:
#                 if npot == idx_potential:
#                     temperatures = temp + line.strip().split()[2:]
#             if 'Flux:' in line:
#                 fluxex = flux + line.strip().split()[1:]
#
#     assert len(dist) == len(temp) == len(flux)
#
#     return dist, temp, flux
#
#
# def _get_minimal_energies(output_string):
#     """ get the minimal energies from flux.out file string
#         returns in kcal/mol
#     """
#
#     energies = ar.matrix.read(
#         output_string,
#     start_ptt=app.padded(app.escape('Minimal energy (kcal/mol):')) + '\n',
#         )
#
#     return energies
#
#
# def _get_min_flux_temps(output_string):
#     """ get the temperatures associated with the minal thermal fluxes
#         from flux.out file string
#         returns in K
#     """
#
#     pattern = 'T, K:' + app.SPACES + app.capturing(app.LINE_FILL)
#     temp_lines = apf.all_captures(pattern, output_string)
#     temperatures = [line.strip().split() for line in temp_lines]
#     temperatures = np.array(temperatures, dtype=np.float64)
#
#     return temperatures
#
#
# def _get_min_flux_fluxes(output_string):
#     """ get the fluxes associated with the minal thermal fluxes
#         from flux.out file string
#         returns in 10^11 cm^3/sec
#     """
#
#     pattern = 'Flux:' + app.SPACES + app.capturing(app.LINE_FILL)
#     flux_lines = apf.all_captures(pattern, output_string)
#     fluxes = [line.strip().split() for line in flux_lines]
#     fluxes = np.array(fluxes, dtype=np.float64)
#
#     return fluxes
#
#
# def _get_min_e_confs(output_string):
#     """ gets the minimal energy configration from flux.out
#     """
#
#     # get all the blocks
#     pattern = app.capturing(
#         'Minimal energy configuration (Angstrom):' + app.WILDCARD +
#         'interatomic distance matrix (Angstrom):')
#     geom_blocks = apf.all_captures(pattern, output_string)
#
#     # read the geometries from the block
#     geoms = []
#     for block in geom_blocks:
#         syms, xyzs = ar.geom.read(
#             block,
#             start_ptt=app.padded(app.NEWLINE).join([
#                 app.padded(
#                     app.escape('Minimal energy configuration (Angstrom):'),
#                     app.NONNEWLINE),
#                 app.LINE, '']))
#         geoms.append(automol.geom.from_data(syms, xyzs, angstrom=True))
#
#     return geoms
