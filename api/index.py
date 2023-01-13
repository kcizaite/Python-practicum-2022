from flask import Flask, render_template, request, send_file, current_app, redirect
from local_settings import SECRET_KEY
import requests
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import base64
import io
import datetime
import logging
import os
from flask_sqlalchemy import SQLAlchemy

# SQL
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "citiesdatabase.db"))
app = Flask(__name__)
# SQL
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
# Record each weather search in the log file
logging.basicConfig(filename="static/data/log.txt", encoding='utf-8', level=logging.WARN,
                    format=f'%(asctime)s: %(message)s')
logging.disable(logging.INFO)


# SQL
class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(80), nullable=False)
    temp = db.Column(db.Integer())

    # def __init__(self, city_name, temp):
    #     self.city_name = city_name
    #     self.temp = temp

    def __repr__(self):
        # return f'{self.city_name}: {self.temp} °C'
        return f'{self.city_name}: {self.temp}'


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')


# UPDATE WEEK 4
@app.route('/cities', methods=['GET', 'POST'])
def cities():
    new = ''
    if request.form:
        city_name = Cities(city_name=request.form.get("city_name"))
        logging.warning(city_name)
        # temp = Cities(temp=request.form.get("temp"))
        if city_name:
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name.city_name \
                  + "&units=metric&appid=" + SECRET_KEY
            weather_data = requests.get(url).json()
            new = weather_data['main']['temp']
            print(new)
            temp = Cities(temp=new)
            # temp = weather_data['main']['temp']
            db.session.add(city_name, temp)
            db.session.commit()
    cities = Cities.query.all()
    print(cities, " city")
    return render_template("cities.html", cities=cities)


# UPDATE
@app.route("/update", methods=["POST"])
def update():
    new_name = request.form.get("new_name")
    old_name = request.form.get("old_name")
    city_name = Cities.query.filter_by(city_name=old_name).first()
    city_name.city_name = new_name
    db.session.commit()
    return redirect("/cities")


# DELETE
@app.route("/delete", methods=["POST"])
def delete():
    city_name = request.form.get("city_name")
    city_name = Cities.query.filter_by(city_name=city_name).first()
    db.session.delete(city_name)
    db.session.commit()
    return redirect("/cities")


@app.route('/log')
def log():
    with open('static/data/log.txt') as file:
        head = []
        lines = file.readlines()
        for i in (lines[:-6:-1]):
            head.append(i)
    return render_template('log.html', head=head)


# UPDATE WEEK 3
@app.route('/weather_history', methods=["GET", "POST"])
def weather_history():
    date_start = ''
    date_end = ''
    geo_data_lon = ''
    geo_data_lat = ''
    error = 0
    city_name = ''
    country = ''
    geo_data = ''
    plot_url = ''
    average_temp = 0
    # Get geographic coordinates for a city of your liking via an API call
    url = "http://api.openweathermap.org/geo/1.0/direct?q=Vilnius&limit=5&appid=" + SECRET_KEY
    current_location = requests.get(url).json()
    coord_lat = current_location[0]['lat']
    coord_lon = current_location[0]['lon']
    if request.method == "POST":
        city_name = request.form.get("city_name")
        date_start = request.form.get("date_start")
        date_end = request.form.get("date_end")
        start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
        # LOGGING
        logging.warning(city_name + " " + date_start + " " + date_end)
        # Get geographic coordinates for any city via an API call
        if city_name:
            url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_name \
                  + "&limit=1&appid=" + SECRET_KEY
            geo_data = requests.get(url).json()
            country = geo_data[0]['country']
            geo_data_lat = geo_data[0]['lat']
            geo_data_lon = geo_data[0]['lon']
            city_location = Point(geo_data_lat, geo_data_lon)
            # Display one year of temperature history - min., max., average
            data = Daily(city_location, start, end)
            data = data.fetch()
            data.to_excel('static/data/weather_data.xlsx', sheet_name='sheet')
            data.plot(y=['tavg', 'tmin', 'tmax'])
            tavg = data['tavg']
            sum = 0
            count = 0
            for i in tavg:
                sum += i
                count += 1
            average_temp = sum / count
            average_temp += average_temp
            logging.info(average_temp)
            plt.xlabel("Time interval")
            plt.ylabel("Temperature °C")
            plt.legend(['Average temperature', 'Minimum temperature', 'Maximum temperature'])
            plt.savefig('static/data/weather_data.pdf', dpi=50)
            img = io.BytesIO()
            plt.savefig(img, format="png")
            plt.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode("utf8")
        else:
            error = 1
    return render_template('weatherHistory.html',
                           coord_lat=coord_lat, coord_lon=coord_lon, geo_data_lat=geo_data_lat,
                           geo_data_lon=geo_data_lon, city_name=city_name, country=country, error=error,
                           geo_data=geo_data, plot_url=plot_url, average_temp=average_temp, date_start=date_start,
                           date_end=date_end
                           )


# Provide a download link for an Excel document with temperature data (raw data)
@app.route('/download_excel')
def download_excel():
    path = 'static/data/weather_data.xlsx'
    return send_file(path, as_attachment=True)


# Provide a download link for a PDF document with a temperature chart (graphical data)
@app.route('/download_pdf')
def download_pdf():
    path = 'static/data/weather_data.pdf'
    return send_file(path, as_attachment=True)


@app.errorhandler(500)
def handle_bad_request(e):
    return render_template('weatherHistory.html')


# UPDATE 2 WEEK
@app.route('/weather', methods=["GET", "POST"])
def weather():
    weather_data = ''
    city_name = ''
    error = 0
    #  Get a weather report for a city of your liking via API call
    url = "https://api.openweathermap.org/data/2.5/weather?q=Vilnius&appid=" + SECRET_KEY + "&units=metric"
    current_data = requests.get(url).json()
    # Get a weather report for any city via API call
    if request.method == "POST":
        city_name = request.form.get("city_name")
        if city_name:
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name \
                  + "&units=metric&appid=" + SECRET_KEY
            weather_data = requests.get(url).json()
            logging.warning(city_name + " " + str(weather_data['main']['temp']) + " C")
        else:
            error = 1
    return render_template('weather.html', new_data=current_data, data=weather_data, city_name=city_name, error=error)


# UPDATE 1 WEEK
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
