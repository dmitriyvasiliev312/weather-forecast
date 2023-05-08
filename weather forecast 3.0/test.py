from weather import Weather
from pprint import pprint
API_KEY = '6b57940003b5d63b09f5c888a26c7819'

w = Weather(API_KEY, city = 'kyiv')
w.week_forecast()