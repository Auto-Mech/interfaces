!===================================================
!  GLOBAL KEYWORD SECTION
!===================================================
% if temperatures != '':
TemperatureList[K]                     ${temperatures}
% else:
Temperature(step[K],size)              ${temp_step}    ${ntemps}
% endif:
RelativeTemperatureIncrement           ${rel_temp_inc}
AtomDistanceMin[angstrom]              ${atom_dist_min}\
