import config
from requests import get
from collections import defaultdict, Counter

def get_current_weather_for_city(city_name: str) -> str:
    data = get(
        url="https://api.openweathermap.org/data/2.5/weather", 
        params={"appid": config.weather_token, "q" : city_name, "units": "metric"}
    ).json()
    
    # 200 must be integer type
    if data["cod"] == 200:
        return parse_current_weather_report(data)
    # 404 must be str type
    elif data["cod"] == "404":
        return "City is not found"
    else:
        return "Something went wrong while getting weather report"

def get_five_day_weather_report_for_city(city_name) -> str:
    data = get(
        url="https://api.openweathermap.org/data/2.5/forecast",
        params={"appid": config.weather_token, "q" : city_name, "units": "metric"}
    ).json()

    if data["cod"] == "200":
        return format_five_day_report(parse_five_day_weather_report(data), city_name)
    elif data["cod"] == "404":
        return "City is not found"
    else:
        return "Something went wrong while getting weather report" 


def parse_current_weather_report(data):
    name = data["name"]
    country = data["sys"]["country"]

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    message = (
        f"🌤 Weather in *{name}, {country}*\n"
        f"• Condition: *{description}*\n"
        f"• Temperature: *{temp:.1f}°C* (feels like *{feels:.1f}°C*)\n"
        f"• Humidity: *{humidity}%*\n"
        f"• Pressure: *{pressure} hPa*\n"
        f"• Wind: *{wind_speed} m/s*"
    )

    return message

def parse_five_day_weather_report(data) -> dict:
    daily = defaultdict(lambda: {
        "temps": [],
        "feels": [],
        "descriptions": [],
        "icons": []
    })

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]

        daily[date]["temps"].append(entry["main"]["temp"])
        daily[date]["feels"].append(entry["main"]["feels_like"])
        daily[date]["descriptions"].append(entry["weather"][0]["description"])
        daily[date]["icons"].append(entry["weather"][0]["icon"])

    summary = {}

    for date, values in daily.items():
        summary[date] = {
            "temp_min": round(min(values["temps"]), 1),
            "temp_max": round(max(values["temps"]), 1),
            "feels_min": round(min(values["feels"]), 1),
            "feels_max": round(max(values["feels"]), 1),
            "description": Counter(values["descriptions"]).most_common(1)[0][0],
            "icon": Counter(values["icons"]).most_common(1)[0][0]
        }

    return summary

def format_five_day_report(summary: dict, city_name: str) -> str:
    message = f"📍 5-Day Forecast for *{city_name}*\n\n"
    for date, values in summary.items():
        message += (
            f"Date: {date}\n"
            f"Temp: {values['temp_min']}°C → {values['temp_max']}°C\n"
            f"Feels: {values['feels_min']}°C → {values['feels_max']}°C\n"
            f"Condition: {values['description'].title()}\n\n"
        )
    return message































