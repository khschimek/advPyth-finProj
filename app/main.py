import os
from flask import Flask, render_template, request
from weather import main as get_weather
from typing import Optional, Any
from database_operations import insert_data
from passlib.hash import sha256_crypt

app = Flask(__name__)


weather_data = {}


@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    data: Optional[Any] = None
    data = get_weather('grand junction', 'co', 'usa')

    global weather_data
    nyData = get_weather("new york city", "ny", "usa")
    chData = get_weather("chicago", "il", "usa")
    deData = get_weather("denver", "co", "usa")
    laData = get_weather("los angeles", "ca", "usa")

    weather_data['ny'] = nyData
    weather_data['ch'] = chData
    weather_data['de'] = deData
    weather_data['la'] = laData

    return render_template('home.html', data=data, weather_data=weather_data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard() -> str:
    data: Optional[Any] = None
    if request.method == 'POST':
        # Fallback to empty string if None
        city = request.form.get('cityName') or ''
        # Fallback to empty string if None
        state = request.form.get('stateName') or ''
        # Fallback to empty string if None
        country = request.form.get('countryName') or ''
        data = get_weather(city, state, country)

    return render_template('dashboard.html', data=data,
                           weather_data=weather_data)


@app.route('/login', methods=['GET', 'POST'])
def login_user() -> str:
    if request.method == 'POST':
        user_data = {
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        insert_data(user_data)
        # Convert the response to a string if necessary
        return render_template('login.html')
    else:
        return render_template('login.html')  # Show the form on GET request


@app.route('/register', methods=['GET', 'POST'])
def register_user() -> str:
    if request.method == 'POST':
        user_data = {
            "first_name": request.form.get('fname'),
            "last_name": request.form.get('lname'),
            "email": request.form.get('email'),
            # Be cautious with password handling
            "password": request.form.get('password')
        }
        user_data['password'] = sha256_crypt.hash(user_data['password'])
        insert_data(user_data)
        # Convert the response to a string if necessary
        return render_template('register.html')
    else:
        return render_template('register.html')  # Show the form on GET request


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
