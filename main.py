"""Pipeline demo: load -> generate -> check (parallel) -> score -> select.
Usage: python main.py [small|medium|large] [num_candidates]"""
import sys
import time

from candidate_generator import generate_candidates
from conflict_checker import CONSTRAINTS, check_parallel
from data_loader import load_dataset
from scorer import fitness, penalty, select_best


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "medium"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    print(f"[1] Loading dataset '{name}'")
    data = load_dataset(f"data/{name}.json")
    print(f"    sessions={data['n_sessions']}, rooms={data['n_rooms']}")

    print(f"[2] Master generating {count} candidate timetables")
    cands = generate_candidates(data, count)

    print("[3] Workers checking conflicts in parallel")
    t0 = time.perf_counter()
    results = check_parallel(data, cands)
    print(f"    done in {time.perf_counter() - t0:.3f}s")

    valid = sum(1 for r in results if r["total"] == 0)
    print(f"[4] Valid (zero-conflict) candidates: {valid}/{count}")

    best, f = select_best(results)
    r = results[best]
    print(f"[5] Best candidate: #{best} | penalty={penalty(r)} | fitness={f:.4f}")
    print("    violations:", {k: r[k] for k in CONSTRAINTS})


if __name__ == "__main__":
    main()
