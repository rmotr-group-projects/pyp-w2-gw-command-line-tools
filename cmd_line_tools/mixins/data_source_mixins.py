
import requests
import json

class JSONDataRequestMixin(object):
    """
    Handles requests from an online JSON resource
    Returns the JSON data as a dict
    
    Expects self.REQUEST_URL to exist
    """
    #Assumes self.REQUEST_URL exists
    def request_data(self):
        return self._get(self.REQUEST_URL)
    
    def _get(self,url,params=None):
        r = requests.get(url, params=params)
        return r.json()
        
class PagedJSONDataMixin(object):
    """
    Handles requests from an online JSON resource
    Expects to receive data in a paged format such that
        'next' indicates url to next page of results
        'results' contains the results for this page
        
    Expects self.REQUEST_URL to exist.
    """
    def request_data(self):
        return self._get_all(self.REQUEST_URL)
    
    def _get(self,url):
        r = requests.get(url)
        return r.json()
        
    def _get_all(self,url):
        data = []
        # Process first page of results
        r = self._get(url)
        for elem in r['results']:
            data.append(elem)
        # Page through results
        while r['next']:
            r = self._get(r['next'])
            for elem in r['results']:
                data.append(elem)
        return data