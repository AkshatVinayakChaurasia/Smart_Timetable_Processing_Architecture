"""Scorer: weighted penalty per candidate -> fitness (higher is better)."""
from booth import booth_multiply

WEIGHTS = {"faculty": 10, "room": 10, "section": 10, "capacity": 5, "lab": 8}


def penalty(result):
    # weight x count computed with Booth's algorithm
    return sum(booth_multiply(WEIGHTS[k], result[k]) for k in WEIGHTS)


def fitness(result):
    return 1.0 / (1.0 + penalty(result))


def select_best(results):
    """Return (index, fitness) of the best candidate."""
    scored = [(fitness(r), i) for i, r in enumerate(results)]
    f, i = max(scored)
    return i, f
