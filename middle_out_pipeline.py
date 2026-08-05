#!/usr/bin/env python3
"""
Middle-out abstraction pipeline for cyclic peptide geometry.

Core invariant (the middle):
    sequence → hard domain reduction → kernel dimension / obstruction

Slices matriculate outward; the topological coordinate is never discarded.
"""
import numpy as np
from numpy.linalg import norm, eigvalsh, svd
from scipy.optimize import minimize

RANK = {'A': 2, 'G': 2, 'P': 1}
PHI_PRO = np.deg2rad(-65.0)
BL = {'N_CA': 1.458, 'CA_C': 1.525, 'C_N': 1.329}
BA = {'N_CA_C': np.deg2rad(111.2), 'CA_C_N': np.deg2rad(116.2)}

def Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def Rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
def homog(R, t):
    T = np.eye(4); T[:3, :3] = R; T[:3, 3] = t; return T
def residue_T(phi, psi, omega=np.pi):
    T1 = homog(Rz(phi), np.array([BL['N_CA'], 0., 0.]))
    T2 = homog(Rz(psi) @ Rx(BA['N_CA_C']), np.array([BL['CA_C'], 0., 0.]))
    T3 = homog(Rz(omega - np.pi) @ Rx(BA['CA_C_N']), np.array([BL['C_N'], 0., 0.]))
    return T3 @ T2 @ T1
def so3_log(R):
    tr = np.clip((np.trace(R) - 1) / 2, -1., 1.)
    th = np.arccos(tr)
    if th < 1e-10: return np.zeros(3)
    K = (R - R.T) / (2 * np.sin(th))
    return np.array([K[2, 1], K[0, 2], K[1, 0]]) * th

def slice0_topology(seq):
    seq = list(seq)
    N, npro = len(seq), seq.count('P')
    domain = sum(RANK.get(r, 2) for r in seq)
    ker = max(0, domain - min(6, domain))
    obst = (2 * N - 6) - ker
    return {'slice': 0, 'N': N, 'n_pro': npro, 'domain': domain, 'ker': ker, 'obstruction': obst}

def _unpack(seq, params):
    N = len(seq); ph, ps = np.zeros(N), np.zeros(N); idx = 0
    for i, r in enumerate(seq):
        if RANK.get(r, 2) == 2:
            ph[i], ps[i] = params[idx], params[idx+1]; idx += 2
        else:
            ph[i], ps[i] = PHI_PRO, params[idx]; idx += 1
    return ph, ps

def _residual(seq, params):
    ph, ps = _unpack(seq, params)
    T = np.eye(4)
    for p, s in zip(ph, ps):
        T = T @ residue_T(p, s)
    return np.concatenate([so3_log(T[:3, :3]), T[:3, 3]])

def slice2_kinematic(seq, ntrials=8, seed=0):
    seq = list(seq)
    dims = [RANK.get(r, 2) for r in seq]
    nparams = sum(dims)
    rng = np.random.default_rng(seed)
    def obj(p): return np.sum(_residual(seq, p)**2)
    best, bestf = None, np.inf
    for _ in range(ntrials):
        p0 = []
        for d in dims:
            p0.extend(rng.uniform(-np.pi, np.pi, d))
        res = minimize(obj, np.array(p0), method='L-BFGS-B',
                       bounds=[(-np.pi, np.pi)]*nparams, options={'maxiter': 200})
        if res.fun < bestf:
            bestf, best = res.fun, res.x.copy()
    r0 = _residual(seq, best)
    J = np.zeros((6, nparams))
    for i in range(nparams):
        p2 = best.copy(); p2[i] += 1e-6
        J[:, i] = (_residual(seq, p2) - r0) / 1e-6
    evals = np.sort(np.real(eigvalsh(J.T @ J)))
    svals = svd(J, compute_uv=False)
    rank = int(np.sum(svals > 1e-6))
    ker = int(np.sum(evals < 1e-7))
    lam_min = float(evals[ker]) if ker < len(evals) else 0.0
    return {'ker': ker, 'rank_dmu': rank, 'lam_min': lam_min,
            'residual_norm': float(norm(r0)), 'params': best}

def run_middle_out(seq, seed=0):
    core = slice0_topology(seq)
    kin = slice2_kinematic(seq, seed=seed)
    return core, kin

if __name__ == '__main__':
    print('MIDDLE-OUT PIPELINE')
    for s in ['AAAAA', 'PAAAA', 'PPAAA', 'PPPAA', 'PPPPP', 'APPPA', 'GPGPG']:
        core, kin = run_middle_out(s, seed=hash(s) % 2**20)
        print(f"{s:8s}  obst={core['obstruction']:.0f}  ker0={core['ker']}  "
              f"ker2={kin['ker']}  λmin={kin['lam_min']:.3f}  ||res||={kin['residual_norm']:.2e}")
