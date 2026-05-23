# GigReady - Music Practice Tracker
# RUN THIS FILE: python3 main.py
# Author: Estelle
# Description: A command-line program for musicians to log practice sessions,
#              track progress across songs, set weekly goals, and estimate gig readiness.

import datetime
from models import Musician, PracticeSession
from file_io import save_data, load_data, export_report


def get_today():
    """Return today's date as an ISO format string (e.g. '2026-05-18')."""
    return datetime.date.today().isoformat()


def get_this_week_dates():
    """Return a list of ISO date strings for every day in the current week (Mon-Sun)."""
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    return [(start + datetime.timedelta(days=i)).isoformat() for i in range(7)]


def prompt_int(prompt, min_val, max_val):
    """Ask user for an integer within a range, keep asking until valid."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def log_session(musician):
    """Prompt the user to log a new practice session for a song."""
    print("\n--- Log Practice Session ---")
    title = input("Song title: ").strip()
    if not title:
        print("Song title cannot be empty.")
        return

    duration = prompt_int("Duration (minutes): ", 1, 600)
    difficulty = prompt_int("Difficulty (1 = easy, 5 = very hard): ", 1, 5)
    notes = input("Notes (optional, press Enter to skip): ").strip()

    session = PracticeSession(
        date=get_today(),
        duration=duration,
        difficulty=difficulty,
        notes=notes
    )
    musician.log_session(title, session)
    print(f"Session logged for '{title}'!")


def view_all_songs(musician):
    """Display a summary table of all songs and their practice statistics."""
    print("\n--- All Songs ---")
    if not musician.songs:
        print("No songs logged yet.")
        return

    print(f"{'Song':<30} {'Sessions':>8} {'Total Min':>10} {'Avg Difficulty':>15}")
    print("-" * 65)
    for title, song in musician.songs.items():
        print(f"{title:<30} {song.session_count():>8} {song.total_minutes():>10} {song.average_difficulty():>14.1f}")


def view_weekly_goal(musician):
    """Show the user's weekly practice goal and current progress as a progress bar."""
    print("\n--- Weekly Goal ---")
    if musician.weekly_goal == 0:
        print("No weekly goal set. Use option 4 to set one.")
        return

    this_week = get_this_week_dates()
    done = musician.total_minutes_this_week(this_week)
    goal = musician.weekly_goal
    percent = min(int(done / goal * 100), 100)
    bar = "#" * (percent // 5) + "-" * (20 - percent // 5)

    print(f"Goal: {goal} min/week")
    print(f"Done this week: {done} min")
    print(f"Progress: [{bar}] {percent}%")

    if done >= goal:
        print("Goal reached! Great work!")
    else:
        print(f"{goal - done} minutes to go.")


def set_weekly_goal(musician):
    """Prompt the user to set a new weekly practice goal in minutes."""
    print("\n--- Set Weekly Goal ---")
    goal = prompt_int("Enter your weekly practice goal (minutes): ", 1, 10000)
    musician.weekly_goal = goal
    print(f"Weekly goal set to {goal} minutes.")


def view_song_detail(musician):
    """Display full session history and statistics for a specific song."""
    print("\n--- Song Detail ---")
    if not musician.songs:
        print("No songs logged yet.")
        return

    title = input("Enter song title: ").strip()
    if title not in musician.songs:
        print(f"'{title}' not found.")
        return

    song = musician.songs[title]
    print(f"\nSong: {song.title}")
    print(f"Total sessions: {song.session_count()}")
    print(f"Total time: {song.total_minutes()} minutes")
    print(f"Average difficulty: {song.average_difficulty():.1f}/5")
    print("\nSession history:")
    for i, s in enumerate(song.sessions, 1):
        note_str = f" | Notes: {s.notes}" if s.notes else ""
        print(f"  {i}. {s.date} | {s.duration} min | Difficulty: {s.difficulty}/5{note_str}")


def view_practice_chart(musician):
    """Show a horizontal ASCII bar chart of practice minutes per song."""
    print("\n--- Practice Time Chart ---")
    if not musician.songs:
        print("No songs logged yet.")
        return

    max_minutes = max(s.total_minutes() for s in musician.songs.values())
    if max_minutes == 0:
        print("No practice time logged.")
        return

    bar_max = 30  # max bar width in characters
    songs_sorted = sorted(
        musician.songs.values(),
        key=lambda s: -s.total_minutes()
    )

    for song in songs_sorted:
        minutes = song.total_minutes()
        bar_len = int((minutes / max_minutes) * bar_max)
        bar = "#" * bar_len
        print(f"{song.title:<20} |{bar:<30}| {minutes} min")


def view_practice_plan(musician):
    """Show today's suggested practice plan based on readiness scores."""
    print("\n--- Today's Practice Plan ---")
    if not musician.songs:
        print("No songs logged yet. Log a session first!")
        return

    plan = musician.generate_practice_plan(num_songs=3)
    total = sum(minutes for _, minutes in plan)

    print(f"Suggested session total: {total} minutes")
    print("-" * 50)
    for song, minutes in plan:
        score = song.readiness_score()
        print(f"  {song.title:<22} {minutes:>3} min   (readiness: {score:>3}/100)")
    print("\nTip: weaker songs get more time to bring them up to gig level.")


def export_practice_report(musician):
    """Save a human-readable practice report to disk and show the path."""
    print("\n--- Export Practice Report ---")
    if not musician.songs:
        print("No songs logged yet. Nothing to export.")
        return

    try:
        path = export_report(musician)
        print(f"Report saved to:\n  {path}")
    except OSError as e:
        print(f"Could not save report: {e}")


def view_readiness_report(musician):
    """Show which songs need the most attention before a performance."""
    print("\n--- Gig Readiness Report ---")
    if not musician.songs:
        print("No songs logged yet.")
        return

    songs = musician.songs_needing_attention()
    average_score = sum(song.readiness_score() for song in songs) / len(songs)

    print(f"Overall readiness: {average_score:.0f}/100")
    if average_score >= 80:
        print("Setlist status: performance ready.")
    elif average_score >= 50:
        print("Setlist status: almost there.")
    else:
        print("Setlist status: needs focused practice.")

    print(f"\n{'Song':<30} {'Score':>7} {'Next step':<25}")
    print("-" * 65)
    for song in songs:
        score = song.readiness_score()
        if score < 40:
            advice = "prioritise this song"
        elif score < 70:
            advice = "review weak sections"
        else:
            advice = "keep warm"
        print(f"{song.title:<30} {score:>6}/100  {advice:<25}")


BOX_WIDTH = 44


def print_banner():
    """Print the GigReady welcome banner."""
    inner = BOX_WIDTH - 2
    print("+" + "=" * inner + "+")
    print("|" + " " * inner + "|")
    print("|" + "G I G R E A D Y".center(inner) + "|")
    print("|" + "Track.  Practice.  Perform.".center(inner) + "|")
    print("|" + " " * inner + "|")
    print("+" + "=" * inner + "+")


def print_menu():
    """Print the main menu options to the console."""
    options = [
        "1.  Log a practice session",
        "2.  View all songs",
        "3.  View practice chart",
        "4.  View weekly goal progress",
        "5.  Set weekly goal",
        "6.  View song details",
        "7.  View gig readiness report",
        "8.  Today's practice plan",
        "9.  Export practice report",
        "10. Save and quit",
    ]
    inner = BOX_WIDTH - 2
    print()
    print("+" + "-" * inner + "+")
    print("|" + " MENU ".center(inner) + "|")
    print("+" + "-" * inner + "+")
    for opt in options:
        print("| " + opt.ljust(inner - 2) + " |")
    print("+" + "-" * inner + "+")


def main():
    """Main entry point: load data, run the menu loop, and save on exit."""
    print_banner()

    musician = load_data()
    if musician is None:
        name = input("First time here! Enter your name: ").strip()
        if not name:
            name = "Musician"
        musician = Musician(name=name)
        print(f"Welcome, {musician.name}!")
    else:
        print(f"Welcome back, {musician.name}!")

    while True:
        print_menu()
        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            log_session(musician)
        elif choice == "2":
            view_all_songs(musician)
        elif choice == "3":
            view_practice_chart(musician)
        elif choice == "4":
            view_weekly_goal(musician)
        elif choice == "5":
            set_weekly_goal(musician)
        elif choice == "6":
            view_song_detail(musician)
        elif choice == "7":
            view_readiness_report(musician)
        elif choice == "8":
            view_practice_plan(musician)
        elif choice == "9":
            export_practice_report(musician)
        elif choice == "10":
            save_data(musician)
            print("Data saved. See you next practice!")
            break
        else:
            print("Invalid option. Please choose 1-10.")


if __name__ == "__main__":
    main()
