import os
from flask import Flask, render_template, request, redirect, url_for
from . weather import main as get_weather
from typing import Optional, Any
from . database_operations import insert_data, find_data
from passlib.hash import pbkdf2_sha256

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
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Check if email or username already exists
        email_exists = find_data({"email": user_data["email"]})
        username_exists = find_data({"username": user_data["username"]})

        if email_exists or username_exists:
            # Redirect to 'testing' page if email or username exists
            return redirect(url_for('registererror'))

        # If email and username are unique, hash password and create a new user
        user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
        response = insert_data(user_data)

        # Check if the user was successfully inserted
        if response.get('insertedId'):
            # Redirect to the 'testing' page
            return redirect(url_for('registersuccess'))
        
        return render_template('register.html')
    else:
        return render_template('register.html')  # Show the form on GET request


@app.route('/registererror')
def registererror() -> str:
    return render_template('registererror.html')
    # Replace with a proper HTML template if necessary

@app.route('/registersuccess')
def registersuccess() -> str:
    return render_template('registersuccess.html')
    # Replace with a proper HTML template if necessary


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
