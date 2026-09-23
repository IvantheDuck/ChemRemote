---
task: unsupported
engine: pyscf
error_class: none
outcome: workaround
n_atoms: 2
method: B3LYP
basis: 6-31G(d)
cores: 1
mode: slurm
---
Symptom: MAESTRO has no isotope-aware thermochemistry and reaction-equilibrium-constant composite for H2 + D2 -> 2 HD.

Attempts: The requested Gaussian 16 run failed before execution because the site module did not provide g16 to this user. A raw PySCF 2.14.0 calculation then optimized H2 and evaluated an analytic Hessian at B3LYP/6-31G(d) on one Slurm CPU core. The common Born-Oppenheimer Hessian was mass-weighted with exact H and D masses for H2, D2, and HD. Standard-state translational, rotational, vibrational, and electronic partition-function ratios were assembled at 298.15 K and 1 atm.

Result: Success. The calculated contributions were K_trans=1.192784556, K_rot=3.556465935, K_vib=0.765305441, K_elec=1, giving K=3.246500404. Nuclear-spin statistical weights were intentionally excluded and documented in summary.md. Slurm accounting was disabled, so no measured wall time was available.

Context: The result and raw inputs are in the user's H2/D2/HD calculation directory. The H2 equilibrium bond length was 0.74278821 Angstrom; harmonic frequencies were 4453.123 (H2), 3150.044 (D2), and 3857.012 cm^-1 (HD).
