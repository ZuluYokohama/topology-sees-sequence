"""Reference-connection strain: holonomy at preferred Ramachandran geometry.

Closed structures have trivial holonomy by definition. theta is the residual
screw of the REFERENCE connection (every residue at preferred basin).
"""
import numpy as np
from numpy.linalg import norm, pinv

B={'N_CA':1.458,'CA_C':1.525,'C_N':1.329}
A={'N_CA_C':np.deg2rad(111.2),'CA_C_N':np.deg2rad(116.2),'C_N_CA':np.deg2rad(121.7)}

def Rx(a):
    c,s=np.cos(a),np.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Rz(a):
    c,s=np.cos(a),np.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def H(R,t):
    T=np.eye(4); T[:3,:3]=R; T[:3,3]=t; return T

def T_res(phi,psi,omega=np.pi):
    return (H(Rz(phi),[B['N_CA'],0,0]) @
            H(Rz(psi)@Rx(np.pi-A['N_CA_C']),[B['CA_C'],0,0]) @
            H(Rz(omega)@Rx(np.pi-A['CA_C_N']),[B['C_N'],0,0]) @
            H(Rx(np.pi-A['C_N_CA']),[0,0,0]))

def so3_log(R):
    c=np.clip((np.trace(R)-1)/2,-1,1); th=np.arccos(c)
    if th<1e-9: return np.zeros(3)
    K=(R-R.T)/(2*np.sin(th)); return th*np.array([K[2,1],K[0,2],K[1,0]])

def se3_log(T):
    w=so3_log(T[:3,:3]); th=norm(w)
    if th<1e-9: return np.concatenate([w,T[:3,3]])
    K=np.array([[0,-w[2],w[1]],[w[2],0,-w[0]],[-w[1],w[0],0]])/th
    Vi=np.eye(3)-th/2*K+(1-th*np.sin(th)/(2*(1-np.cos(th))))*K@K
    return np.concatenate([w,Vi@T[:3,3]])

REF={'G':(-82.,8.),'P':(-65.,145.),'X':(-63.,-43.)}
cls=lambda r: r if r in ('G','P') else 'X'

def _omegas_for(seq, omega_mode='trans'):
    """Per-residue omega conventions.

    omega_mode:
      'trans'   — ω=π for every residue (default, paper-style all-trans).
      'cis_pro' — ω=0 for Pro, ω=π otherwise (executable cis-Pro convention).
      sequence of length N — explicit omegas in radians.
    """
    n = len(seq)
    if isinstance(omega_mode, (list, tuple, np.ndarray)):
        if len(omega_mode) != n:
            raise ValueError('omega sequence length must match seq')
        return list(omega_mode)
    if omega_mode == 'trans':
        return [np.pi] * n
    if omega_mode == 'cis_pro':
        return [0.0 if r == 'P' else np.pi for r in seq]
    raise ValueError(f"unknown omega_mode: {omega_mode!r}")


def ref_holonomy(seq, omega_mode='trans'):
    omegas = _omegas_for(seq, omega_mode)
    M = np.eye(4)
    for r, om in zip(seq, omegas):
        p, s = REF[cls(r)]
        M = M @ T_res(np.deg2rad(p), np.deg2rad(s), om)
    return M


def closure_jac(seq, omega_mode='trans'):
    omegas = _omegas_for(seq, omega_mode)
    N = len(seq)
    Ts = []
    for r, om in zip(seq, omegas):
        p, s = REF[cls(r)]
        Ts.append(T_res(np.deg2rad(p), np.deg2rad(s), om))
    J = np.zeros((6, 2 * N)); eps = 1e-6
    for i in range(N):
        for j, _ in enumerate(('phi', 'psi')):
            p, s = REF[cls(seq[i])]; d = [np.deg2rad(p), np.deg2rad(s)]; d[j] += eps
            Tp = T_res(d[0], d[1], omegas[i])
            M0 = np.eye(4); M1 = np.eye(4)
            for k in range(N):
                M0 = M0 @ Ts[k]; M1 = M1 @ (Tp if k == i else Ts[k])
            J[:, 2 * i + j] = (se3_log(M1) - se3_log(M0)) / eps
    return J


def strain(seq, omega_mode='trans'):
    M = ref_holonomy(seq, omega_mode); xi = se3_log(M); J = closure_jac(seq, omega_mode)
    dq = -pinv(J) @ xi
    return dict(theta=norm(xi[:3]), theta_deg=np.degrees(norm(xi[:3])),
                gap=norm(xi[3:]), E=float(dq @ dq), N=len(seq), omega_mode=omega_mode)


if __name__ == '__main__':
    print('N  theta(deg)  gap  E')
    for N in [7, 9, 12, 15]:
        r = strain('A' * N)
        print(f"{N:3d} {r['theta_deg']:10.2f} {r['gap']:8.3f} {r['E']:10.4f}")
    print('seq strain at N=12 (trans ω):')
    for s in ['A' * 12, 'G' * 12, 'P' * 12, 'PG' * 6]:
        r = strain(s)
        print(f"  {s:20s} E={r['E']:.3f} theta={r['theta_deg']:.1f}")
    print('poly-Pro N=12 cis_pro vs trans:')
    for mode in ('trans', 'cis_pro'):
        r = strain('P' * 12, omega_mode=mode)
        print(f"  omega_mode={mode:8s} E={r['E']:.3f} theta={r['theta_deg']:.1f}")
