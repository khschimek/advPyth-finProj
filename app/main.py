import os
from flask import Flask, render_template, request
from app.weather import main as get_weather
from typing import Optional, Any
from app.database_operations import insert_data

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    data: Optional[Any] = None
    if request.method == 'POST':
        # Fallback to empty string if None
        city = request.form.get('cityName') or ''
        # Fallback to empty string if None
        state = request.form.get('stateName') or ''
        # Fallback to empty string if None
        country = request.form.get('countryName') or ''
        data = get_weather(city, state, country)
    return render_template('home.html', data=data)


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
    return render_template('dashboard.html', data=data)


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
        insert_data(user_data)
        # Convert the response to a string if necessary
        return render_template('register.html')
    else:
        return render_template('register.html')  # Show the form on GET request


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
