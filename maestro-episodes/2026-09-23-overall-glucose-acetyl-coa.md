---
task: unsupported
engine: none
error_class: support_gap
outcome: support_gap
---
Symptom: The user requested the overall biochemical standard Gibbs energy for conversion of glucose to acetyl-CoA.
Attempts: Searched the live MAESTRO catalog for free energy, thermochemistry, energy, and reaction. The catalog exposes ReactionProfileTask, which requires a minimum-energy path and reactant/product/transition-state Gibbs energies, but not an overall multistep biochemical standard free-energy calculation.
Result: MAESTRO support gap. The requested quantity must be evaluated from biochemical thermodynamic data rather than a MAESTRO QM reaction-profile run.
Context: Net reaction specified under transformed biochemical standard conditions, pH 7, 298 K: glucose + 2 ADP + 2 Pi + 2 NAD+ + CoA -> 2 acetyl-CoA + 2 ATP + 2 NADH + 2 H+ + 2 H2O.
