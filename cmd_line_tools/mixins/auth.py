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

# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)


#Sqlite3 Authentication

import sqlite3
class SqliteAuthenticationMixin(object):
    """Create database connection to sqlite and check for username password"""
    
    def create_connection(self):
        self.con = sqlite3.connect("UserDataBase.db") #sqlite3 has no connect member??
        self.c = self.connection.cursor()
        return self.c
        
    def create_username_password_table(self):
        self.c = self.create_connection()
        self.c.execute('''CREATE TABLE Users (username text, password text)''')
        self.connection.commit()
        
    def set_username_password(self, username, password):
        self.c = self.create_connection()
        self.c.execute("INSERT INTO Users VALUES(username, password)")
        self.connection.commit()
        
        
    def is_authenticated(self,username, password):
        self.c = self.create_connection()
        password_from_db = self.c.execute("SELECT password FROM Users WHERE username = {}".format(password))
        if password == password_from_db:
            return True
        return False