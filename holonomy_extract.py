"""
holonomy_extract.py  --  P1 measurement, corrected.

Bishop holonomy from coordinates. No optimizer.
Closed structures have trivial holonomy by definition; this measures the
geometric holonomy of the CA space curve (equals -2pi*Wr mod 2pi), which
is NOT automatically the sheaf theta (see CORRECTIONS.md, STATUS_P1_P2.md).
"""
import re, numpy as np
from numpy.linalg import norm

B = {'N_CA': 1.458, 'CA_C': 1.525, 'C_N': 1.329}
A = {'N_CA_C': np.deg2rad(111.2), 'CA_C_N': np.deg2rad(116.2), 'C_N_CA': np.deg2rad(121.7)}

def _place(a, b, c, bond, ang, tor):
    bc = (c - b) / norm(c - b)
    n = np.cross(b - a, bc); n /= norm(n)
    m = np.cross(n, bc)
    d = np.array([-bond*np.cos(ang), bond*np.cos(tor)*np.sin(ang), bond*np.sin(tor)*np.sin(ang)])
    return c + d[0]*bc + d[1]*m + d[2]*n

def build_backbone(phis, psis, omegas=None):
    n = len(phis)
    omegas = [np.pi]*n if omegas is None else omegas
    N  = [np.zeros(3)]
    CA = [np.array([B['N_CA'], 0., 0.])]
    C  = [CA[0] + B['CA_C']*np.array([np.cos(np.pi - A['N_CA_C']), np.sin(np.pi - A['N_CA_C']), 0.])]
    for i in range(n-1):
        N.append(_place(N[i], CA[i], C[i], B['C_N'], A['CA_C_N'], psis[i]))
        CA.append(_place(CA[i], C[i], N[i+1], B['N_CA'], A['C_N_CA'], omegas[i]))
        C.append(_place(C[i], N[i+1], CA[i+1], B['CA_C'], A['N_CA_C'], phis[i+1]))
    return np.array(N), np.array(CA), np.array(C)

_num = lambda s: float(re.sub(r'\(\d+\)', '', s))

def _cart_matrix(a, b, c, al, be, ga):
    al, be, ga = map(np.deg2rad, (al, be, ga))
    v = np.sqrt(1 - np.cos(al)**2 - np.cos(be)**2 - np.cos(ga)**2 + 2*np.cos(al)*np.cos(be)*np.cos(ga))
    return np.array([
        [a, b*np.cos(ga), c*np.cos(be)],
        [0, b*np.sin(ga), c*(np.cos(al)-np.cos(be)*np.cos(ga))/np.sin(ga)],
        [0, 0, c*v/np.sin(ga)]])

def read_cif_backbone(path):
    txt = open(path, errors='ignore').read()
    g = lambda k: _num(re.search(rf'{k}\s+(\S+)', txt).group(1))
    M = _cart_matrix(g('_cell_length_a'), g('_cell_length_b'), g('_cell_length_c'),
                     g('_cell_angle_alpha'), g('_cell_angle_beta'), g('_cell_angle_gamma'))
    out = {}
    for line in txt.splitlines():
        m = re.match(r'^(N|CA|C)_(?:([A-Za-z]+):)?(\d+)\s+([A-Za-z]{1,2})\s+'
                     r'(-?[\d.]+(?:\(\d+\))?)\s+(-?[\d.]+(?:\(\d+\))?)\s+(-?[\d.]+(?:\(\d+\))?)', line)
        if not m: continue
        atom, chain, res = m.group(1), (m.group(2) or 'A'), int(m.group(3))
        f = np.array([_num(m.group(5)), _num(m.group(6)), _num(m.group(7))])
        out.setdefault(chain, {}).setdefault(res, {})[atom] = M @ f
    return out

def _rot_between(u, v):
    """Minimal SO(3) rotation taking unit vector u onto v (det = +1 always)."""
    c = np.clip(u @ v, -1, 1)
    ax = np.cross(u, v); s = norm(ax)
    if s < 1e-12:
        if c > 0:
            return np.eye(3)
        # Antiparallel: 180° about a deterministic axis perpendicular to u.
        # -I is improper (det=-1) and must not be used.
        helper = np.array([1., 0., 0.]) if abs(u[0]) < 0.9 else np.array([0., 1., 0.])
        ax = np.cross(u, helper); ax = ax / norm(ax)
        # Rodrigues with th=π: I + 0*K + 2 K@K = 2 n n^T - I
        return 2.0 * np.outer(ax, ax) - np.eye(3)
    ax = ax / s; th = np.arctan2(s, c)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)

def bishop_holonomy(CA):
    n = len(CA)
    T = np.array([CA[(i+1) % n] - CA[i] for i in range(n)])
    T = T / norm(T, axis=1, keepdims=True)
    u = np.cross(T[0], [0., 0., 1.])
    if norm(u) < 1e-8: u = np.cross(T[0], [0., 1., 0.])
    u0 = u/norm(u); u = u0.copy()
    for i in range(n):
        u = _rot_between(T[i], T[(i+1) % n]) @ u
    u -= (u @ T[0])*T[0]; u /= norm(u)
    c = np.clip(u0 @ u, -1, 1)
    s = np.cross(u0, u) @ T[0]
    return float(np.arctan2(s, c))

def solid_angle(CA):
    n = len(CA)
    T = np.array([CA[(i+1) % n] - CA[i] for i in range(n)])
    T = T / norm(T, axis=1, keepdims=True)
    tot = 0.0
    for i in range(n):
        a, b, c = T[i-1], T[i], T[(i+1) % n]
        n1 = np.cross(a, b); n2 = np.cross(b, c)
        if norm(n1) < 1e-12 or norm(n2) < 1e-12: continue
        n1 /= norm(n1); n2 /= norm(n2)
        ang = np.arctan2(np.cross(n1, n2) @ b, n1 @ n2)
        tot += ang
    return float(-tot)

lam_min = lambda th, N: 2 - 2*np.cos(th/N)
E_tot   = lambda th, N: 2*N*(1 - np.cos(th/N))

def analyse(CA):
    N = len(CA)
    d = [norm(CA[(i+1) % N] - CA[i]) for i in range(N)]
    th = bishop_holonomy(CA)
    return dict(N=N, theta=th, theta_deg=np.degrees(th), solid=solid_angle(CA),
                ca_mean=float(np.mean(d)), ca_min=float(np.min(d)), ca_max=float(np.max(d)),
                lam_min=lam_min(th, N), E_tot=E_tot(th, N))

def read_pdb_ca(path, chain=None):
    """Read CA coordinates, preserving chain identity.

    chain=None  → return dict[chain_id] -> (N,3) CA array (all chains, separate).
    chain='A'   → return (N,3) array for that chain only, or None if empty.
    Never merges distinct chains into one CA curve.
    """
    by_chain = {}
    for line in open(path, errors='ignore'):
        if line.startswith(('ATOM', 'HETATM')) and line[12:16].strip() == 'CA':
            ch = line[21].strip() or 'A'
            if chain is not None and ch != chain:
                continue
            resi = int(line[22:26])
            xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            by_chain.setdefault(ch, {})[resi] = xyz
        if line.startswith('ENDMDL'):
            break
    arrays = {
        ch: np.array([d[k] for k in sorted(d)])
        for ch, d in by_chain.items() if d
    }
    if chain is not None:
        return arrays.get(chain)
    return arrays
