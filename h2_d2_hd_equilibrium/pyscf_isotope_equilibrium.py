# maestro: raw
"""Raw PySCF workaround: isotope-aware partition functions for H2 + D2 -> 2 HD."""
import json
import math
from pathlib import Path

import numpy as np
from pyscf import dft, gto
from pyscf.geomopt.geometric_solver import optimize
from pyscf.hessian import thermo
from pyscf.data import nist

ROOT = Path(__file__).resolve().parent
T = 298.15
P = 101325.0
H_PLANCK = 6.62607015e-34
K_B = 1.380649e-23
AMU_KG = 1.66053906660e-27
BOHR_M = 5.29177210903e-11
HARTREE_J = 4.3597447222071e-18
CM_TO_K = 1.438776877
M_H = 1.00782503223
M_D = 2.01410177812


def q_translation(mass_amu):
    mass = mass_amu * AMU_KG
    return ((2.0 * math.pi * mass * K_B * T) / H_PLANCK**2) ** 1.5 * K_B * T / P


def q_rotation(masses_amu, coords_bohr, sigma):
    masses = np.asarray(masses_amu) * AMU_KG
    coords = np.asarray(coords_bohr) * BOHR_M
    center = np.einsum("i,ij->j", masses, coords) / masses.sum()
    shifted = coords - center
    inertia = np.sum(masses * np.sum(shifted * shifted, axis=1))
    return 8.0 * math.pi**2 * inertia * K_B * T / (sigma * H_PLANCK**2), inertia


def q_vibration(freq_cm):
    theta = CM_TO_K * float(freq_cm)
    x = theta / T
    return math.exp(-0.5 * x) / (-math.expm1(-x))


def main():
    initial = "H 0 0 0; H 0 0 0.7414"
    mol = gto.M(atom=initial, basis="6-31g(d)", unit="Angstrom", charge=0, spin=0)
    mf = dft.RKS(mol)
    mf.xc = "b3lyp"
    mf.grids.level = 3
    mf.conv_tol = 1e-10
    mf.kernel()
    mol_eq = optimize(mf, maxsteps=50)
    mf_eq = dft.RKS(mol_eq)
    mf_eq.xc = "b3lyp"
    mf_eq.grids.level = 3
    mf_eq.conv_tol = 1e-10
    e_elec = float(mf_eq.kernel())
    hessian = mf_eq.Hessian().kernel()
    coords = mol_eq.atom_coords()

    species = {
        "H2": {"masses": [M_H, M_H], "sigma": 2},
        "D2": {"masses": [M_D, M_D], "sigma": 2},
        "HD": {"masses": [M_H, M_D], "sigma": 1},
    }
    result = {"temperature_K": T, "pressure_Pa": P, "electronic_energy_hartree": e_elec,
              "bond_length_angstrom": float(np.linalg.norm(coords[1] - coords[0]) * nist.BOHR),
              "species": {}}
    for name, item in species.items():
        vib = thermo.harmonic_analysis(mol_eq, hessian, mass=np.asarray(item["masses"]), imaginary_freq=False)
        freqs = np.asarray(vib["freq_wavenumber"], dtype=float)
        if len(freqs) != 1 or freqs[0] <= 0:
            raise RuntimeError(f"{name}: expected one positive diatomic vibrational frequency, got {freqs.tolist()}")
        qt = q_translation(sum(item["masses"]))
        qr, inertia = q_rotation(item["masses"], coords, item["sigma"])
        qv = q_vibration(freqs[0])
        result["species"][name] = {
            "mass_amu": sum(item["masses"]), "symmetry_number": item["sigma"],
            "frequency_cm-1": float(freqs[0]), "q_trans": qt, "q_rot": qr, "q_vib": qv,
            "inertia_kg_m2": inertia, "electronic_degeneracy": 1,
        }

    a, b, c = result["species"]["H2"], result["species"]["D2"], result["species"]["HD"]
    k_trans = c["q_trans"]**2 / (a["q_trans"] * b["q_trans"])
    k_rot = c["q_rot"]**2 / (a["q_rot"] * b["q_rot"])
    k_vib = c["q_vib"]**2 / (a["q_vib"] * b["q_vib"])
    delta_e_h = 2 * e_elec - e_elec - e_elec
    k_elec = math.exp(-delta_e_h * HARTREE_J / (K_B * T))
    result["equilibrium_constant"] = {"K_trans": k_trans, "K_rot": k_rot, "K_vib": k_vib,
                                       "K_elec": k_elec, "K_total": k_trans*k_rot*k_vib*k_elec,
                                       "delta_E_elec_hartree": delta_e_h}
    (ROOT / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        "# H₂ + D₂ → 2 HD equilibrium constant", "",
        "- Method: raw PySCF 2.14.0, B3LYP/6-31G(d); geometry optimization + analytic Hessian.",
        f"- Conditions: gas phase, {T:.2f} K, {P/101325:.2f} atm, one CPU core.",
        "- Isotope treatment: one H₂ Born–Oppenheimer Hessian with exact nuclear masses applied to H₂, D₂, and HD.",
        "- Nuclear-spin statistical weights are not included; electronic ground-state degeneracy is 1 for every species.", "",
        "## Molecular quantities", "",
        "| Species | ν (cm⁻¹) | q_trans | q_rot | q_vib |", "|---|---:|---:|---:|---:|",
    ]
    for name in ("H2", "D2", "HD"):
        x = result["species"][name]
        lines.append(f"| {name} | {x['frequency_cm-1']:.3f} | {x['q_trans']:.8e} | {x['q_rot']:.8e} | {x['q_vib']:.8e} |")
    k = result["equilibrium_constant"]
    lines += ["", "## Equilibrium-constant contributions", "",
              "| Contribution | Value |", "|---|---:|",
              f"| Translation, K_trans | {k['K_trans']:.10g} |",
              f"| Rotation, K_rot | {k['K_rot']:.10g} |",
              f"| Vibration, K_vib | {k['K_vib']:.10g} |",
              f"| Electronic, K_elec | {k['K_elec']:.10g} |",
              f"| **Total K** | **{k['K_total']:.10g}** |", "",
              f"Optimized H–H bond length: {result['bond_length_angstrom']:.8f} Å."]
    (ROOT / "summary.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
