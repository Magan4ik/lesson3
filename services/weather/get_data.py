import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

const = {
    "CONNECT_TIMEOUT": 10,
    "READ_TIMEOUT": 25
}

def get_openweather_appid():
    return os.getenv('WEATHER_APPID')