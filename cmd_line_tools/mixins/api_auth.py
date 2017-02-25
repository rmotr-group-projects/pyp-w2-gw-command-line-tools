import requests
import json

class ApiCheckMixin(object):
    def authenticate_key(self, api_key):
        msg = "Invalid API key. Please see http://openweathermap.org/faq#error401 for more info."
        check = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=8011,nz&appid={}'.format(api_key))
        check_json = check.json()
        try:
            if check_json["message"] == msg:
                return False
        except KeyError:
            return check_json
        return True