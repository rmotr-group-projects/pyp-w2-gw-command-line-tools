import sqlite3

# c = sqlite3.connect('logins.db')
# c.cursor()
# # c.execute('''CREATE TABLE users(username text, password text)''')
# c.execute('''INSERT INTO users(username, password) VALUES ('test_user', 'test_password')''')
# c.commit()
# c.close()


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


class SqliteAuthenticationMixin(object):
    
    def authenticate(self, username, password):
        c = sqlite3.connect('logins.db')
        cursor = c.cursor()
        # Current Users in Database: ('test_user', 'test_pass'), ('John Doe', '123456')
        
        try:
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone():
                return {'username': username, 'password': password}
        # except:
        #     raise Exception('Database Connection Failure')
        finally:
            cursor.close()



# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)
