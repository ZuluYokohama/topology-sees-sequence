"""Reproduce the P1 measurement end to end. Downloads 8 CCDC CIFs."""
import os, glob, subprocess, numpy as np
from holonomy_extract import read_cif_backbone, analyse
BASE="https://huggingface.co/datasets/RosettaCommons/AfCycDesign/resolve/main/data/CCDC_cifs"
IDS=["RH7_1","RH8_1","RH9_1","RH10_1","RH11_1","RH12_1","RH13_1","RAR13_1"]
os.makedirs("cifs",exist_ok=True)
for i in IDS:
    p=f"cifs/{i}.cif"
    if not os.path.exists(p):
        subprocess.run(["curl","-sL",f"{BASE}/{i}.cif","-o",p])
wrap=lambda x:(x+np.pi)%(2*np.pi)-np.pi
print(f"{'ID':<9}{'ch':>3}{'N':>4}{'CA-CA':>8}{'theta_deg':>11}{'lam_min':>10}{'E_tot':>9}")
for f in sorted(glob.glob("cifs/*.cif")):
    ID=os.path.basename(f)[:-4]
    for c,res in sorted(read_cif_backbone(f).items()):
        nums=sorted(k for k,v in res.items() if 'CA' in v)
        if len(nums)<5: continue
        r=analyse(np.array([res[k]['CA'] for k in nums]))
        if not(3.5<r['ca_mean']<4.1 and r['ca_max']<4.6): continue
        assert abs(wrap(r['theta']-r['solid']))<1e-9, "transport/solid-angle mismatch"
        print(f"{ID:<9}{c:>3}{r['N']:>4}{r['ca_mean']:>8.3f}{r['theta_deg']:>11.2f}"
              f"{r['lam_min']:>10.5f}{r['E_tot']:>9.5f}")
