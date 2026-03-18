---
name: steps
description: "Steps — it tells you to walk. Connects to Oura Ring, Apple Watch, Garmin, Fitbit, or Apple Health export for your real step count, then nudges you to move. Reads your CLAUDE.md to coach YOU, not generic fitness advice. Triggers: 'steps', 'how many steps', 'should I walk', 'go for a walk', 'step count', 'steps today', '/steps'"
argument-hint: "[check, walk, or goal number]"
---

# Steps — It tells you to walk.

> "2,899 steps. Walk. Now. 10 min."

## What This Is

One skill. One job. Check your steps. Tell you to move.

No nutrition. No macros. No water glasses. No sleep analysis. Just the one thing every desk worker needs: someone who tells them to stand up and walk.

It lives in Claude Code — where you already are. Not a separate app you ignore.

## How It Works

```
Step count (from your wearable or phone)
  + Time of day (morning gentle, afternoon direct, evening urgent)
  + CLAUDE.md psychology (invisible — adapts tone to YOUR brain)
  = The right nudge at the right moment
```

## Get The Number

Steps connects to whatever you have. Pick one:

| Device | MCP Server | Install | Real-Time? |
|--------|-----------|---------|-----------|
| **Oura Ring** | `oura-ring-mcp` | `claude mcp add oura -- npx -y oura-ring-mcp` | Yes |
| **Apple Watch** | `apple-health-mcp` | `claude mcp add apple-health -- npx -y @neiltron/apple-health-mcp` | Export-based |
| **Garmin** | `garmin-connect-mcp` | `claude mcp add garmin -- npx -y @nicolasvegam/garmin-connect-mcp` | Yes |
| **Fitbit** | `mcp-fitbit` | `claude mcp add fitbit -- npx -y mcp-fitbit` | Yes |
| **WHOOP** | `whoop-mcp` | `claude mcp add whoop -- npx -y whoop-mcp` | Yes |

**No wearable?** Export Apple Health from your iPhone (Settings → Health → Export All Health Data), unzip, and convert with the included `convert_health_xml.py` script. Free. Works on any Mac.

**Data priority:** Try MCP tools first (real-time). Fall back to Apple Health CSV. The skill auto-detects what's available.

## The Output

When triggered, show this:

```
╔══════════════════════════════════╗
║  STEPS — Mon Mar 17, 6:14 PM    ║
╠══════════════════════════════════╣
║                                  ║
║  2,899 / 10,000    29%          ║
║  ██████░░░░░░░░░░░░░░  7,101 to go  ║
║                                  ║
║  Walk. 15 minutes. Now.          ║
║                                  ║
╚══════════════════════════════════╝
```

## The Nudge (Invisible Psychology)

If the user has a `CLAUDE.md` or `~/.claude/CLAUDE.md`, read it silently. Adapt tone. Never mention "psychology engine" or "ADHD detected" — just nudge differently.

**ADHD noted?** → Short. Punchy. No guilt. "Walk. Now. 10 min."
**Competitive personality?** → "You had 8,200 by now yesterday. Today: 2,899."
**Reward-motivated?** → "Hit 5K steps. Earn that coffee."
**Frustrated right now?** → "10-min walk. Not fitness. Debugging advice. Fresh eyes."

**No CLAUDE.md?** Default to direct, friendly tone. No onboarding needed.

**Time-based nudge rules:**

| Time | Steps Status | Nudge |
|------|-------------|-------|
| Morning (<12pm) | Low | "Quick 10-min walk before deep work. Fresh air = better code." |
| Afternoon (12-5pm) | Behind pace | "[X] steps at [time]. 15 minutes. Go." |
| Evening (5pm+) | Behind pace | "You need [Y] more. Walk after dinner." |
| Any time | On pace | "[X] steps. On track." |
| Any time | Goal hit | "[X] / 10,000. Crushed it." |

## iMessage Nudges (The Frictionless Way)

The real magic: Steps texts you throughout the day. You don't open an app. You don't check a dashboard. Your phone buzzes with your step count and a nudge — 4 times a day.

### Setup (macOS only — uses iMessage via AppleScript)

1. Copy `health-coach.py` to anywhere on your Mac
2. Edit the `PHONE` variable to your own number (texts yourself)
3. Edit `HEALTH_DIR` to point to your Apple Health CSV folder
4. Add to crontab:

```bash
crontab -e
# Add these 4 lines:
0 10 * * * python3 /path/to/health-coach.py morning
0 14 * * * python3 /path/to/health-coach.py afternoon
0 18 * * * python3 /path/to/health-coach.py evening
0 21 * * * python3 /path/to/health-coach.py night
```

Now your Mac texts you at 10am, 2pm, 6pm, and 9pm with your step count and a nudge. No app. No notification you swipe away. An iMessage from yourself that you actually read.

**Test it first:**
```bash
python3 health-coach.py test
# Shows your steps, workout status, goal — no message sent
```

## Goal

Default: **10,000 steps/day.**

Change it: `/steps 8000` → saves to `~/.claude/skills/steps/goal.json`

## Commands

| Say | Get |
|-----|-----|
| `/steps` | Step count + nudge |
| `/steps 8000` | Set goal to 8,000 |
| `/steps walk` | "Go walk" with context |
| "go for a walk" | Same as `/steps walk` |
| "how many steps" | Same as `/steps` |

## What's Included

```
steps-drop/
├── SKILL.md              ← This file (copy to ~/.claude/skills/steps/)
├── health-coach.py       ← iMessage cron nudger (the frictionless way)
├── convert_health_xml.py ← Apple Health XML → CSV (saves $0.99)
└── SETUP.md              ← Quick start guide
```
