%if rotor_id != '':
# ${rotor_id}
%endif
Rotor  Hindered
% if geom:
  Geometry[angstrom]   ${natom}
${geom}
% endif
  Group                ${group}
  Axis                 ${axis}
  Symmetry             ${symmetry}
  Potential[kcal/mol]  ${npotential}
${potential} 
% if use_quantum_weight:
  UseQuantumWeight
% endif
End
