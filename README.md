# Steps

It tells you to walk.

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

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that checks your real step count and nudges you to move. Connects to Oura Ring, Apple Watch, Garmin, Fitbit, or WHOOP. One skill. One job.

## The Killer Feature: iMessage Nudges

Your Mac texts you your step count **4 times a day** — 10am, 2pm, 6pm, 9pm. No app to open. No notification to swipe away. An iMessage you actually read.

```
Morning:   "842 steps. Take a 10 min walk before you start. Fresh air = better code."
Afternoon: "Only 3,201 steps. It's 2pm. Go outside for 15 minutes. 6,799 to go."
Evening:   "Almost there — just 1,580 more. Quick walk after dinner?"
Night:     "Daily report — 10,421/10,000 steps. CRUSHED IT."
```

## Install

### 1. Copy the skill

```bash
mkdir -p ~/.claude/skills/steps
cp SKILL.md ~/.claude/skills/steps/SKILL.md
```

### 2. Connect your step data (pick one)

**Oura Ring** (real-time, recommended):
```bash
claude mcp add oura -- npx -y oura-ring-mcp
```
Get your token at [cloud.ouraring.com/personal-access-tokens](https://cloud.ouraring.com/personal-access-tokens)

**Apple Health** (free, export-based):
```bash
# Export from iPhone: Health app → Profile → Export All Health Data → AirDrop to Mac
python3 convert_health_xml.py ~/Downloads/apple_health_export/export.xml ~/apple-health-data
claude mcp add apple-health -- npx -y @neiltron/apple-health-mcp
```

**Garmin / Fitbit / WHOOP:**
```bash
claude mcp add garmin -- npx -y @nicolasvegam/garmin-connect-mcp
claude mcp add fitbit -- npx -y mcp-fitbit
claude mcp add whoop -- npx -y whoop-mcp
```

### 3. Set up iMessage nudges (macOS)

```bash
# Edit health-coach.py — set your phone number and health data path
# Then test it:
python3 health-coach.py test

# Add to crontab:
crontab -e
```

```cron
0 10 * * * python3 /path/to/health-coach.py morning
0 14 * * * python3 /path/to/health-coach.py afternoon
0 18 * * * python3 /path/to/health-coach.py evening
0 21 * * * python3 /path/to/health-coach.py night
```

## Usage

| Command | What you get |
|---------|-------------|
| `/steps` | Step count + nudge |
| `/steps 8000` | Set daily goal |
| `/steps walk` | "Go walk" with context |
| `go for a walk` | Auto-triggers |
| `how many steps` | Auto-triggers |

## What's Inside

| File | What it does |
|------|-------------|
| `SKILL.md` | The Claude Code skill — copy to `~/.claude/skills/steps/` |
| `health-coach.py` | iMessage cron script — texts you 4x daily |
| `convert_health_xml.py` | Apple Health XML → CSV converter (saves $0.99) |
| `SETUP.md` | Detailed setup guide |

## Invisible Psychology

If you have a `CLAUDE.md` with notes about how you think (ADHD, competitive, reward-driven), Steps reads it silently and adapts its tone. You never see "psychology engine" — you just notice the nudges hit different.

No `CLAUDE.md`? Works fine with a direct, friendly default tone.

## Why This Exists

Every fitness app asks you to come to IT. Open the app. Check the dashboard. Log the data. That's friction. That's why they fail.

Steps lives where you already are — in Claude Code. And the iMessage cron means you don't even need to be in Claude Code. Your Mac just texts you. That's it.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- macOS (for iMessage nudges — the skill itself works anywhere)
- One step data source (Oura, Apple Health, Garmin, Fitbit, or WHOOP)

## License

MIT
