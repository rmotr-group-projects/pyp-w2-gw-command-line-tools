
import requests
from requests.exceptions import HTTPError
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
        if r.status_code != 200:
            raise HTTPError('Unable to retrieve data. (HTTP status code: {}'.format(r.status_code))
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
        if r.status_code != 200:
            raise HTTPError('Unable to retrieve data. (HTTP status code: {}'.format(r.status_code))
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
        
class GoogleFeelingLuckyMixin(object):
    GOOGLE_URL="http://www.google.com/search?q='{}'&btnI"
    
    def request_data(self, search_term):
        url = self.GOOGLE_URL.format(search_term)
        return requests.get(url).url