!===================================================
!  ENERGY TRANSFER SECTION
!===================================================
Model
  EnergyRelaxation
    Exponential
       Factor[1/cm]                     ${exp_factor}
       Power                            ${exp_power}
       ExponentCutoff                   ${exp_cutoff}
    End
  CollisionFrequency
    LennardJones
       Epsilons[K]                      ${epsilons}
       Sigmas[angstrom]                 ${sigmas}
       Masses[amu]                      ${masses}
    End
