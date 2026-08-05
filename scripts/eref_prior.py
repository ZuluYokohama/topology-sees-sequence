#!/usr/bin/env python3
"""E_ref as sequence prior: experimental vs hallucinated vs random.

No coordinates, no force field. Writes data/eref_*.csv and prints summary.
"""
from __future__ import annotations

import csv
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from derive import strain  # noqa: E402

AA = list("ACDEFGHIKLMNPQRSTVWY")
DATA = ROOT / "data"
SEED = 0


def load(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = (r.get("sequence") or "").strip().upper()
            if not s or any(c not in AA for c in s):
                continue
            rows.append(
                {"id": r.get("ID", ""), "seq": s, "N": len(s), "type": r.get("Type", "")}
            )
    return rows


def e_ref(seq: str) -> float:
    return float(strain(seq)["E"])


def summarize(name: str, Es: list[float]) -> dict:
    Es_s = sorted(Es)

    def q(p: float) -> float:
        i = (len(Es_s) - 1) * p
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        if lo == hi:
            return Es_s[lo]
        return Es_s[lo] * (hi - i) + Es_s[hi] * (i - lo)

    return {
        "name": name,
        "n": len(Es),
        "mean": statistics.fmean(Es),
        "median": statistics.median(Es),
        "p10": q(0.10),
        "p90": q(0.90),
        "frac_gt1": sum(e > 1 for e in Es) / len(Es),
        "frac_gt5": sum(e > 5 for e in Es) / len(Es),
        "frac_gt20": sum(e > 20 for e in Es) / len(Es),
    }


def main() -> None:
    random.seed(SEED)
    DATA.mkdir(exist_ok=True)
    exp_path = DATA / "afcycpep_data_experimental.csv"
    hall_path = DATA / "afcycpep_data_hallucinated.csv"
    if not exp_path.exists() or not hall_path.exists():
        raise SystemExit(
            f"Missing CSVs under {DATA}. Download from "
            "RosettaCommons/AfCycDesign (data/afcycpep_data_*.csv)."
        )

    exp = load(exp_path)
    hall = load(hall_path)
    for r in exp:
        r["E"] = e_ref(r["seq"])

    byN: dict[int, list] = defaultdict(list)
    for r in hall:
        byN[r["N"]].append(r)
    hall_s = []
    for N in sorted(byN):
        pool = byN[N][:]
        random.shuffle(pool)
        hall_s.extend(pool[:40])
    if len(hall_s) > 400:
        random.shuffle(hall_s)
        hall_s = hall_s[:400]
    for r in hall_s:
        r["E"] = e_ref(r["seq"])

    rand = []
    for r in hall_s:
        s = "".join(random.choice(AA) for _ in range(r["N"]))
        rand.append(
            {
                "id": f"R{r['N']}_{len(rand)}",
                "seq": s,
                "N": r["N"],
                "type": "Random",
                "E": e_ref(s),
            }
        )

    rand_exp = []
    for r in exp:
        for _ in range(50):
            s = "".join(random.choice(AA) for _ in range(r["N"]))
            rand_exp.append({"N": r["N"], "E": e_ref(s), "type": "Random@expN"})

    rows_out = [
        summarize("experimental", [r["E"] for r in exp]),
        summarize("hallucinated_sample", [r["E"] for r in hall_s]),
        summarize("random_matched_hallN", [r["E"] for r in rand]),
        summarize("random_matched_expN", [r["E"] for r in rand_exp]),
    ]

    print(
        f"{'cohort':22s} {'n':>5s} {'mean':>8s} {'median':>8s} "
        f"{'p10':>8s} {'p90':>8s} {'>1':>7s} {'>5':>7s} {'>20':>7s}"
    )
    for srow in rows_out:
        print(
            f"{srow['name']:22s} {srow['n']:5d} {srow['mean']:8.3f} "
            f"{srow['median']:8.3f} {srow['p10']:8.3f} {srow['p90']:8.3f} "
            f"{srow['frac_gt1']:7.2%} {srow['frac_gt5']:7.2%} {srow['frac_gt20']:7.2%}"
        )

    print("\nWithin-N mean E_ref (hall sample vs random same N):")
    hN: dict[int, list] = defaultdict(list)
    rN: dict[int, list] = defaultdict(list)
    for r in hall_s:
        hN[r["N"]].append(r["E"])
    for r in rand:
        rN[r["N"]].append(r["E"])
    for N in sorted(hN):
        if N not in rN:
            continue
        hm, rm = statistics.fmean(hN[N]), statistics.fmean(rN[N])
        print(
            f"  N={N:2d}  hall n={len(hN[N]):3d} mean={hm:7.3f}  "
            f"rand mean={rm:7.3f}  delta(hall-rand)={hm - rm:+7.3f}"
        )

    print("\nExperimental sequences:")
    print(f"{'ID':12s} {'seq':16s} {'N':>3s} {'E_ref':>8s}")
    for r in sorted(exp, key=lambda x: x["E"]):
        print(f"{r['id']:12s} {r['seq']:16s} {r['N']:3d} {r['E']:8.3f}")

    with (DATA / "eref_prior_summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)
    with (DATA / "eref_experimental.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "seq", "N", "E"])
        w.writeheader()
        for r in exp:
            w.writerow({"id": r["id"], "seq": r["seq"], "N": r["N"], "E": f"{r['E']:.6f}"})
    with (DATA / "eref_hall_sample.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "seq", "N", "E", "type"])
        w.writeheader()
        for r in hall_s:
            w.writerow(
                {
                    "id": r["id"],
                    "seq": r["seq"],
                    "N": r["N"],
                    "E": f"{r['E']:.6f}",
                    "type": "Hallucinated",
                }
            )
        for r in rand:
            w.writerow(
                {
                    "id": r["id"],
                    "seq": r["seq"],
                    "N": r["N"],
                    "E": f"{r['E']:.6f}",
                    "type": "Random",
                }
            )
    print(f"\nwrote under {DATA}")


if __name__ == "__main__":
    main()
