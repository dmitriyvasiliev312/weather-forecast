from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from weather import Weather
from pprint import pprint

API_KEY = '6b57940003b5d63b09f5c888a26c7819'

app = Flask(__name__)
app.secret_key = '1111'

@app.route('/<latitude>/<longitude>')
def index(latitude, longitude):
    weather = Weather(latitude = latitude, longitude = longitude, API_KEY = API_KEY)
    forecast_list = weather.one_day_forecast()
    current_temp = weather.get_current_weather()['temp']
    icon = weather.get_current_weather()['icon']
    weather_type = weather.get_current_weather()['weather']
    city = weather.get_city_name()
    today = list()
    min_temp = weather.get_min_max_for_4_days()[0]
    max_temp = weather.get_min_max_for_4_days()[1]
    week_days = weather.get_min_max_for_4_days()[2]
    for i in range(8):
        today.append(f"{forecast_list[i]['time']} {forecast_list[i]['icon']}  {forecast_list[i]['temp']}℃")
        
    return render_template('index.html', city = city, temp = current_temp, today = today, icon = icon, weather = weather_type,
    week = [f'{week_days[0]} min: {min_temp[0]}℃ max: {max_temp[0]}℃', f'{week_days[1]} min: {min_temp[1]}℃ max: {max_temp[1]}℃', 
            f'{week_days[2]} min: {min_temp[2]}℃ max: {max_temp[2]}℃', f'{week_days[3]} min: {min_temp[3]}℃ max: {max_temp[3]}℃'])

@app.route('/', methods = ['POST', 'GET'])
def start_page():
    if request.method == 'POST' :
        if request.form.get('city_name'):
            try:
                weather = Weather(API_KEY, city = request.form['city_name'])
                coordinates = weather.coordinates_by_city(request.form['city_name'])
                return redirect(url_for('index', latitude = coordinates['lat'], longitude = coordinates['lon']))
            except:
                if request.form['city_name'] != '':
                    print(f"Город не найден: {request.form['city_name']}")
                    flash('Город не найден.')

    return render_template('start_page.html')

if __name__ == '__main__':
    app.run(debug = True)