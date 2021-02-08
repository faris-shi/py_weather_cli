# -*- coding: utf-8 -*-

from datetime import datetime

import requests


try:
    from py_weather_cli.weather import *
    from py_weather_cli.utils import *
except ModuleNotFoundError:
    from weather import *
    from utils import *

_FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric&lang={}'

_CODE_MAP = {
        200: CODE_THUNDERY_SHOWERS,
		201: CODE_THUNDERY_SHOWERS,
		210: CODE_THUNDERY_SHOWERS,
		230: CODE_THUNDERY_SHOWERS,
		231: CODE_THUNDERY_SHOWERS,
		202: CODE_THUNDERY_HEAVY_RAIN,
		211: CODE_THUNDERY_HEAVY_RAIN,
		212: CODE_THUNDERY_HEAVY_RAIN,
		221: CODE_THUNDERY_HEAVY_RAIN,
		232: CODE_THUNDERY_HEAVY_RAIN,
		300: CODE_LIGHT_RAIN,
		301: CODE_LIGHT_RAIN,
		310: CODE_LIGHT_RAIN,
		311: CODE_LIGHT_RAIN,
		313: CODE_LIGHT_RAIN,
		321: CODE_LIGHT_RAIN,
		302: CODE_HEAVY_RAIN,
		312: CODE_HEAVY_RAIN,
		314: CODE_HEAVY_RAIN,
		500: CODE_LIGHT_SHOWERS,
		501: CODE_LIGHT_SHOWERS,
		502: CODE_HEAVY_SHOWERS,
		503: CODE_HEAVY_SHOWERS,
		504: CODE_HEAVY_SHOWERS,
		511: CODE_LIGHT_SLEET,
		520: CODE_LIGHT_SHOWERS,
		521: CODE_LIGHT_SHOWERS,
		522: CODE_HEAVY_SHOWERS,
		531: CODE_HEAVY_SHOWERS,
		600: CODE_LIGHT_SNOW,
		601: CODE_LIGHT_SNOW,
		602: CODE_HEAVY_SNOW,
		611: CODE_LIGHT_SLEET,
		612: CODE_LIGHT_SLEET_SHOWERS,
		615: CODE_LIGHT_SLEET,
		616: CODE_LIGHT_SLEET,
		620: CODE_LIGHT_SNOW_SHOWERS,
		621: CODE_LIGHT_SNOW_SHOWERS,
		622: CODE_THUNDERY_SNOW_SHOWERS,
		701: CODE_FOG,
		711: CODE_FOG,
		721: CODE_FOG,
		741: CODE_FOG,
		731: CODE_UNKNOWN,
		751: CODE_UNKNOWN,
		761: CODE_UNKNOWN,
		762: CODE_UNKNOWN,
		771: CODE_UNKNOWN,
		781: CODE_UNKNOWN,
		800: CODE_SUNNY,
		801: CODE_PARTLY_CLOUDY,
		802: CODE_CLOUDY,
		803: CODE_VERY_CLOUDY,
		804: CODE_VERY_CLOUDY,
		900: CODE_UNKNOWN,
		901: CODE_UNKNOWN,
		902: CODE_UNKNOWN,
		903: CODE_UNKNOWN,
		904: CODE_UNKNOWN,
		905: CODE_UNKNOWN,
		906: CODE_UNKNOWN,
		951: CODE_UNKNOWN,
		952: CODE_UNKNOWN,
		953: CODE_UNKNOWN,
		954: CODE_UNKNOWN,
		955: CODE_UNKNOWN,
		956: CODE_UNKNOWN,
		957: CODE_UNKNOWN,
		958: CODE_UNKNOWN,
		959: CODE_UNKNOWN,
		960: CODE_UNKNOWN,
		961: CODE_UNKNOWN,
		962: CODE_UNKNOWN,
}

class OpenWeatherMap(Backend):

    def _parse_daily(self, daily_list, num_days):
        forecast = []
        day = None
        for daily_data in daily_list:
            if len(forecast) >= int(num_days):
                break
            slot = self._parse_weather_condition(daily_data)
            if day and day.date != slot.date:
                forecast.append(day)
                day = None
            if not day:
                day = Day(date=slot.date, slots=[])
            day.append(slot)
        return forecast

    def _parse_weather_condition(self, detail):
        dt = detail['dt_txt']
        code = detail['weather'][0]['id']
        desc = detail['weather'][0]['description'].title()
        temp = UnitSystem(detail['main']['temp'])
        feels_like = UnitSystem(detail['main']['feels_like'])
        chance_of_rain_percent = detail['rain']['3h'] * 100 if 'rain' in detail else None
        precipitation = UnitSystem(detail['pop'] / 1000 / 1000) if 'pop' in detail else None
        visibility = UnitSystem(detail['visibility'] / 1000)
        wind_speed = UnitSystem(detail['wind']['speed'] * 3.6)
        wind_direction = detail['wind']['deg']
        humidity = UnitSystem(detail['main']['humidity'])
        code = CODE_UNKNOWN if code not in _CODE_MAP else _CODE_MAP.get(code)

        return Cond(
            date = dt[:10],
            time = dt[11:],
            code = code,
            desc = desc,
            temp = temp,
            feels_like = feels_like,
            chance_of_rain_percent = chance_of_rain_percent,
            precipitation = precipitation,
            visibility = visibility,
            wind_speed = wind_speed,
            wind_direction = wind_direction,
            humidity = humidity
        )

    def _parse_astro(self, json_data):
        return Astro(
            moonrise = '',
            moonset = '',
            sunrise = to_local_time(json_data['city']['sunrise']),
            sunset = to_local_time(json_data['city']['sunrise'])
        )

    def _parse_location(self, json_data):
        return Location(
            city = json_data['city']['name'],
            country = json_data['city']['country'],
            latitude = json_data['city']['coord']['lat'],
            longitude = json_data['city']['coord']['lon']
        )

    def fetch(self, weather_config):
        if len(weather_config.api_key) == 0:
            print("No openweathermap.org API key specified.\nYou have to register for one at https://home.openweathermap.org/users/sign_up")
            exit()

        response = get_json_data(_FORECAST_URL.format(
            weather_config.city_name, 
            weather_config.api_key, 
            weather_config.lang
        ))
        forecast = self._parse_daily(response['list'], weather_config.num_days)
        current = forecast[0].slots[0]
        return Data(
            current = current,
            forecast = forecast[1:],
            location = self._parse_location(response),
            astro = self._parse_astro(response)
        )

open_weather_map = OpenWeatherMap()
