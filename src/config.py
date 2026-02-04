from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
weather_token = os.getenv("WEATHER_TOKEN")
db_file = "database.db"

class States(Enum):
    S_ENTER_CITY = "0"
    S_CITY_SETTED = "1"