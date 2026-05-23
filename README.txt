GigReady - Music Practice Tracker
==================================

HOW TO RUN
----------
Run the following command in your terminal:
    python3 main.py

No external libraries required. Uses Python built-in modules only (json, datetime, os).

FILES
-----
main.py       - Main program. Run this file to start the application.
models.py     - Class definitions and readiness scoring logic.
file_io.py    - Functions to save and load data (gigready_data.json).
tests.py      - Assert-based test suite. Run with: python3 tests.py

DATA
----
Practice data is automatically saved to gigready_data.json in the project folder.
This file is created on first save and loaded on startup.

ADVANCED TOPICS USED
--------------------
- Classes/Objects (Week 7): Song, PracticeSession, Musician classes
- Advanced Flow / Exception Handling (Week 8): try-except in file_io.py and prompt_int()
- File I/O (Week 9): JSON read/write in file_io.py
- Testing with assert (Week 10): 13 test cases in tests.py

MAIN FEATURES
-------------
- Log practice sessions by song
- View totals and average difficulty
- ASCII bar chart of practice time per song
- Set and track a weekly practice goal
- Generate a gig readiness report that recommends which songs need attention
- Generate today's practice plan based on readiness scores
- Export a plain-text practice report to gigready_report.txt
