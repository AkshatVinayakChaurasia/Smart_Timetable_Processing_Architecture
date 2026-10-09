"""Candidate generator (master side).

A candidate timetable = list with one (room_index, start_slot) per session.
start_slot is a global index: day * slots_per_day + slot_in_day.

Prototype strategy: randomized placement with a few retries per session.
(The full genetic-algorithm style generation is planned for the final review.)
"""
import random


def _placement_cost(data, i, room, start, occ_room, occ_fac, occ_sec):
    S = data["slots_per_day"]
    dur = data["sess_dur"][i]
    cost = 0
    if data["room_cap"][room] < data["sec_size"][data["sess_section"][i]]:
        cost += 1
    if dur > 1 and (start % S) + dur > S:
        cost += 1
    for t in range(start, start + dur):
        if (room, t) in occ_room:
            cost += 1
        if (data["sess_faculty"][i], t) in occ_fac:
            cost += 1
        if (data["sess_section"][i], t) in occ_sec:
            cost += 1
    return cost


def generate_candidate(data, rng, tries=6):
    total_slots = data["days"] * data["slots_per_day"]
    occ_room, occ_fac, occ_sec = set(), set(), set()
    cand = []
    for i in range(data["n_sessions"]):
        best, best_cost = None, None
        for _ in range(tries):
            room = rng.randrange(data["n_rooms"])
            start = rng.randrange(total_slots)
            c = _placement_cost(data, i, room, start, occ_room, occ_fac, occ_sec)
            if best_cost is None or c < best_cost:
                best, best_cost = (room, start), c
                if c == 0:
                    break
        room, start = best
        for t in range(start, start + data["sess_dur"][i]):
            occ_room.add((room, t))
            occ_fac.add((data["sess_faculty"][i], t))
            occ_sec.add((data["sess_section"][i], t))
        cand.append(best)
    return cand


def generate_candidates(data, count, seed=42):
    rng = random.Random(seed)
    return [generate_candidate(data, rng) for _ in range(count)]
