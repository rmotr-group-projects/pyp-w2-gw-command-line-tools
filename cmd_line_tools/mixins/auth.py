import json
import sqlite3
import os

# reads in json file for usernames/passwords
class JsonAuthenticationMixin(object):
    credentials = json.load(open("passwords.json", 'r')) # implement flexible file locations
    def authenticate(self, username, password):
        for user in self.credentials:
            if self.credentials[user] == {'username': username, 'password': password}:
                return self.credentials[user]
                
class Sqlite3AuthenticationMixin(object):
    def authenticate(self, username, password):
        conn = sqlite3.connect("passwords.sqlite")
        conn.text_factory = str
        credentials = conn.cursor()
        credentials.execute('SELECT * FROM auth where user = "{}" and password = "{}"'.format(username, password))
        creds = credentials.fetchall()
        for user in creds:
            if user == (username, password):
                return {"username":user[0], "password":user[1]}
        credentials.close()

# conn = sqlite3.connect("passwords.sqlite")
# conn.text_factory = str
# credentials = conn.cursor()
# credentials.execute('SELECT * FROM auth where user = "user1" and password = "supersecret"')
# creds = credentials.fetchall()
# print(creds)
# credentials.close()


class LoginMixin(object):
    """Basic login mixin.

    This mixin will provide the mechanisms to authenticate a user. But it
    doesn't provide authentication by itself.
    It relies in the `authentication` method from other
    Authentication services (like the one shown below).

    You can plug any authentication service that you like, as long
    as it keeps its interface.
    """
    def login(self):
        username = self.request_input_data('username')
        password = self.request_input_data('password')
        
        # How does authenticate work if it's not defined in this class?
        self._authenticated_user = self.authenticate(username, password)

        return self._authenticated_user

    @property
    def is_authenticated(self):
        return bool(getattr(self, '_authenticated_user', None) or self.login())

    @property
    def user(self):
        return self._authenticated_user


class SimpleAuthenticationMixin(object):
    AUTHORIZED_USERS = []

    def authenticate(self, username, password):
        for user in self.AUTHORIZED_USERS:
            if user == {'username': username, 'password': password}:
                return user

# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)



