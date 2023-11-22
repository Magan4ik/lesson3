import requests
import datetime

from services.weather import get_data


class WeatherData:
    def __init__(self, lat: float, lon: float, units: str = "metric", lang: str = "en"):
        appid = get_data.get_openweather_appid()
        connect_timeout = get_data.const["CONNECT_TIMEOUT"]
        read_timeout = get_data.const["READ_TIMEOUT"]
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/weather",
                               params={"lat": lat, "lon": lon, "appid": appid, "units": units, "lang": lang},
                               timeout=(connect_timeout, read_timeout))

            self.full_data: dict = res.json()
        except Exception as exp:
            raise ValueError(exp)

        self.name: str = self.full_data["name"]
        self.country: str = self.full_data["sys"]["country"]

        weather = self.full_data["weather"][0]
        self.weather: str = weather["main"]
        self.weather_description: str = weather["description"]

        main = self.full_data["main"]
        self.temp: float = main["temp"]
        self.feel_temp: float = main["feels_like"]
        self.min_temp: float = main["temp_min"]
        self.max_temp: float = main["temp_max"]
        self.sea_pressure: int = main.get("sea_level", -1)
        self.grnd_pressure: int = main.get("grnd_level", -1)
        self.humidity: int = main["humidity"]

        wind = self.full_data["wind"]
        self.wind_speed: float = wind["speed"]
        self.wind_speed_kh: float = self.wind_speed * 3600 / 1000
        deg = wind["deg"]
        east_degs = list(range(338, 361))
        east_degs.extend(list(range(0, 23)))
        convert_deg = {"East": east_degs,
                       "Northeast": list(range(23, 68)),
                       "North": list(range(68, 113)),
                       "Northwest": list(range(113, 158)),
                       "West": list(range(158, 203)),
                       "Southwest": list(range(203, 248)),
                       "South": list(range(248, 293)),
                       "Southeast": list(range(293, 338))}

        for diraction, degs in convert_deg.items():
            if deg in degs:
                self.wind_diraction: str = diraction
                break
        else:
            self.wind_diraction: str = "NaN"

        self.icon_url: str = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"

        self.date_time = datetime.datetime.utcfromtimestamp(self.full_data["dt"])
        self.timezone: int = self.full_data["timezone"] // 3600
        self.time_string: str = f"{self.date_time.hour + self.timezone}:{self.date_time.minute}"

    def get_full_data(self) -> dict:
        return self.full_data


class WeatherInterface:
    def __init__(self, city_name: str, state_code: str = None, country_code: str = None):
        self._appid = get_data.get_openweather_appid()
        if state_code:
            city_name += ',' + state_code
        if country_code:
            city_name += ',' + country_code

        try:
            res = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                               params={'q': city_name, 'appid': self._appid, 'limit': 5})

            self.data = res.json()
        except Exception as exp:
            raise ValueError(exp)

    def get_city_list(self) -> list:
        city_list = []
        for d in self.data:
            city_list.append(f'{0},{1}'.format(d['name'], d['country']))
        return city_list

    def get_weather_byindex(self, index: int = 0, units: str = "metric", lang: str = "en") -> WeatherData:
        if index >= len(self.data):
            raise IndexError(f"No such index exists. Max:{len(self.data)-1}")
        city = self.data[index]  # get first city data in dict
        lat = city["lat"]
        lon = city["lon"]
        return WeatherData(lat, lon, units=units, lang=lang)

    def get_first_weather(self, units: str = "metric", lang: str = "en") -> WeatherData:
        return self.get_weather_byindex(index=0, units=units, lang=lang)
