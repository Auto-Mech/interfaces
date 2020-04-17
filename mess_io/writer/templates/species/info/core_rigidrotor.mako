  Geometry[angstrom]        ${natom}
${geom}
  Core RigidRotor
    SymmetryFactor          ${sym_factor}
% if interp_emax is not None:     
    ZeroPointEnergy[1/cm]             0.0
    InterpolationEnergyMax[kcal/mol]  ${interp_emax}
% endif
  End\
