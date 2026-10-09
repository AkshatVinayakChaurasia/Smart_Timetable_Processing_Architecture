# Smart Timetable Processing Architecture

**Course:** Computer Architecture & Parallel Processing (CCSE0304) | **SDG 4 – Quality Education**
**Project status:** ~65% complete (Review 2 – Development & Application)

A master-worker prototype that checks candidate university timetables for
constraint violations, **sequentially** and **in parallel**, and compares the two.

## Constraints checked
Faculty clash · Room clash · Section clash · Room capacity · Lab continuity (2 consecutive slots, same day)

## Architecture (pipeline)
`load -> generate candidates (master) -> check conflicts (workers) -> merge -> score -> select best`

| File | Role |
|---|---|
| `generate_data.py` | Creates small / medium / large synthetic datasets (JSON) |
| `data_loader.py` | Input loader (read-only data shared by workers) |
| `candidate_generator.py` | Master: generates candidate timetables |
| `conflict_checker.py` | Sequential baseline + parallel checker (multiprocessing pool, dynamic work queue) |
| `scorer.py`, `booth.py` | Weighted penalty -> fitness; Booth's algorithm for weight x count |
| `benchmark.py` | T_seq vs T_par, speedup, efficiency, correctness check -> `results/` |
| `test_correctness.py` | Unit tests + parallel == sequential check |
| `main.py` | End-to-end demo |

## How to run (Python 3.8+, no external packages)
```bash
python generate_data.py        # create datasets in data/
python test_correctness.py     # run tests
python benchmark.py            # sequential vs parallel comparison
python main.py medium 200      # full pipeline demo
```

## Design notes
- **Race conditions avoided:** inputs are read-only; every task returns its own private result, and only the master merges them.
- **Load balancing:** dynamic work queue (`imap_unordered`) handles uneven task sizes.
- **Metrics:** Speedup = T_seq / T_par, Efficiency = Speedup / cores.
- Small datasets show little/no gain because process-creation overhead dominates.

## Done vs. remaining
- [x] Constraint set, data model, datasets
- [x] Sequential + parallel conflict checkers, correctness tests
- [x] Basic candidate generator (randomized with retries), weighted scorer
- [x] Benchmark (time, speedup, efficiency)
- [ ] Full candidate generation (genetic-algorithm style evolution)
- [ ] Tune worker count and batch size
- [ ] Final benchmark on larger datasets, graphs, Amdahl's-law analysis
- [ ] Final documentation and demo
