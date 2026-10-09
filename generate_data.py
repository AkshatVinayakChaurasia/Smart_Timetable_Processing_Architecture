"""Synthetic dataset generator (small / medium / large) -> data/*.json"""
import json
import os
import random

CONFIGS = {
    "small":  dict(sections=3,  faculty=5,  rooms=4,  theory=5, labs=1),
    "medium": dict(sections=8,  faculty=12, rooms=8,  theory=6, labs=2),
    "large":  dict(sections=20, faculty=25, rooms=14, theory=7, labs=2),
}
DAYS = 5
SLOTS_PER_DAY = 6
SUBJECTS = ["DSA", "OS", "DBMS", "CAPP", "Maths", "Python", "AI", "Networks", "SE"]


def build(name, cfg, seed=7):
    rng = random.Random(seed)
    faculty = [f"F{i+1}" for i in range(cfg["faculty"])]
    rooms = [{"id": f"R{i+1}", "capacity": rng.choice([45, 60, 75, 90])}
             for i in range(cfg["rooms"])]
    sections = [{"id": f"S{i+1}", "size": rng.randint(40, 70)}
                for i in range(cfg["sections"])]
    sessions = []
    sid = 0
    for sec in sections:
        for k in range(cfg["theory"]):
            sessions.append({"id": sid, "subject": SUBJECTS[k % len(SUBJECTS)],
                             "type": "theory", "faculty": rng.choice(faculty),
                             "section": sec["id"], "duration": 1})
            sid += 1
        for k in range(cfg["labs"]):
            sessions.append({"id": sid, "subject": SUBJECTS[k % len(SUBJECTS)] + " Lab",
                             "type": "lab", "faculty": rng.choice(faculty),
                             "section": sec["id"], "duration": 2})
            sid += 1
    return {"name": name, "days": DAYS, "slots_per_day": SLOTS_PER_DAY,
            "faculty": faculty, "rooms": rooms, "sections": sections,
            "sessions": sessions}


def main():
    os.makedirs("data", exist_ok=True)
    for name, cfg in CONFIGS.items():
        ds = build(name, cfg)
        with open(os.path.join("data", f"{name}.json"), "w") as f:
            json.dump(ds, f, indent=2)
        print(f"{name:7s}: {len(ds['sessions'])} sessions, "
              f"{len(ds['rooms'])} rooms, {len(ds['faculty'])} faculty, "
              f"{len(ds['sections'])} sections")


if __name__ == "__main__":
    main()
