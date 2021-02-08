# -*- coding: utf-8 -*-

import os.path
import sys
import configparser 

import click

try:
    from py_weather_cli.openweathermap import *
    from py_weather_cli.ascii_art import *
    from py_weather_cli.weather import *
except ModuleNotFoundError:
    from openweathermap import *
    from ascii_art import *
    from weather import *



ALL_BACKENDS = {
    "open-weather-map": open_weather_map
}

ALL_FRONTENDS = {
    "ascii-art-table": ascii_art
}

CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.weather-cli')

weather_config = WeatcherConfig(
        city_name = 'Toronto', 
        api_key = 'b8b62a4df47b629b0762ce047f0bc75b',
        lang = 'en',
        num_days = 5,
        unit = UNITS_METRIC,
        backends = 'open-weather-map',
        frontends = 'ascii-art-table'
    )

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    map = {key: value for key, value in config.items('GLOBAL')}
    return WeatcherConfig(**map)

def check_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            f.write(f'[GLOBAL]\n')
            f.write(f'city_name=\n')
            f.write(f'api_key=\n')
            f.write(f'lang=en\n')
            f.write(f'num_days=5\n')
            f.write(f'unit=metric\n')
            f.write(f'backends=open-weather-map\n')
            f.write(f'frontends=ascii-art-table\n')

@click.command()
@click.option('--city', '-c', default='', type=str, help = "full city name")
@click.option('--unit', '-u', default='metric', type=click.Choice(['metric', 'imperial', 'si']), help = "measure unit")
def cli(city, unit):
    check_config()
    weather_config = load_config()
    weather_config.city_name = city
    weather_config.unit = unit

    if not weather_config.city_name or len(weather_config.city_name) == 0:
        raise ValueError('please enter the city name')

    data = ALL_BACKENDS[weather_config.backends].fetch(weather_config)
    ALL_FRONTENDS[weather_config.frontends].render(data, weather_config.unit)


if __name__ == '__main__':
    cli()