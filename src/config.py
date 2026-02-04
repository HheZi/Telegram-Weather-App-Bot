import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
weather_token = os.getenv("WEATHER_TOKEN")
db_file = "database.db"