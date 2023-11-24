import requests
import datetime

from services.weather import config


class WeatherData:
    def __init__(self, full_data: dict, city: str, country: str, timezone: int, city_id: int):
        self.full_data = full_data
        
        self.city = city
        self.country = country
        self.id = city_id

        weather = self.full_data["weather"][0]
        self.weather: str = weather["main"]
        self.weather_description: str = weather["description"]

        main = self.full_data["main"]
        self.temp: float = round(main["temp"], 1)
        self.feel_temp: float = round(main["feels_like"], 1)
        self.min_temp: float = round(main["temp_min"], 1)
        self.max_temp: float = round(main["temp_max"], 1)
        self.sea_pressure: int = main.get("sea_level", -1)
        self.grnd_pressure: int = main.get("grnd_level", -1)
        self.humidity: int = main["humidity"]

        wind = self.full_data["wind"]
        self.wind_speed: float = wind["speed"]
        self.wind_speed_kh: float = round(self.wind_speed * 3600 / 1000, 1)
        deg = wind["deg"]
        east_degs = list(range(338, 361))
        east_degs.extend(list(range(0, 23)))
        convert_deg = {"East": east_degs,
                       "Northeast": range(23, 68),
                       "North": range(68, 113),
                       "Northwest": range(113, 158),
                       "West": range(158, 203),
                       "Southwest": range(203, 248),
                       "South": range(248, 293),
                       "Southeast": range(293, 338)}

        for diraction, degs in convert_deg.items():
            if deg in degs:
                self.wind_diraction: str = diraction
                break
        else:
            self.wind_diraction: str = "NaN"

        self.icon_url: str = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"

        self.date_time = datetime.datetime.utcfromtimestamp(self.full_data["dt"])
        self.timezone: int = timezone // 3600
        hour = self.date_time.hour + self.timezone
        if hour >= 24:
            hour -= 24
        minute = self.date_time.minute
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        self.time_string: str = f"{hour}:{minute}"

    def get_full_data(self) -> dict:
        return self.full_data


class WeatherInterface:
    _appid = config.get_openweather_appid()
    connect_timeout = config.const["CONNECT_TIMEOUT"]
    read_timeout = config.const["READ_TIMEOUT"]

    def __init__(self, city_name: str, state_code: str = None, country_code: str = None):
        if state_code:
            city_name += ',' + state_code
        if country_code:
            city_name += ',' + country_code

        try:
            res = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                               params={'q': city_name, 'appid': self._appid, 'limit': 5},
                               timeout=(self.connect_timeout, self.read_timeout))

            self.data = res.json()
        except Exception as exp:
            raise ValueError(exp)

    def get_city_list(self, string: bool = True) -> list:
        if string:
            city_list = []
            for d in self.data:
                city_list.append(f'{0},{1}'.format(d['name'], d['country']))
            return city_list
        else:
            return self.data

    def get_coords_byindex(self, index: int = 0) -> tuple[float, float]:
        if index >= len(self.data):
            raise IndexError(f"No such index exists. Max:{len(self.data)-1}")
        city = self.data[index]  # get index city data in dict
        lat: float = city["lat"]
        lon: float = city["lon"]
        return lat, lon

    def get_weather_byindex(self, index: int = 0, units: str = "metric", lang: str = "en") -> WeatherData:
        lat, lon = self.get_coords_byindex(index)
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/weather",
                               params={"lat": lat, "lon": lon, "appid": self._appid, "units": units, "lang": lang},
                               timeout=(self.connect_timeout, self.read_timeout))

            full_data: dict = res.json()
            city = full_data['name']
            country = full_data['sys']['country']
            timezone = full_data['timezone']
            city_id = full_data['id']
            return WeatherData(full_data, city, country, timezone, city_id)
        except Exception as exp:
            raise ValueError(exp)

    def get_forecast_byindex(self, index: int = 0, cnt: int = 5, units: str = "metric", lang: str = "en") -> list[WeatherData]:
        lat, lon = self.get_coords_byindex(index)
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/forecast",
                               params={"lat": lat, "lon": lon, "appid": self._appid, "cnt": cnt, "units": units, "lang": lang},
                               timeout=(self.connect_timeout, self.read_timeout))

            full_data: dict = res.json()
            city = full_data['city']['name']
            country = full_data['city']['country']
            timezone = full_data['city']['timezone']
            city_id = full_data['city']['id']
            forecast: list = full_data['list']
            forecast_data = list()
            for data in forecast:
                forecast_data.append(WeatherData(data, city, country, timezone, city_id))
            return forecast_data
        except Exception as exp:
            raise ValueError(exp)

    def get_first_weather(self, units: str = "metric", lang: str = "en") -> WeatherData:
        return self.get_weather_byindex(index=0, units=units, lang=lang)

    def get_first_forecast(self, cnt: int = 5, units: str = "metric", lang: str = "en") -> list[WeatherData]:
        return self.get_forecast_byindex(0, cnt=cnt, units=units, lang=lang)

    @classmethod
    def get_weather_byid(cls, city_id: int, units: str = "metric", lang: str = "en") -> WeatherData:
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/weather",
                               params={"id": city_id, "appid": cls._appid, "units": units, "lang": lang},
                               timeout=(cls.connect_timeout, cls.read_timeout))

            full_data: dict = res.json()
            city = full_data['name']
            country = full_data['sys']['country']
            timezone = full_data['timezone']
            return WeatherData(full_data, city, country, timezone, city_id)
        except Exception as exp:
            raise ValueError(exp)

    @classmethod
    def get_forecast_byid(cls, city_id: int, cnt: int = 5, units: str = "metric", lang: str = "en") -> list[WeatherData]:
        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/forecast",
                               params={"id": city_id, "appid": cls._appid, "cnt": cnt, "units": units, "lang": lang},
                               timeout=(cls.connect_timeout, cls.read_timeout))

            full_data: dict = res.json()
            city = full_data['city']['name']
            country = full_data['city']['country']
            timezone = full_data['city']['timezone']
            forecast: list = full_data['list']
            forecast_data = list()
            for data in forecast:
                forecast_data.append(WeatherData(data, city, country, timezone, city_id))
            return forecast_data
        except Exception as exp:
            raise ValueError(exp)