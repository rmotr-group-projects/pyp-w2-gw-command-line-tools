import requests
import json

class WeatherMixin(object):
    def checkweather(self, zipcode, countrycode, api_key):
        url = "http://api.openweathermap.org/data/2.5/weather?zip={},{}&appid={}&units=imperial".format(zipcode, countrycode, api_key)
        
        data = requests.get(url)
        self.json_data = data.json()
        try:    
            self.weather_data = "The temperature is {} degrees with {}".format(self.json_data["main"]["temp"], self.json_data["weather"][0]["description"])
        except KeyError:
            self.weather_data = "INVALID PARAMS!!! :("
        return self.json_data
