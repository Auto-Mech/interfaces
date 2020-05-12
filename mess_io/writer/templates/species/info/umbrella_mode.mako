Umbrella
% if geom:
  Geometry[angstrom]   ${natom}
${geom}
% endif
  Group                ${group}
  Axis                 ${axis}
  ReferenceAtom        ${ref_atom} 
  Potential[kcal/mol]  ${npotential}
${potential} 
End
