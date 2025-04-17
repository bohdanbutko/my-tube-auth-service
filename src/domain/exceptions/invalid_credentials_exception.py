class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid credentials"
