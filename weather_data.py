import requests
from rich import print
from pydantic import BaseModel



class weather_data(BaseModel):
        number : int
        name : str
        startTime : str
        endTime : str
        isDaytime : bool
        temperature : int
        temperatureUnit : str
        temperatureTrend : str
        probabilityOfPrecipitation : dict
        windSpeed : str
        windDirection : str
        icon : str
        shortForecast : str
        detailedForecast : str

        def to_dict(self):
            return {
                "number": self.number,
                "name": self.name,
                "startTime": self.startTime,
                "endTime": self.endTime,
                "isDaytime": self.isDaytime,
                "temperature": self.temperature,
                "temperatureUnit": self.temperatureUnit,
                "temperatureTrend": self.temperatureTrend,
                "probabilityOfPrecipitation": self.probabilityOfPrecipitation,
                "windSpeed": self.windSpeed,
                "windDirection": self.windDirection,
                "icon": self.icon,
                "shortForecast": self.shortForecast,
                "detailedForecast": self.detailedForecast
            }

    


def get_weather_data():
    url = f'https://api.weather.gov/gridpoints/GYX/76,54/forecast'
    resp = requests.get(url)
    resp.raise_for_status()
    weather_data_list = resp.json()["properties"]["periods"]
    data = [weather_data(**item) for item in weather_data_list]
    return data
    
    

