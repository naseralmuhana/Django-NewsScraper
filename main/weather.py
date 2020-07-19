import requests
from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2
# Create your views here.


def get_weather():

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9499293d662f054a40ec056d21f2bbcc"

    # when goes online
    # ip = get_geo_address(request)
    # city = get_geo(ip)

    city = 'Amman'
    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': r['name'],
        'country': r['sys']['country'],
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {
        'city_weather': city_weather,
    }

    return context


def get_geo(ip):
    g = GeoIP2()
    city = g.city(ip)
    return city


def get_geo_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
