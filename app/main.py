import os
from flask import Flask, render_template, request
from flask import redirect, url_for, session
from werkzeug.wrappers import Response
from . weather import main as get_weather
from typing import Optional, Any, Union
from . database_operations import insert_data, find_data
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, UserMixin, LoginManager
from flask_login import login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_very_secret_and_random_key_here'


# Create an instance of LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_route'  # Name of the login route


weather_data = {}


class User(UserMixin):
    def __init__(self, id: Any, first_name: str,
                 last_name: str, username: str, email: str) -> None:
        self.id = str(id)  # ID is still kept for reference
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email

    def get_id(self) -> str:
        # Override the method to return the username instead of the ID
        return self.username


@login_manager.user_loader
def load_user(username: str) -> Optional[User]:
    user_data = find_data({"username": username})
    if user_data:
        return User(user_data["_id"],
                    user_data["first_name"],
                    user_data["last_name"],
                    user_data["username"],
                    user_data["email"])
    return None


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
@login_required
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
def login_route() -> Union[str, Response]:
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')  # Log identifier

        user_data = find_data(
            {"$or": [{"username": identifier}, {"email": identifier}]})

        if user_data and pbkdf2_sha256.verify(password, user_data["password"]):
            user = User(
                user_data["_id"],
                user_data["first_name"],
                user_data["last_name"],
                user_data["username"],
                user_data["email"])
            print(user_data)
            session.permanent = True  # Note the spelling correction
            login_user(user, remember=True, force=True)
            return redirect(url_for('dashboard'))
        else:
            print("Login failed")  # Log failed login
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user() -> Union[str, Response]:
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
            # Handle registration error
            return render_template(
                'register.html',
                error="Email or username already exists")

        user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
        response = insert_data(user_data)

        if response.get('insertedId'):
            return redirect(url_for('registersuccess'))

        # Handle other errors
        return render_template('register.html', error="Registration failed")

    return render_template('register.html')


@app.route('/registererror')
def registererror() -> str:
    return render_template('registererror.html')
    # Replace with a proper HTML template if necessary


@app.route('/registersuccess')
@login_required
def registersuccess() -> str:
    return render_template('registersuccess.html')
    # Replace with a proper HTML template if necessary


@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return render_template('logout.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
