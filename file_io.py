# file_io.py - Save and load Musician data to/from a JSON file
# Author: Estelle

import json
import os
from models import Musician, PracticeSession

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "gigready_data.json")


def save_data(musician):
    """Save a Musician's data (name, goal, and all sessions) to JSON."""
    data = {
        "name": musician.name,
        "weekly_goal": musician.weekly_goal,
        "songs": {}
    }
    for title, song in musician.songs.items():
        data["songs"][title] = [s.to_dict() for s in song.sessions]

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_data():
    """Load Musician data from JSON.

    Returns a Musician object on success, or None if no save file exists
    or the file is corrupted/malformed.
    """
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None  # no save file yet, caller will create new Musician
    except json.JSONDecodeError:
        print("Warning: save file is corrupted. Starting fresh.")
        return None

    try:
        musician = Musician(
            name=data["name"],
            weekly_goal=data.get("weekly_goal", 0)
        )
        for title, sessions_data in data.get("songs", {}).items():
            for s_data in sessions_data:
                session = PracticeSession.from_dict(s_data)
                musician.log_session(title, session)
        return musician
    except (KeyError, ValueError, TypeError) as e:
        print(f"Warning: save file has unexpected structure ({e}). Starting fresh.")
        return None
