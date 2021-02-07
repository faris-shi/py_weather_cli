# -*- coding: utf-8 -*-

import re
import collections


try:
    from weather_cli.weather import *
except ModuleNotFoundError:
    from weather import *

ThresholdColor = collections.namedtuple('ThresholdColor', 'threshold color')

CODE_TO_ICON = {
        CODE_UNKNOWN: [
            "    .-.      ",
            "     __)     ",
            "    (        ",
            "     `-᾿     ",
            "      •      ",
        ],
        CODE_CLOUDY: [
            "             ",
            "\033[38;5;250m     .--.    \033[0m",
            "\033[38;5;250m  .-(    ).  \033[0m",
            "\033[38;5;250m (___.__)__) \033[0m",
            "             ",
        ],
        CODE_FOG: [
            "             ",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "\033[38;5;251m  _ - _ - _  \033[0m",
            "\033[38;5;251m _ - _ - _ - \033[0m",
            "             ",
        ],
        CODE_HEAVY_RAIN: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
        ],
        CODE_HEAVY_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
            "\033[38;5;21;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
        ],
        CODE_HEAVY_SNOW: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
            "\033[38;5;255;1m  * * * *    \033[0m",
        ],
        CODE_HEAVY_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
            "\033[38;5;255;1m    * * * *  \033[0m",
            "\033[38;5;255;1m   * * * *   \033[0m",
        ],
        CODE_LIGHT_RAIN: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
            "\033[38;5;111m   ʻ ʻ ʻ ʻ   \033[0m",
        ],
        CODE_LIGHT_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ ʻ ʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        CODE_LIGHT_SLEET: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;111m    ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m*  \033[0m",
            "\033[38;5;255m   *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ   \033[0m",
        ],
        CODE_LIGHT_SLEET_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;111m     ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m* \033[0m",
            "\033[38;5;255m    *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ  \033[0m",
        ],
        CODE_LIGHT_SNOW: [
            "\033[38;5;250m     .-.     \033[0m",
            "\033[38;5;250m    (   ).   \033[0m",
            "\033[38;5;250m   (___(__)  \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
            "\033[38;5;255m   *  *  *   \033[0m",
        ],
        CODE_LIGHT_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *  *  * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        CODE_PARTLY_CLOUDY: [
            "\033[38;5;226m   \\  /\033[0m      ",
            "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "             ",
        ],
        CODE_SUNNY: [
            "\033[38;5;226m    \\   /    \033[0m",
            "\033[38;5;226m     .-.     \033[0m",
            "\033[38;5;226m  ‒ (   ) ‒  \033[0m",
            "\033[38;5;226m     `-᾿     \033[0m",
            "\033[38;5;226m    /   \\    \033[0m",
        ],
        CODE_THUNDERY_HEAVY_RAIN: [
            "\033[38;5;240;1m     .-.     \033[0m",
            "\033[38;5;240;1m    (   ).   \033[0m",
            "\033[38;5;240;1m   (___(__)  \033[0m",
            "\033[38;5;21;1m  ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚\033[38;5;228;5m⚡\033[38;5;21;25m‚ʻ   \033[0m",
            "\033[38;5;21;1m  ‚ʻ‚ʻ\033[38;5;228;5m⚡\033[38;5;21;25mʻ‚ʻ   \033[0m",
        ],
        CODE_THUNDERY_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;228;5m    ⚡\033[38;5;111;25mʻ ʻ\033[38;5;228;5m⚡\033[38;5;111;25mʻ ʻ \033[0m",
            "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        ],
        CODE_THUNDERY_SNOW_SHOWERS: [
            "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
            "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
            "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
            "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
            "\033[38;5;255m    *  *  *  \033[0m",
        ],
        CODE_VERY_CLOUDY: [
            "             ",
            "\033[38;5;240;1m     .--.    \033[0m",
            "\033[38;5;240;1m  .-(    ).  \033[0m",
            "\033[38;5;240;1m (___.__)__) \033[0m",
            "             ",
        ],
    }

class AsciiArt(Frontend):

    def __init__(self):
        self.unit = None

    def aatpad(self, s, must_len=15):
        real_s = re.sub(r"\033.*?m", "", s)
        real_len = len(real_s)
        extra_len = len(re.findall(u'[\u4e00-\u9fa5]', real_s))
        need_len = must_len - real_len - extra_len
        s += need_len * ' '
        return s

    def format_temp(self, feels_like, current_temp):
        def color(temp):
            # check value as METRIC unit, specify different color according to the temperature.
            temp_value, _ = temp.temp(UNITS_METRIC)
            col = 196
            colmap = [
                ThresholdColor(-15, 21),
                ThresholdColor(-12, 27),
                ThresholdColor(-9, 33),
                ThresholdColor(-6, 39),
                ThresholdColor(-3, 45),
                ThresholdColor(0, 51),
                ThresholdColor(2, 50),
                ThresholdColor(4, 49),
                ThresholdColor(6, 48),
                ThresholdColor(8, 47),
                ThresholdColor(10, 46),
                ThresholdColor(13, 82),
                ThresholdColor(16, 118),
                ThresholdColor(19, 154),
                ThresholdColor(22, 190),
                ThresholdColor(25, 226),
                ThresholdColor(28, 220),
                ThresholdColor(31, 214),
                ThresholdColor(34, 208),
                ThresholdColor(37, 202),
            ]
            for candidate in colmap:
                if temp_value < candidate.threshold:
                    col = candidate.color
                    break
            return "\033[38;5;%03dm%d\033[0m" % (col, temp.temp(self.unit)[0])
        _, unit = current_temp.temp(self.unit)[1]

        if feels_like:
            if feels_like.temp() < current_temp.temp():
                return self.aatpad("%s - %s %s" % (color(feels_like), color(current_temp), unit))
            elif feels_like.temp() > current_temp.temp():
                return self.aatpad("%s - %s %s" % (color(current_temp), color(feels_like), unit))
        return self.aatpad("%s %s" % (color(current_temp), unit))

    def format_wind(self, wind_speed, wind_degree):
        def wind_dir(degree):
            if not degree:
                return '?'
            arrows = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]
            index = int((degree + 22) % 360 / 45)
            return "\033[1m" + arrows[index] + "\033[0m"
        
        def color(wind_speed):
            speed, _ = wind_speed.speed(UNITS_METRIC)
            col = 196
            colmap = [
                ThresholdColor(0, 46),
                ThresholdColor(4, 82),
                ThresholdColor(7, 118),
                ThresholdColor(10, 154),
                ThresholdColor(13, 190),
                ThresholdColor(16, 226),
                ThresholdColor(20, 220),
                ThresholdColor(24, 214),
                ThresholdColor(28, 208),
                ThresholdColor(32, 202),
            ]
            for candidate in colmap:
                if speed < candidate.threshold:
                    col = candidate.color
                    break
            return "\033[38;5;%03dm%d\033[0m" % (col, wind_speed.speed(self.unit)[0])
        
        _, u = wind_speed.speed(self.unit)
        return self.aatpad("%s %s %s" % (wind_dir(wind_degree), color(wind_speed), u))


    def format_visibility(self, visibility):
        if not visibility:
            return self.aatpad("")
        v, u = visibility.distance(self.unit)
        return self.aatpad("%d %s" % (v, u))

    def format_rain(self, precipitation, chance_of_rain_percent):
        if not precipitation:
            v, u = precipitation.distance(self.unit)
            if  not chance_of_rain_percent:
                return self.aatpad("%.1f %s | %d%%" % (v, u, chance_of_rain_percent))
            return self.aatpad("%.1f %s" % (v, u))
        elif chance_of_rain_percent:
            return self.aatpad("%d%%" % chance_of_rain_percent)
        return self.aatpad("")

    def format_cond(self, cur, cond, is_current=False):
        pass
        icon = CODE_TO_ICON[cond.code]
        border = ' ' if is_current else '|'
        cur[0] = '%s%-s%-s%s' % (cur[0], icon[0], self.aatpad(cond.desc), border)
        cur[1] = '%s%-s%s%s' % (cur[1], icon[1], self.format_temp(cond.feels_like, cond.temp), border)
        cur[2] = '%s%-s%s%s' % (cur[2], icon[2], self.format_wind(cond.wind_speed, cond.wind_direction), border)
        cur[3] = '%s%-s%s%s' % (cur[3], icon[3], self.format_visibility(cond.visibility), border)
        cur[4] = '%s%-s%s%s' % (cur[4], icon[4], self.format_rain(cond.precipitation, cond.chance_of_rain_percent), border)

    def print_day(self, day):
        desired_times_of_day = [9, 12, 15, 18]
        cols = [cand for cand in day.slots if int(cand.time[:cand.time.find(':')]) in desired_times_of_day]

        ret = ['|', '|', '|', '|', '|']
        date_fmt = "┤ %11s ├" % day.date
        s = (
            "                                                   ┌─────────────┐ ",
            "┌────────────────────────────┬─────────────────────" + date_fmt + "─────────────────────┬────────────────────────────┐",
            "│           Morning          │            Noon     └──────┬──────┘    Evening          │            Night           │",
            "├────────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤",
        )
        for line in s:
            print(line)
        for cond in cols:
            self.format_cond(ret, cond)
        for line in ret:
            print(line)
        print("└────────────────────────────┴────────────────────────────┴────────────────────────────┴────────────────────────────┘")

    def render(self, data, unit):
        self.unit = unit
        ret = ['', '', '', '', '']
        self.format_cond(ret, data.current, is_current=True)
        location = data.location
        print(f'Weather in {location.city} / {location.country} ({location.latitude}, {location.longitude})')
        for line in ret:
            print(line)
        for day in data.forecast:
            self.print_day(day)



ascii_art = AsciiArt()