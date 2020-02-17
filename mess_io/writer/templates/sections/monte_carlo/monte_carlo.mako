  MonteCarlo
    MoleculeSpecification       ${atom_list}
${flux_mode_str}\
    DataFile                    ${data_file_name}
    ElectronicLevels[1/cm]      ${nlevels}
${levels}
    GroundEnergy[kcal/mol]      ${ground_energy}
    ReferenceEnergy[kcal/mol]   ${reference_energy}
% if nfreqs > 0:
  Frequencies[1/cm]         ${nfreqs}
${freqs}
% endif
% if no_qc_corr:
    NoQuantumCorrection
% endif
% if use_cm_shift:
    UseCMShift
% endif
  End
