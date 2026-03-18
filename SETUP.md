# Steps — Quick Start

It tells you to walk. That's it.

## Install the skill

```bash
mkdir -p ~/.claude/skills/steps
cp SKILL.md ~/.claude/skills/steps/SKILL.md
```

## Connect your step data (pick one)

### Option A: Oura Ring (real-time, recommended)

```bash
claude mcp add oura -- npx -y oura-ring-mcp
```

Get your access token at https://cloud.ouraring.com/personal-access-tokens
Add it to `~/.claude.json`:
```json
{
  "mcpServers": {
    "oura": {
      "command": "npx",
      "args": ["-y", "oura-ring-mcp"],
      "env": {
        "OURA_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Option B: Apple Health (free, export-based)

1. iPhone → Health app → Profile pic (top right) → Export All Health Data
2. AirDrop the zip to your Mac
3. Unzip it
4. Convert XML to CSVs (this saves you the $0.99 app):

```bash
mkdir -p ~/apple-health-data
python3 convert_health_xml.py ~/Downloads/apple_health_export/export.xml ~/apple-health-data
```

5. Install the MCP:
```bash
claude mcp add apple-health -- npx -y @neiltron/apple-health-mcp
```

Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "apple-health": {
      "command": "npx",
      "args": ["-y", "@neiltron/apple-health-mcp"],
      "env": {
        "HEALTH_DATA_DIR": "/Users/YOURUSERNAME/apple-health-data"
      }
    }
  }
}
```

### Option C: Garmin / Fitbit / WHOOP

```bash
claude mcp add garmin -- npx -y @nicolasvegam/garmin-connect-mcp
claude mcp add fitbit -- npx -y mcp-fitbit
claude mcp add whoop -- npx -y whoop-mcp
```

## Set up iMessage nudges (the frictionless way)

This is the killer feature. Your Mac texts you your step count 4x daily.

1. Edit `health-coach.py`:
   - Set `PHONE` to your phone number
   - Set `HEALTH_DIR` to your Apple Health CSV folder

2. Test it:
```bash
python3 health-coach.py test
```

3. Add to crontab:
```bash
crontab -e
```

Add these 4 lines:
```
0 10 * * * python3 /full/path/to/health-coach.py morning
0 14 * * * python3 /full/path/to/health-coach.py afternoon
0 18 * * * python3 /full/path/to/health-coach.py evening
0 21 * * * python3 /full/path/to/health-coach.py night
```

Now you get step count texts at 10am, 2pm, 6pm, and 9pm. No app to open. No notification to swipe. An iMessage you actually read.

## Use it

```
/steps              → check your steps right now
/steps 8000         → change your daily goal
/steps walk         → "go walk" with context
"go for a walk"     → triggers automatically
"how many steps"    → triggers automatically
```

That's it. One skill. One job. Walk.
