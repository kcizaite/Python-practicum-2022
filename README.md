# Python practicumn 2022

<h2>Flask app:</h2>

* route /welcome, responds with the string "welcome"
* route /welcome/home, responds with the string "welcome home"
* route /welcome/back, responds with the string "welcome back"
  _____________________________________________________________

<h4>Weather report</h4>

✅ Get a weather report for a city of your liking via API call

* API doc: https://openweathermap.org/current#name
* API Key: shared via another channel

✅ Create a route /weather which responds with received data

* display city name and current temperature in Celsius
* consider using a template to render and display data

✅ Optional task – let the user pick a city
  _____________________________________________________________

✅ Get geographic coordinates for a city of your liking via an API call

* API doc: https://openweathermap.org/api/geocoding-api

✅ Get historical data from dev.meteostat.net via one of these methods:

* JSON API
* Python library
* Bulk data

✅ Display one year of temperature history - min., max., average

* Use the graphical form of representation – matplotlib module

✅ Create a route /weather_history to display data

* Show city name and chart with temperature data, including legend (names of axis, description of data)
* In addition, separately display values for min., max. temperature, the date it was recorded, and the average temperature for the whole range.
* Provide a download link for an Excel document with temperature data (raw data)
* Provide a download link for a PDF document with a temperature chart (graphical data)

✅ Additional advanced task: Send notification of the temperature

* Create a route /notification
* Possible communication channels:
  * a push notification via SIGNL4 or similar service: https://www.signl4.com/
  * e-mail notification
  * SMS message
* Trigger the notification by:
  * Pushing a button on your webpage
  * Setting up a notification when a trigger temperature is reached
  _____________________________________________________________
 
 ✅ Record each weather search in the log file
 
* Log: Date, Time, City, Temperature

✅ Create a route /log to display data for the last 5 searches

* Think about persistent data. The last 5 searches must be displayed even after flask is restarted

✅ Create a route /cities

* Display the current list of cities of interest and their current temperature (updates on list change)
* Let the user add the city to the list
* Let the user change list entry (change city name)
* Let the user delete the city from the list
* Record add/change/delete events to log file
* Let the user manually refresh the currently listed cities’ temperature data.
* The current list and temperature must persist after the flask is restarted
* Optional advanced task: implement this for multiple users (identified by login)
  _____________________________________________________________

<h4>To use this project, use the instructions provided</h4>

1. Has Python on your operating system
2. Download the <b>"Python-practicum-2022"</b> project
3. Install the required settings: `pip install -r requirements.txt`
4. Run the program: `python index.py`

## Good luck!

