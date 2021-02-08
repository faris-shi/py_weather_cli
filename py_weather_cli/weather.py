# -*- coding: utf-8 -*-
import collections
from dataclasses import dataclass
(
    CODE_UNKNOWN,
    CODE_CLOUDY,
    CODE_FOG,
    CODE_HEAVY_RAIN,
    CODE_HEAVY_SHOWERS,
    CODE_HEAVY_SNOW,
    CODE_HEAVY_SNOW_SHOWERS,
    CODE_LIGHT_RAIN,
    CODE_LIGHT_SHOWERS,
    CODE_LIGHT_SLEET,
    CODE_LIGHT_SLEET_SHOWERS,
    CODE_LIGHT_SNOW,
    CODE_LIGHT_SNOW_SHOWERS,
    CODE_PARTLY_CLOUDY,
    CODE_SUNNY,
    CODE_THUNDERY_HEAVY_RAIN,
    CODE_THUNDERY_SHOWERS,
    CODE_THUNDERY_SNOW_SHOWERS,
    CODE_VERY_CLOUDY
) = range(19)


(
    UNITS_METRIC,
    UNITS_IMPERIAL,
    UNITS_SI
) = ('metric', 'imperial', 'si')

ThresholdColor = collections.namedtuple('ThresholdColor', 'threshold color')


class DataObject(object):
    
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        for att in self.__slots__:
            setattr(self, att, None)
        for k, v in zip(self.__slots__, args):
            setattr(self, k, v)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_json(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}


class Cond(DataObject):
    __slots__ = (
        'date',
        'time',
        'code',
        'desc',
        'temp',
        'feels_like',
        'chance_of_rain_percent',
        'precipitation',
        'visibility',
        'wind_speed',
        'wind_direction',
        'humidity'
    )


class Astro(DataObject):
    __slots__ = ('moonrise', 'moonset', 'sunrise', 'sunset')


class Day(DataObject):
    __slots__ = ('date', 'slots')

    def append(self, slot):
        self.slots.append(slot)


class Location(DataObject):
    __slots__ = ('city', 'country', 'latitude', 'longitude')


class Data(DataObject):
    __slots__ = ('current', 'forecast', 'location', 'astro')

@dataclass
class WeatcherConfig:
    city_name:str
    api_key:str
    lang:str
    num_days:str
    unit:str
    backends:str
    frontends:str

# the default unit is UNITS_METRIC
class UnitSystem(object):
    def __init__(self, value):
        self.value = value
        setattr(self, 'value', value)

    def temp(self, unit=None):
        if not unit or unit == UNITS_METRIC:
            return self.value, '°C'
        elif unit == UNITS_IMPERIAL:
            return self.value*1.8 + 32, '°F'
        elif unit == UNITS_SI:
            return self.value + 273.16, '°K'

    def speed(self, unit=None):
        if not unit or unit == UNITS_METRIC:
            return self.value, 'km/h'
        elif unit == UNITS_IMPERIAL:
            return self.value / 1.609, 'mph'
        elif unit == UNITS_SI:
            return self.value / 3.6, 'm/s'

    def distance(self, unit=None):
        if not unit or unit == UNITS_METRIC or unit == UNITS_SI:
            if self.value < 1:
                return self.value * 1000, 'm'
            return self.value, 'km'
        elif unit == UNITS_IMPERIAL:
            res, unit = self.value / 0.0254, 'in'
            if res < 3*12:
                return res, unit
            elif res < 8*10*22*36:
                return res / 36, 'yd'
            return res / 8 / 10 / 22 / 36, 'mi'


class Backend(object):
    def fetch(self, arg_ns):
        raise NotImplementedError


class Frontend(object):
    def render(self, data, uint):
        raise NotImplementedError