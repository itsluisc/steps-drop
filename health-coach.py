#!/usr/bin/env python3
"""
Steps — iMessage Walk Reminder
Texts you your step count 4x daily. The frictionless way to hit 10K steps.

Setup:
  1. Edit PHONE below to your own number
  2. Edit HEALTH_DIR to your Apple Health CSV folder
  3. Add to crontab (run: crontab -e):
     0 10 * * * python3 /path/to/health-coach.py morning
     0 14 * * * python3 /path/to/health-coach.py afternoon
     0 18 * * * python3 /path/to/health-coach.py evening
     0 21 * * * python3 /path/to/health-coach.py night

  Test without sending: python3 health-coach.py test

Requirements: macOS only (uses iMessage via AppleScript). No pip installs.
"""

import csv
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# EDIT THESE TWO LINES
# ============================================================
HEALTH_DIR = Path.home() / "apple-health-data"  # Where your CSVs live
PHONE = "+1XXXXXXXXXX"                           # Your phone number (texts yourself)
# ============================================================

STEPS_FILE = HEALTH_DIR / "HKQuantityTypeIdentifierStepCount.csv"
WORKOUT_FILE_PREFIX = "HKWorkoutActivityType"

# Goals
STEP_GOAL = 10000
MORNING_MINIMUM = 1000    # by 10am
AFTERNOON_MINIMUM = 4000  # by 2pm
EVENING_MINIMUM = 7000    # by 6pm

def send_imessage(message):
    """Send iMessage to self."""
    script = f'''
    tell application "Messages"
        set targetService to 1st account whose service type = iMessage
        set targetBuddy to participant "{PHONE}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)

def get_steps_today():
    """Read today's step count from Apple Health CSV."""
    if not STEPS_FILE.exists():
        return 0

    today = datetime.now().strftime("%Y-%m-%d")
    total = 0

    with open(STEPS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = row.get("startDate", "")
            if today in start:
                try:
                    total += float(row.get("value", 0))
                except (ValueError, TypeError):
                    pass

    return int(total)

def had_workout_today():
    """Check if any workout was logged today."""
    today = datetime.now().strftime("%Y-%m-%d")

    for f in HEALTH_DIR.glob(f"{WORKOUT_FILE_PREFIX}*.csv"):
        with open(f, "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if today in row.get("startDate", ""):
                    return True
    return False

def morning_check():
    """10 AM — gentle start."""
    steps = get_steps_today()
    if steps < MORNING_MINIMUM:
        send_imessage(
            f"Morning. {steps:,} steps so far. "
            f"Take a 10 min walk before you start working. "
            f"Fresh air = better focus. Goal: {STEP_GOAL:,} today."
        )
    else:
        send_imessage(
            f"Already at {steps:,} steps this morning. Good start. "
            f"Keep it up — {STEP_GOAL:,} is the target."
        )

def afternoon_check():
    """2 PM — mid-day nudge."""
    steps = get_steps_today()
    remaining = max(0, STEP_GOAL - steps)

    if steps < AFTERNOON_MINIMUM:
        send_imessage(
            f"Only {steps:,} steps today. "
            f"It's 2pm. Go outside for 15 minutes right now. "
            f"{remaining:,} steps to go."
        )
    elif steps < 6000:
        send_imessage(
            f"{steps:,} steps — decent but not there yet. "
            f"Walk after your next task. {remaining:,} to go."
        )

def evening_check():
    """6 PM — final push."""
    steps = get_steps_today()
    remaining = max(0, STEP_GOAL - steps)
    workout = had_workout_today()

    msg = f"Evening check: {steps:,} steps today."

    if steps < EVENING_MINIMUM:
        msg += f" You need {remaining:,} more. Go for a 30 min walk NOW."
    elif steps < STEP_GOAL:
        msg += f" Almost there — just {remaining:,} more. Quick walk after dinner?"
    else:
        msg += f" CRUSHED IT. {steps:,}/{STEP_GOAL:,} steps."

    if not workout:
        msg += " No workout logged — even 20 min counts."

    send_imessage(msg)

def night_summary():
    """9 PM — daily summary."""
    steps = get_steps_today()
    workout = had_workout_today()
    hit_goal = steps >= STEP_GOAL

    if hit_goal and workout:
        verdict = "MASSIVE day"
    elif hit_goal:
        verdict = "Steps crushed, no workout tho"
    elif workout:
        verdict = f"Workout done but only {steps:,} steps"
    else:
        verdict = f"Only {steps:,} steps and no workout. Tomorrow we go harder"

    send_imessage(
        f"Daily report — {verdict}. "
        f"{steps:,}/{STEP_GOAL:,} steps | "
        f"Workout: {'Yes' if workout else 'No'}. "
        f"Consistency > intensity. Show up tomorrow."
    )

if __name__ == "__main__":
    if PHONE == "+1XXXXXXXXXX":
        print("ERROR: Edit PHONE in this file to your phone number first!")
        print("       Also edit HEALTH_DIR to point to your Apple Health CSV folder.")
        sys.exit(1)

    mode = sys.argv[1] if len(sys.argv) > 1 else "afternoon"

    if mode == "morning":
        morning_check()
    elif mode == "afternoon":
        afternoon_check()
    elif mode == "evening":
        evening_check()
    elif mode == "night":
        night_summary()
    elif mode == "test":
        steps = get_steps_today()
        workout = had_workout_today()
        print(f"Steps today: {steps:,}")
        print(f"Workout today: {workout}")
        print(f"Step goal: {STEP_GOAL:,}")
        print(f"Remaining: {max(0, STEP_GOAL - steps):,}")
    else:
        print(f"Usage: python3 health-coach.py [morning|afternoon|evening|night|test]")
