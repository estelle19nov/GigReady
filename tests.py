# tests.py - Test cases for GigReady using assert statements
# Run with: python3 tests.py
# Covers positive, negative, and edge cases (Week 10 TDD approach).
# Author: Estelle

from models import Song, PracticeSession, Musician


# ---------- Positive cases ----------

def test_song_total_minutes():
    """Total minutes should sum across all sessions."""
    song = Song("Bohemian Rhapsody")
    song.add_session(PracticeSession("2026-05-18", 30, 3))
    song.add_session(PracticeSession("2026-05-19", 20, 4))
    assert song.total_minutes() == 50


def test_song_session_count():
    """session_count should return number of sessions."""
    song = Song("Imagine")
    song.add_session(PracticeSession("2026-05-18", 15, 2))
    assert song.session_count() == 1


def test_song_average_difficulty():
    """average_difficulty should be the arithmetic mean."""
    song = Song("Clair de Lune")
    song.add_session(PracticeSession("2026-05-18", 20, 2))
    song.add_session(PracticeSession("2026-05-19", 20, 4))
    assert song.average_difficulty() == 3.0


def test_musician_log_session():
    """log_session should create the song if it doesn't exist."""
    musician = Musician("Alice")
    session = PracticeSession("2026-05-18", 45, 3)
    musician.log_session("Yesterday", session)
    assert "Yesterday" in musician.songs
    assert musician.songs["Yesterday"].total_minutes() == 45


def test_musician_weekly_total():
    """Weekly total should only include sessions in the given week."""
    musician = Musician("Bob", weekly_goal=100)
    week = ["2026-05-12", "2026-05-13", "2026-05-14"]
    musician.log_session("Song A", PracticeSession("2026-05-12", 30, 3))
    musician.log_session("Song B", PracticeSession("2026-05-13", 25, 2))
    musician.log_session("Song A", PracticeSession("2026-05-20", 60, 4))  # outside week
    assert musician.total_minutes_this_week(week) == 55


def test_song_readiness_score():
    """readiness_score should increase with useful practice history."""
    song = Song("Ready Song")
    song.add_session(PracticeSession("2026-05-18", 40, 2))
    song.add_session(PracticeSession("2026-05-19", 40, 2))
    assert song.readiness_score() == 90


def test_songs_needing_attention_order():
    """songs_needing_attention should put the least ready song first."""
    musician = Musician("Casey")
    musician.log_session("Strong Song", PracticeSession("2026-05-18", 80, 2))
    musician.log_session("Weak Song", PracticeSession("2026-05-18", 10, 5))
    ordered = musician.songs_needing_attention()
    assert ordered[0].title == "Weak Song"


def test_practice_session_to_and_from_dict():
    """to_dict and from_dict should be inverses."""
    session = PracticeSession("2026-05-18", 30, 3, "felt good")
    d = session.to_dict()
    restored = PracticeSession.from_dict(d)
    assert restored.date == session.date
    assert restored.duration == session.duration
    assert restored.difficulty == session.difficulty
    assert restored.notes == session.notes


# ---------- Edge cases ----------

def test_song_no_sessions():
    """A song with no sessions should return zero stats, not crash."""
    song = Song("Empty Song")
    assert song.total_minutes() == 0
    assert song.session_count() == 0
    assert song.average_difficulty() == 0


def test_musician_no_songs_weekly_total():
    """A musician with no songs should report 0 minutes this week."""
    musician = Musician("New User")
    week = ["2026-05-12", "2026-05-13"]
    assert musician.total_minutes_this_week(week) == 0


# ---------- Negative cases (invalid input should raise) ----------

def test_negative_duration_raises():
    """Creating a session with non-positive duration should raise ValueError."""
    try:
        PracticeSession("2026-05-18", 0, 3)
        assert False, "Expected ValueError for duration=0"
    except ValueError:
        pass


def test_difficulty_out_of_range_raises():
    """Difficulty outside 1-5 should raise ValueError."""
    try:
        PracticeSession("2026-05-18", 30, 6)
        assert False, "Expected ValueError for difficulty=6"
    except ValueError:
        pass

    try:
        PracticeSession("2026-05-18", 30, 0)
        assert False, "Expected ValueError for difficulty=0"
    except ValueError:
        pass


def run_all_tests():
    """Run every test function and report pass/fail counts."""
    tests = [
        # Positive
        test_song_total_minutes,
        test_song_session_count,
        test_song_average_difficulty,
        test_musician_log_session,
        test_musician_weekly_total,
        test_song_readiness_score,
        test_songs_needing_attention_order,
        test_practice_session_to_and_from_dict,
        # Edge
        test_song_no_sessions,
        test_musician_no_songs_weekly_total,
        # Negative
        test_negative_duration_raises,
        test_difficulty_out_of_range_raises,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__} - {e}")
        except Exception as e:
            print(f"ERROR: {test.__name__} - {type(e).__name__}: {e}")

    print(f"\n{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    run_all_tests()
