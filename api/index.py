from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# UPDATE home page
@app.route('/')
def home():
    return render_template('index.html')


# UPDATE /weather
@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = ''
    error = 0
    city_name = ''
    # Selected city - Vilnius
    weather_api_key = '60aa068482d6ddc251ae5f53570ac5fb'
    url = "https://api.openweathermap.org/data/2.5/weather?q=Vilnius&appid=" + weather_api_key + "&units=metric"
    current_data = requests.get(url).json()
    # Choice of cities
    if request.method == "POST":
        city_name = request.form.get("city_name")
        if city_name:
            weather_api_key = '60aa068482d6ddc251ae5f53570ac5fb'
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name \
                  + "&units=metric&appid=" + weather_api_key
            weather_data = requests.get(url).json()
        else:
            error = 1
    return render_template('weather.html', new_data=current_data, data=weather_data, city_name=city_name, error=error)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/welcome/home')
def welcome_home():
    return render_template('welcomeHome.html')


@app.route('/welcome/back')
def welcome_back():
    return render_template('welcomeBack.html')


if __name__ == '__main__':
    app.run()
