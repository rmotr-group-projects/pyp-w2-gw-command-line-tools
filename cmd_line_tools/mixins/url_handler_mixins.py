from .output import StdoutOutputMixin
import re
from bs4 import BeautifulSoup
import requests
import webbrowser


class URLValidationMixin(object):
    """
    Validates URLs
    Will fail if missing protocol(ie. http://)
    """

    def validate(self, url):
        regex = re.compile(
            r'^https?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)


class PrintURLToStdoutMixin(URLValidationMixin,
                            StdoutOutputMixin):
    """
    Validates URL and then prints to stdout
    """

    def open(self, url):
        if self.validate(url):
            self.write(url)


class PrintURLPageTitleToStdoutMixin(URLValidationMixin,
                                     StdoutOutputMixin):
    """
    Validates URL and then prints title and url to stdout
    """

    def open(self, url):
        if self.validate(url):
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            self.write(soup.head.title.text)
            self.write(url)


class OpenURLInBrowser(URLValidationMixin):
    """
    Validates URL and then opens in web browser
    """

    def open(self, url):
        if self.validate(url):
            webbrowser.open(url)
