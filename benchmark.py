"""Sequential vs parallel benchmark.
Speedup = T_seq / T_par ; Efficiency = Speedup / cores."""
import csv
import os
import time

from candidate_generator import generate_candidates
from conflict_checker import check_parallel, check_sequential
from data_loader import load_dataset

CANDIDATES = {"small": 200, "medium": 2000, "large": 4000}


def best_of(fn, repeats):
    best, out = None, None
    for _ in range(repeats):
        t0 = time.perf_counter()
        out = fn()
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return best, out


def run(names=("small", "medium", "large"), repeats=2, workers=None):
    workers = workers or os.cpu_count() or 1
    rows = []
    print(f"CPU cores used: {workers}\n")
    print(f"{'dataset':8s}{'sessions':>9s}{'cands':>7s}{'T_seq(s)':>10s}"
          f"{'T_par(s)':>10s}{'speedup':>9s}{'effic.':>8s}{'correct':>9s}")
    for name in names:
        data = load_dataset(os.path.join("data", f"{name}.json"))
        cands = generate_candidates(data, CANDIDATES[name])
        t_seq, r_seq = best_of(lambda: check_sequential(data, cands), repeats)
        t_par, r_par = best_of(
            lambda: check_parallel(data, cands, workers=workers), repeats)
        speedup = t_seq / t_par
        eff = speedup / workers
        ok = r_seq == r_par
        rows.append([name, data["n_sessions"], len(cands), workers,
                     round(t_seq, 4), round(t_par, 4),
                     round(speedup, 3), round(eff, 3), ok])
        print(f"{name:8s}{data['n_sessions']:>9d}{len(cands):>7d}{t_seq:>10.3f}"
              f"{t_par:>10.3f}{speedup:>9.2f}{eff:>8.2f}{str(ok):>9s}")
    os.makedirs("results", exist_ok=True)
    with open(os.path.join("results", "benchmark_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "sessions", "candidates", "workers", "t_seq_s",
                    "t_par_s", "speedup", "efficiency", "results_match"])
        w.writerows(rows)
    print("\nSaved: results/benchmark_results.csv")


if __name__ == "__main__":
    run()
