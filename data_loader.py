"""Input loader: JSON -> compact integer arrays (read-only, shared by all workers)."""
import json


def load_dataset(path):
    with open(path) as f:
        raw = json.load(f)
    fac_idx = {f: i for i, f in enumerate(raw["faculty"])}
    sec_idx = {s["id"]: i for i, s in enumerate(raw["sections"])}
    return {
        "name": raw["name"],
        "days": raw["days"],
        "slots_per_day": raw["slots_per_day"],
        "n_sessions": len(raw["sessions"]),
        "n_rooms": len(raw["rooms"]),
        "sess_faculty": [fac_idx[s["faculty"]] for s in raw["sessions"]],
        "sess_section": [sec_idx[s["section"]] for s in raw["sessions"]],
        "sess_dur": [s["duration"] for s in raw["sessions"]],
        "room_cap": [r["capacity"] for r in raw["rooms"]],
        "sec_size": [s["size"] for s in raw["sections"]],
    }
