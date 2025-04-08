from flask import Blueprint, render_template, request
import requests
from config import API_KEY, BASE_URL

weather_bp = Blueprint('weather', __name__)

def get_weather(city):
    response = requests.get(f"{BASE_URL}?q={city}&units=imperial&APPID={API_KEY}")
    data = response.json()
    
    if data.get("cod") == '404':
        return None
    else:
        return {
            "city": city,
            "weather": data["weather"][0]["main"],
            "temperature": round(data["main"]["temp"])
        }

@weather_bp.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data)
