
import requests
import json

class JSONDataRequestMixin(object):
    #Assumes self.REQUEST_URL exists
    def request_data(self):
        return self._get(self.REQUEST_URL)
    
    def _get(self,url,params=None):
        r = requests.get(url, params=params)
        return r.json()
        
class PagedJSONDataMixin(object):
    #Assumes self.REQUEST_URL exists
    def request_data(self):
        return self._get_all(self.REQUEST_URL)
    
    def _get(self,url):
        r = requests.get(url)
        return r.json()
        
    #assumes next in first layer of data
    #assumes results using results key
    def _get_all(self,url):
        data = []
        r = self._get(url)
        for elem in r['results']:
            data.append(elem)
        while r['next']:
            r = self._get(r['next'])
            for elem in r['results']:
                data.append(elem)
        return data