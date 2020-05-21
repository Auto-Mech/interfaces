%if rotor_id != '':
# ${rotor_id}
%endif
InternalRotation
% if geom:
  Geometry[angstrom]   ${natom}
${geom}
% endif
  Group                      ${group}
  Axis                       ${axis}
  Symmetry                   ${symmetry}
  GridSize                   ${grid_size}
  MassExpansionSize          ${mass_exp_size}
  PotentialExpansionSize     ${pot_exp_size}
  HamiltonSizeMin            ${hmin}
  HamiltonSizeMax            ${hmax}
End
\
