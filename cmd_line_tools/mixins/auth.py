import json

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
    '''
    def authenticate(self, username, password):
        for user in self.AUTHORIZED_USERS:
            if user == {'username': username, 'password': password}:
                return user
    '''

class JSONAuthenticationMixin(object):
    
    def authenticate(self, username, password):
        for user in self.get_auth_users():  #return iterable list of dictionaries
            if user == {'username': username, 'password': password}:
                return user
    
    def get_auth_users(self):
        #replace hardcoded dict with readjson(file.json)
        authorized_users = [{'username': 'jsondoe', 'password': 'xxx'}]
        return authorized_users
        
# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)
