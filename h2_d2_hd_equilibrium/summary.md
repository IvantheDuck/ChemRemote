# H₂ + D₂ → 2 HD equilibrium constant

- Method: raw PySCF 2.14.0, B3LYP/6-31G(d); geometry optimization + analytic Hessian.
- Conditions: gas phase, 298.15 K, 1.00 atm, one CPU core.
- Isotope treatment: one H₂ Born–Oppenheimer Hessian with exact nuclear masses applied to H₂, D₂, and HD.
- Nuclear-spin statistical weights are not included; electronic ground-state degeneracy is 1 for every species.

## Molecular quantities

| Species | ν (cm⁻¹) | q_trans | q_rot | q_vib |
|---|---:|---:|---:|---:|
| H2 | 4453.123 | 1.12480359e+05 | 1.70883458e+00 | 2.15598798e-05 |
| D2 | 3150.044 | 3.17776006e+05 | 3.41504394e+00 | 5.00174779e-04 |
| HD | 3857.012 | 2.06480908e+05 | 4.55572486e+00 | 9.08450906e-05 |

## Equilibrium-constant contributions

| Contribution | Value |
|---|---:|
| Translation, K_trans | 1.192784556 |
| Rotation, K_rot | 3.556465935 |
| Vibration, K_vib | 0.7653054407 |
| Electronic, K_elec | 1 |
| **Total K** | **3.246500404** |

Optimized H–H bond length: 0.74278821 Å.
