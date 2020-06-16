!===================================================
!  GLOBAL KEYWORD SECTION
!===================================================
TemperatureList[K]                     ${temperatures}
PressureList[atm]                      ${pressures}
!
EnergyStepOverTemperature              .2
ExcessEnergyOverTemperature            40
ModelEnergyLimit[kcal/mol]             400
!
CalculationMethod                      direct
!
WellCutoff                             10
ChemicalEigenvalueMax                  0.2
!
ReductionMethod                        diagonalization 
!
AtomDistanceMin[bohr]                  1.3
RateOutput                             rate.out
