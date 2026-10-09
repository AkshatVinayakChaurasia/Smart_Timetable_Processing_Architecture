"""Conflict checker: sequential baseline + parallel (master-worker) version.

Constraints checked per candidate:
  faculty clash, room clash, section clash, room capacity, lab continuity.

Clash detection compares every pair of sessions (O(n^2)) - simple, easy to
explain, and compute-heavy enough for parallelism to matter.
"""
import multiprocessing as mp
import os

CONSTRAINTS = ("faculty", "room", "section", "capacity", "lab")


def check_candidate(data, cand):
    n = data["n_sessions"]
    S = data["slots_per_day"]
    fac, sec, dur = data["sess_faculty"], data["sess_section"], data["sess_dur"]
    room_cap, sec_size = data["room_cap"], data["sec_size"]

    faculty = room_c = section = capacity = lab = 0
    for i in range(n):
        room_i, start_i = cand[i]
        end_i = start_i + dur[i]
        if room_cap[room_i] < sec_size[sec[i]]:
            capacity += 1
        if dur[i] > 1 and (start_i % S) + dur[i] > S:
            lab += 1
        for j in range(i + 1, n):
            room_j, start_j = cand[j]
            if start_i < start_j + dur[j] and start_j < end_i:  # time overlap
                if fac[i] == fac[j]:
                    faculty += 1
                if room_i == room_j:
                    room_c += 1
                if sec[i] == sec[j]:
                    section += 1
    total = faculty + room_c + section + capacity + lab
    return {"faculty": faculty, "room": room_c, "section": section,
            "capacity": capacity, "lab": lab, "total": total}


# ---------------- sequential baseline ----------------
def check_sequential(data, candidates):
    return [check_candidate(data, c) for c in candidates]


# ---------------- parallel (master-worker) ----------------
_DATA = None  # read-only shared input, set once per worker process


def _init_worker(data):
    global _DATA
    _DATA = data


def _worker_task(item):
    idx, cand = item
    return idx, check_candidate(_DATA, cand)  # result is private to the task


def check_parallel(data, candidates, workers=None, batch_size=None):
    """Master hands out candidates through a dynamic work queue
    (imap_unordered); workers validate independently; master merges results."""
    workers = workers or os.cpu_count() or 1
    if batch_size is None:
        batch_size = max(1, len(candidates) // (workers * 4))
    results = [None] * len(candidates)
    with mp.Pool(workers, initializer=_init_worker, initargs=(data,)) as pool:
        for idx, res in pool.imap_unordered(
                _worker_task, enumerate(candidates), chunksize=batch_size):
            results[idx] = res  # merge step (only the master writes here)
    return results
