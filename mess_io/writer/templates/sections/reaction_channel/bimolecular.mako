Bimolecular ${bimolec_label} 
!---------------------------------------------------
  Fragment ${species1_label}
${species1_data}\
% if not isatom1:
      ZeroEnergy[kcal/mol]    0.0
% endif
    End
!---------------------------------------------------
  Fragment ${species2_label}
${species2_data}\
% if not isatom2:
      ZeroEnergy[kcal/mol]    0.0
% endif
    End
!---------------------------------------------------
  GroundEnergy[kcal/mol]    ${ground_energy}
End\
