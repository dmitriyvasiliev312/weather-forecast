import requests
from pprint import pprint
from datetime import datetime, timedelta
import locale
from pytils import dt
API_KEY = '6b57940003b5d63b09f5c888a26c7819'

class Weather:
    def __init__(self, API_KEY : str, latitude : str = None, longitude : str = None,  city : str = None):
        if latitude != None and latitude != None:
            self.latitude = latitude
            self.longitude = longitude
        else:
            coordinates = self.coordinates_by_city(city)
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lon']
        self.API_KEY = API_KEY

    def _get_5_days_json(self, language = 'ru'):
        '''Get 3-hours forecast for 5 days in json.'''
        url = 'http://api.openweathermap.org/data/2.5/forecast/?'
        params = dict(lat = self.latitude, lon = self.longitude, appid = self.API_KEY, units = 'metric', lang = [language])
        w = requests.get(url, params = params)
        return w.json()
    
    def get_weekdays_from_date(self, date_string, days):
        '''Takes a date string in the format 'YYYY-MM-DD HH:MM:SS' and an integer value days. 
           It returns a list containing the names of the weekdays starting from tomorrow and for the specified number of days.'''
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        next_day = date + timedelta(days=1)
        week_days = []

        for i in range(days):
            current_day = next_day + timedelta(days=i)
            weekday = dt.ru_strftime("%A", inflected=True, date=current_day)
            week_days.append(weekday)

        return week_days
    
    def get_icon(self, id):
        '''Get icon by id.'''
        weather_icons = dict()
        weather_icons['01d'] = '☀️'
        weather_icons['02d'] = '🌤'
        weather_icons['03d'] = '☁️'
        weather_icons['04d'] = '☁️'
        weather_icons['09d'] = '🌧'
        weather_icons['10d'] = '🌧'
        weather_icons['11d'] = '🌩'
        weather_icons['13d'] = '❄️'
        weather_icons['13d'] = '💨'
        weather_icons['01n'] = '☀️'
        weather_icons['02n'] = '🌤'
        weather_icons['03n'] = '☁️'
        weather_icons['04n'] = '☁️'
        weather_icons['09n'] = '🌧'
        weather_icons['10n'] = '🌧'
        weather_icons['11n'] = '🌩'
        weather_icons['13n'] = '❄️'
        weather_icons['13n'] = '💨'
        return weather_icons[id]
    
    def get_weather_type(self, id):
        '''Get weather type by id.'''
        weather_types = dict()
        weather_types['01d'] = 'sunny'
        weather_types['02d'] = 'sunny_clouds'
        weather_types['03d'] = 'clouds'
        weather_types['04d'] = 'clouds'
        weather_types['09d'] = 'rain'
        weather_types['10d'] = 'rain'
        weather_types['11d'] = 'storm'
        weather_types['13d'] = 'snow'
        weather_types['13d'] = 'clouds'
        weather_types['01n'] = 'sunny'
        weather_types['02n'] = 'sunny_clouds'
        weather_types['03n'] = 'clouds'
        weather_types['04n'] = 'clouds'
        weather_types['09n'] = 'rain'
        weather_types['10n'] = 'rain'
        weather_types['11n'] = 'storm'
        weather_types['13n'] = 'snow'
        weather_types['13n'] = 'clouds'
        return weather_types[id]


    def get_weather_list(self):
        return self._get_5_days_json()['list']
    
    def time_by_date(self, date):
        '''Get time from json-date.'''
        l = list(date)
        return f'{l[11]}{l[12]}:00'

    def one_day_forecast(self): 
        '''List with forecast for one day.'''
        main_list = dict()
        weather_list = self._get_5_days_json()['list'] 
        i = 0 
        while i != 8:
            main_list[i] = dict()
            main_list[i]['time'] = self.time_by_date(str(weather_list[i]['dt_txt']))
            main_list[i]['temp'] = round(weather_list[i]['main']['temp'])
            main_list[i]['feels_like'] = round(weather_list[i]['main']['feels_like'])
            main_list[i]['icon'] = self.get_icon(weather_list[i]['weather'][0]['icon'])
            main_list[i]['desc'] = weather_list[i]['weather'][0]['description']
            i = i + 1
        return main_list

    def coordinates_by_city(self, city : str):
        url = 'http://api.openweathermap.org/geo/1.0/direct?'
        params = dict(q = city, appid = API_KEY )
        r = requests.get(url = url, params = params)
        coordinates = dict(lat = r.json()[0]['lat'], lon = r.json()[0]['lon'])
        return coordinates

    def get_city_name(self):
        json = self._get_5_days_json()
        return json['city']['name']
    
    def get_current_weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather?'
        params = dict(lat = self.latitude, lon = self.longitude, appid = self.API_KEY, lang = 'ru', units = 'metric')
        r = requests.get(url = url, params = params)
        return dict(temp = round(r.json()['main']['temp']), icon = self.get_icon(r.json()['weather'][0]['icon']), weather = self.get_weather_type(r.json()['weather'][0]['icon']))
    
    def get_min_max_for_4_days(self):
        weather_list = self.get_weather_list()
        min_temperatures = []
        max_temperatures = []

        # Find the index of the first data point for the next day
        next_day_index = 0
        for i in range(len(weather_list)):
            if self.time_by_date(weather_list[i]['dt_txt']) == '00:00':
                next_day_index = i
                break

        # Iterate over the weather data for each day
        for i in range(next_day_index, next_day_index + 4 * 8, 8):
            day_weather = weather_list[i : i + 8]  # Extract weather data for the day (8 data points per day)

            # Get the minimum and maximum temperatures for the day
            temperatures = [data['main']['temp'] for data in day_weather]
            min_temp = round(min(temperatures))
            max_temp = round(max(temperatures))

            min_temperatures.append(min_temp)
            max_temperatures.append(max_temp)

            week_days = self.get_weekdays_from_date(weather_list[0]['dt_txt'], 4)

        return min_temperatures, max_temperatures, week_days
    

w = Weather(API_KEY = API_KEY, city = 'kiev')
print(w.get_min_max_for_4_days()[0]) 
print(w.get_min_max_for_4_days()[1])
print(w.get_min_max_for_4_days()[2])

            

                






    


