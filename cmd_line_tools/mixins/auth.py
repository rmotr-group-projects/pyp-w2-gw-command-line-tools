from string import *
import re
import pdb

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

    def authenticate(self, username, password):
        for user in self.AUTHORIZED_USERS:
            if user == {'username': username, 'password': password}:
                return user


class CreateNewUserMixin(object):
    
    AUTHORIZED_USERS = []
    
    def create_new_user(self):
        username = str(self.request_input_data("username (your username must be at least 5 characters long)"))
        password = str(self.request_input_data("password (your password must be at least 8 characters long and must contain letters and numbers)"))
        
        while len(username) < 5:
            print("Your username is too short")
            username = str(self.request_input_data("username (your username must be at least 5 characters long)"))
        
        while len(password) < 8 and not re.match("^[a-zA-Z0-9_]*$", password):
            print("Your password is invalid")
            password = str(self.request_input_data("password (your password must be at least 8 characters long and must contain letters and numbers)"))
        
        new_user = {'username': username, 'password': password}
        self.AUTHORIZED_USERS.append(new_user)
        return self.AUTHORIZED_USERS
     

class ResetPasswordMixin(object):
    
    def reset_password(self):
        #pdb.set_trace()
        
        new_password = str(self.request_input_data("new password (your password must be at least 8 characters long and must contain letters and numbers)"))
        
        while len(new_password) < 8 and not re.match("^[a-zA-Z0-9_]*$", new_password):
            print("Your password is invalid")
            new_password = str(self.request_input_data("new password (your password must be at least 8 characters long and must contain letters and numbers)"))
        
        for login in self.AUTHORIZED_USERS:
            if login['username'] == self._authenticated_user['username']:
                login['password'] = new_password
                new_login_details = login
        
        #return new_login_details



# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)
