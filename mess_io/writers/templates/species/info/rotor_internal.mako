%if rotor_id != '':
# ${rotor_id}
%endif
InternalRotation
  Group                      ${group}
  Axis                       ${axis}
  Symmetry                   ${symmetry}
  MassExpansionSize          ${mass_exp_size}
  PotentialExpansionSize     ${pot_exp_size}
  HamiltonSizeMin            ${hmin}
  HamiltonSizeMax            ${hmax}
  GridSize                   ${grid_size}
End

