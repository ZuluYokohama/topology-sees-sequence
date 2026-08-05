#!/usr/bin/env python3
"""Middle-out v2: Slice 0 is reference-connection strain (not n_Pro)."""
from derive import strain

def middle_out_v2(seq):
    s = ''.join(seq) if not isinstance(seq, str) else seq
    r = strain(s)
    return {
        'N': len(s),
        'E_ref': r['E'],
        'theta_ref_deg': r['theta_deg'],
        'gap': r['gap'],
        'n_pro': s.count('P'),
        'n_gly': s.count('G'),
    }

if __name__ == '__main__':
    print(f"{'seq':20s} {'E_ref':>10s} {'theta':>8s} {'#P':>4s}")
    for seq in ['A'*12, 'G'*12, 'P'*12, 'PG'*6, 'AP'*6, 'A'*9+'PPP']:
        r = middle_out_v2(seq)
        print(f"{seq:20s} {r['E_ref']:10.3f} {r['theta_ref_deg']:8.1f} {r['n_pro']:4d}")
