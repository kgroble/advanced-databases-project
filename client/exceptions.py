class UserDoesNotExist(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class InvalidUser(Exception):
    pass

class InvalidUsername(Exception):
    pass

class NotLoggedIn(Exception):
    pass

class UnknownError(Exception):
    pass

class WrongNumberArguments(Exception):
    pass

class WrongCredentials(Exception):
    pass

class StopApplication(Exception):
    pass