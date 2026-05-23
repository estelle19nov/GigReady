# GigReady

A command-line music practice tracker for musicians who want their practice to count.

GigReady doesn't just log sessions - it scores every song from 0-100 with a **Gig Readiness Report**, so you always know which song needs the most attention before your next performance.

## Features

- Log practice sessions per song (duration, difficulty, notes)
- View totals and average difficulty across your repertoire
- Set and track a weekly practice goal with a progress bar
- **Gig Readiness Report** - scores each song and recommends what to practise next
- **Practice Time Chart** - horizontal ASCII bar chart of minutes per song
- **Today's Practice Plan** - auto-generated plan that prioritises weaker songs
- **Export Practice Report** - save a plain-text summary of all stats to disk
- Data is saved when you choose "Save and quit"

## How to Run

```bash
python3 main.py
```

No external libraries required. Uses only Python built-in modules (`json`, `datetime`, `os`).

## Run the Tests

```bash
python3 tests.py
```

13 tests covering positive, edge, and negative cases.

## Files

| File | Purpose |
|---|---|
| `main.py` | Main program with menu loop |
| `models.py` | `Song`, `PracticeSession`, `Musician` classes + readiness scoring and practice planning |
| `file_io.py` | Save/load data as JSON and export a text report |
| `tests.py` | Assert-based test suite |

## Built With

Course: **COMP9001 - Introduction to Programming** (University of Sydney)

Advanced topics demonstrated:
- Classes / Objects (Week 7)
- Exception Handling - `try-except`, `raise` (Week 8)
- File I/O - JSON read/write and text report export (Week 9)
- Testing with `assert` - positive / edge / negative cases (Week 10)
