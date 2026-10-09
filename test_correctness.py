"""Correctness tests: python test_correctness.py"""
import random
import unittest

from booth import booth_multiply
from candidate_generator import generate_candidates
from conflict_checker import check_candidate, check_parallel, check_sequential
from data_loader import load_dataset


def tiny():
    # 3 sessions: sessions 0,1 same faculty+section; session 2 is a 2-slot lab
    return {"name": "t", "days": 2, "slots_per_day": 4, "n_sessions": 3,
            "n_rooms": 2, "sess_faculty": [0, 0, 1], "sess_section": [0, 0, 1],
            "sess_dur": [1, 1, 2], "room_cap": [50, 80], "sec_size": [60, 40]}


class TestConstraints(unittest.TestCase):
    def test_no_conflict(self):
        r = check_candidate(tiny(), [(1, 0), (1, 1), (0, 4)])
        self.assertEqual(r["total"], 0)

    def test_faculty_and_section_clash(self):
        r = check_candidate(tiny(), [(1, 0), (0, 0), (1, 4)])
        self.assertEqual(r["faculty"], 1)
        self.assertEqual(r["section"], 1)

    def test_room_clash(self):
        r = check_candidate(tiny(), [(1, 0), (1, 0), (1, 5)])
        self.assertEqual(r["room"], 1)

    def test_capacity(self):
        r = check_candidate(tiny(), [(0, 0), (1, 1), (1, 4)])  # sec size 60 > 50
        self.assertEqual(r["capacity"], 1)

    def test_lab_continuity(self):
        r = check_candidate(tiny(), [(1, 0), (1, 1), (1, 3)])  # lab at slot 3 of 4
        self.assertEqual(r["lab"], 1)


class TestParallelEqualsSequential(unittest.TestCase):
    def test_same_results(self):
        for name in ("small", "medium"):
            data = load_dataset(f"data/{name}.json")
            cands = generate_candidates(data, 60)
            self.assertEqual(check_sequential(data, cands),
                             check_parallel(data, cands, workers=2))


class TestBooth(unittest.TestCase):
    def test_matches_python_multiply(self):
        rng = random.Random(1)
        for _ in range(500):
            a, b = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
            self.assertEqual(booth_multiply(a, b), a * b)


if __name__ == "__main__":
    unittest.main()
