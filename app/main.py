from flask import Flask, render_template, request
from app.weather import main as get_weather

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city = request.form.get('cityName')
        state = request.form.get('stateName')
        country = request.form.get('countryName')
        data = get_weather(city, state, country)
    return render_template('index.html', data=data)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(debug=True, host='0.0.0.0', port=port)
