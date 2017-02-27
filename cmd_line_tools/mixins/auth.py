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
                
                
class CheckResetRequiredMixin(object):
    """Updates LoginMixin to check if password reset required.
    
    Instead of returning True or False, now the string 'auth' (previously
    True), 'unauth' (previously False), or 'auth_pw_reset' is returned. In 
    order for 'auth_pw_reset' to be returned, a second user entry for that user 
    in the AUTHORIZED_USERS list is required with an '*' added to the username 
    i.e. AUTHORIZED_USERS =[{
    'username': username, 'password': password
    }, {
    'username': username*, 'password': password
    }]
    Note: The SimpleAuthenticationMixin is also used in this Mixin
    """
    
    @property
    def is_authenticated(self):
        login = self.login()
        if not login:
            return 'unauth'
        loginr = login['username'] + '*'
        if self.authenticate(loginr, login['password']):
            return 'auth_pw_reset'
        elif login:
            return 'auth'



# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)
