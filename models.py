# models.py - Class definitions for GigReady
# Contains: Song, PracticeSession, Musician
# Author: Estelle


class Song:
    """Represents a song the user is practising."""

    def __init__(self, title):
        """Create a new Song with no sessions yet."""
        self.title = title
        self.sessions = []  # list of PracticeSession objects

    def add_session(self, session):
        """Attach a PracticeSession to this song."""
        self.sessions.append(session)

    def total_minutes(self):
        """Return total minutes practised across all sessions."""
        return sum(s.duration for s in self.sessions)

    def session_count(self):
        """Return the number of practice sessions logged for this song."""
        return len(self.sessions)

    def average_difficulty(self):
        """Return the mean difficulty across all sessions, or 0 if none."""
        if not self.sessions:
            return 0
        return sum(s.difficulty for s in self.sessions) / len(self.sessions)

    def readiness_score(self):
        """Return a 0-100 estimate of how ready this song is for a gig."""
        if not self.sessions:
            return 0

        practice_points = min(self.total_minutes(), 100)
        consistency_points = min(self.session_count() * 10, 30)
        difficulty_penalty = self.average_difficulty() * 5
        score = practice_points + consistency_points - difficulty_penalty
        return max(0, min(100, round(score)))


class PracticeSession:
    """Represents a single practice session for a song."""

    def __init__(self, date, duration, difficulty, notes=""):
        """Create a session. Raises ValueError if duration or difficulty is invalid."""
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        if not (1 <= difficulty <= 5):
            raise ValueError("Difficulty must be between 1 and 5.")
        self.date = date          # string, e.g. "2026-05-18"
        self.duration = duration  # int, minutes
        self.difficulty = difficulty  # int 1-5
        self.notes = notes

    def to_dict(self):
        """Convert this session to a dict for JSON saving."""
        return {
            "date": self.date,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "notes": self.notes
        }

    @staticmethod
    def from_dict(data):
        """Rebuild a PracticeSession from a dict loaded from JSON."""
        return PracticeSession(
            date=data["date"],
            duration=data["duration"],
            difficulty=data["difficulty"],
            notes=data.get("notes", "")
        )


class Musician:
    """Represents the user. Stores their songs and weekly practice goal."""

    def __init__(self, name, weekly_goal=0):
        """Create a Musician with an empty song collection."""
        self.name = name
        self.weekly_goal = weekly_goal  # target minutes per week
        self.songs = {}  # title (str) -> Song object

    def get_or_create_song(self, title):
        """Return the Song with this title, creating it if it doesn't exist."""
        if title not in self.songs:
            self.songs[title] = Song(title)
        return self.songs[title]

    def log_session(self, title, session):
        """Log a practice session under the given song title."""
        song = self.get_or_create_song(title)
        song.add_session(session)

    def total_minutes_this_week(self, current_week):
        """Sum minutes from sessions whose date falls within the given week.

        current_week is a list of ISO date strings (Mon-Sun).
        """
        total = 0
        for song in self.songs.values():
            for s in song.sessions:
                if s.date in current_week:
                    total += s.duration
        return total

    def songs_needing_attention(self):
        """Return songs sorted from least ready to most ready."""
        return sorted(
            self.songs.values(),
            key=lambda song: (song.readiness_score(), -song.average_difficulty())
        )

    def generate_practice_plan(self, num_songs=3):
        """Suggest songs to practise today based on readiness scores.

        Returns a list of (song, suggested_minutes) tuples, prioritising the
        weakest songs and assigning more minutes to lower scores.
        """
        weakest = self.songs_needing_attention()[:num_songs]
        plan = []
        for song in weakest:
            score = song.readiness_score()
            if score < 30:
                minutes = 25
            elif score < 60:
                minutes = 20
            else:
                minutes = 15
            plan.append((song, minutes))
        return plan
