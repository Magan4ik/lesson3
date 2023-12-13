import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = base_dir.replace("services", "")
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

settings = {
    "CONNECT_TIMEOUT": 25,
    "READ_TIMEOUT": 25
}

def get_openweather_appid():
    return os.getenv('WEATHER_APPID')

def get_geonames_username():
    return os.getenv('GEONAMES_USERNAME')

def get_google_maps_key():
    return os.getenv('GOOGLE_MAPS_KEY')
