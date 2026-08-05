"""Reproduce the P1 measurement end to end. Downloads 8 CCDC CIFs."""
import os
import subprocess
import tempfile
import numpy as np
from holonomy_extract import read_cif_backbone, analyse

BASE = "https://huggingface.co/datasets/RosettaCommons/AfCycDesign/resolve/main/data/CCDC_cifs"
IDS = ["RH7_1", "RH8_1", "RH9_1", "RH10_1", "RH11_1", "RH12_1", "RH13_1", "RAR13_1"]


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def download_cif(i, dest_dir="cifs"):
    """Download one CIF atomically; fail before leaving a partial cache file."""
    os.makedirs(dest_dir, exist_ok=True)
    p = os.path.join(dest_dir, f"{i}.cif")
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return p
    url = f"{BASE}/{i}.cif"
    fd, tmp = tempfile.mkstemp(prefix=f".{i}.", suffix=".cif.part", dir=dest_dir)
    os.close(fd)
    try:
        subprocess.run(
            ["curl", "--fail", "--silent", "--show-error", "--location",
             "--max-time", "60", "-o", tmp, url],
            check=True,
        )
        if os.path.getsize(tmp) == 0:
            raise RuntimeError(f"empty download for {i}")
        os.replace(tmp, p)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return p


def main():
    for i in IDS:
        download_cif(i)

    print(f"{'ID':<9}{'ch':>3}{'N':>4}{'CA-CA':>8}{'theta_deg':>11}{'lam_min':>10}{'E_tot':>9}")
    for i in IDS:
        f = os.path.join("cifs", f"{i}.cif")
        if not os.path.exists(f):
            print(f"# skip missing {i}")
            continue
        for c, res in sorted(read_cif_backbone(f).items()):
            nums = sorted(k for k, v in res.items() if "CA" in v)
            if len(nums) < 5:
                continue
            r = analyse(np.array([res[k]["CA"] for k in nums]))
            if not (3.5 < r["ca_mean"] < 4.1 and r["ca_max"] < 4.6):
                continue
            phase_err = abs(wrap(r["theta"] - r["solid"]))
            if phase_err >= 1e-9:
                raise RuntimeError(
                    f"transport/solid-angle mismatch for {i} chain {c}: "
                    f"|wrap(theta-solid)|={phase_err}"
                )
            print(
                f"{i:<9}{c:>3}{r['N']:>4}{r['ca_mean']:>8.3f}{r['theta_deg']:>11.2f}"
                f"{r['lam_min']:>10.5f}{r['E_tot']:>9.5f}"
            )


if __name__ == "__main__":
    main()
