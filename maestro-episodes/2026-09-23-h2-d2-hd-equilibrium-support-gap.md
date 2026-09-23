---
task: unsupported
engine: none
error_class: support_gap
outcome: support_gap
---
Symptom: The requested gas-phase equilibrium constant for H2 + D2 -> 2 HD needs isotope-specific translational, rotational, vibrational, and electronic partition-function contributions. ThermochemistryTask accepts ordinary element symbols but rejects D in an XYZ geometry. IsotopeShiftTask produces isotope-shifted harmonic frequencies only, not isotope-specific thermochemistry or reaction equilibrium constants.

Attempts: Queried the live MAESTRO catalog for thermochemistry, free energy, equilibrium constant, frequencies, reaction, and the Korean query. ThermochemistryTask and IsotopeShiftTask were found and inspected. A charge suggestion succeeded for H2 but rejected D2 and HD with an unknown-element error for D.

Result: MAESTRO does not currently provide the composite isotope-exchange equilibrium-constant workflow or the isotope-aware thermochemistry needed for this request. Use an allowed raw-engine workflow for the unsupported calculation.

Context: User requested one CPU core on a cluster node, with a result directory and summary.md. Requested conditions: gas phase, 298.15 K, 1 atm; selected Gaussian/DFT/B3LYP/6-31G(d) during the initial MAESTRO setup.
