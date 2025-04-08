from flask import Flask, render_template, request
import requests
import logging
from config import API_KEY, BASE_URL

app = Flask(__name__)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

def get_weather(city):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        response = requests.get(f"{BASE_URL}?q={city}&units=imperial&APPID={API_KEY}")
        data = response.json()
        
        logging.debug(f"API Response: {data}")  # Debugging log

        if data.get("cod") != 200:
            return None  # City not found or API error

        return {
            "city": city,
            "weather": data.get("weather", [{}])[0].get("main", "No Data"),
            "temperature": round(data.get("main", {}).get("temp", 0)),
            "humidity": data.get("main", {}).get("humidity", "N/A"),
            "wind_speed": data.get("wind", {}).get("speed", "N/A")
        }

    except Exception as e:
        logging.error(f"Error fetching weather: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home route for weather search"""
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        weather_data = get_weather(city)

    return render_template('index.html', weather=weather_data)

# In-memory database for demonstration
person_database = []

@app.route('/person/search', methods=['GET', 'POST'])
def search_person():
    """Search for a person in the database."""
    search_results = []
    if request.method == 'POST':
        name = request.form.get('name', '').lower()
        search_results = [person for person in person_database if name in person['name'].lower()]
    return render_template('search_person.html', results=search_results)

@app.route('/person/report', methods=['GET', 'POST'])
def report_person():
    """Report a missing or found person."""
    message = None
    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')
        person_database.append({'name': name, 'status': status})
        message = f"Person '{name}' reported as '{status}'."
    return render_template('report_person.html', message=message)

# In-memory database for rescue volunteers
rescue_volunteers = []

@app.route('/volunteer/add', methods=['GET', 'POST'])
def add_volunteer():
    """Add a new rescue volunteer."""
    message = None
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        skill = request.form.get('skill')
        rescue_volunteers.append({'name': name, 'contact': contact, 'skill': skill})
        message = f"Rescue Volunteer '{name}' added successfully."
    return render_template('add_volunteer.html', message=message)

@app.route('/volunteer/list', methods=['GET'])
def list_volunteers():
    """List all rescue volunteers."""
    return render_template('list_volunteers.html', volunteers=rescue_volunteers)

if __name__ == "__main__":
    app.run(debug=True)
