from telebot import types, TeleBot
import weatherservice, dbworker, config
from states import States

print("Starting the bot")
bot = TeleBot(config.bot_token)
dbworker.init_database()
print("The bot has been started")

@bot.message_handler(commands=["start"])
def start(message: str) -> None:
    bot.send_message(message.chat.id, "Hello")
    set_user_city(message)

@bot.message_handler(func=lambda message: message.text == "🏙 Set City")
def set_user_city(message: str) -> None:
    bot.send_message(message.chat.id, "Set a city for a weather report")

    dbworker.update_user_current_state(message.chat.id, States.S_ENTER_CITY)

@bot.message_handler(func=lambda message: dbworker.get_user_current_state(message.chat.id) == States.S_ENTER_CITY.value)
def enter_city(message: str) -> None:
    city_name = message.text;

    dbworker.set_user_city(message.chat.id, city_name)

    bot.send_message(message.chat.id, f"'{city_name}' is successfully set as a default city for a weather report")

    dbworker.update_user_current_state(message.chat.id, States.S_CITY_SETTED)
    main_menu(message.chat.id)


@bot.message_handler(func=lambda message: 
    dbworker.get_user_current_state(message.chat.id) == States.S_CITY_SETTED.value 
    and message.text == "🌤 Current Weather"
)
def get_current_weather_report(message: str) -> None:
    city_name = dbworker.get_user_city_name(message.chat.id)

    report = weatherservice.get_current_weather_for_city(city_name)

    bot.send_message(message.chat.id, report)

@bot.message_handler(func=lambda message: 
    dbworker.get_user_current_state(message.chat.id) == States.S_CITY_SETTED.value 
    and message.text == "📅 5-Day Forecast"
) 
def get_five_day_weather_report(message: str) -> None:
    city_name = dbworker.get_user_city_name(message.chat.id)
    
    report = weatherservice.get_five_day_weather_report_for_city(city_name)

    bot.send_message(message.chat.id, report)

def main_menu(chat_id: str) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_current = types.KeyboardButton("🌤 Current Weather")
    btn_forecast = types.KeyboardButton("📅 5-Day Forecast")
    btn_set_city = types.KeyboardButton("🏙 Set City")
    markup.add(btn_current, btn_forecast, btn_set_city)
    
    bot.send_message(chat_id, "Choose an option:", reply_markup=markup)

if __name__ == '__main__':  
     bot.infinity_polling() 
