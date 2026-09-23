---
task: unsupported
engine: gaussian
error_class: environment_error
failure_class: infra_transient
outcome: failed
wall_time_s: 1
n_atoms: 2
method: B3LYP
basis: 6-31G(d)
cores: 1
mode: slurm
---
Symptom: Slurm job 14052 ended before starting Gaussian. Its log says `g16: command not found` after loading the gaussian16/g16 module.

Attempts: Submitted one single-core Gaussian 16 job with the site module. Checked the module definition and then the configured installation directory. The directory is group-restricted for the submitting user, and the module did not place an executable named g16 on PATH.

Result: The requested Gaussian engine is unavailable to this user on the compute node. No retry was submitted.

Context: This was the raw-engine workaround for the unsupported isotope-aware equilibrium-constant workflow for H2 + D2 -> 2 HD at 298.15 K and 1 atm.
