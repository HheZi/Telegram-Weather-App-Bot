# Telegram Weather Bot

Simple Telegram bot that lets users set a default city and get current weather or a 5-day forecast.

**What it is:**
- A small Python bot using `pyTelegramBotAPI` to interact with users.
- Stores per-user city and state in a local SQLite database (`database.db`).
- Fetches weather data via an external weather API (requires a `WEATHER_TOKEN`).

**Prerequisites**
- Python 3.8+ installed
- Create a virtual environment (recommended)
- Required packages (install into the venv): `pyTelegramBotAPI`, `python-dotenv`, `requests`

Example install:
```bash
python -m venv venv
source venv/bin/activate
pip install pyTelegramBotAPI python-dotenv requests
```

**Configuration**
- Create a `.env` file in the project root with the following variables:

```
BOT_TOKEN=<your-telegram-bot-token>
WEATHER_TOKEN=<your-weather-api-token>
```

**Files of interest**
- `bot.py` — main bot logic and command handlers
- `weatherservice.py` — weather API wrapper (calls the weather provider)
- `dbworker.py` — SQLite helpers
- `config.py` — tokens and app state definitions
- `start_bot.sh` / `start_bot.bat` — convenience scripts to run the bot

**Run the bot (Linux / macOS)**
```bash
./start_bot.sh
```

**Run the bot (Windows, from project root)**
```powershell
start_bot.bat
```

**Notes**
- Ensure `BOT_TOKEN` and `WEATHER_TOKEN` are valid before starting the bot.
- The first run will create `database.db` automatically.
- For development, use the shell script; for deployment, run `bot.py` under a process manager.