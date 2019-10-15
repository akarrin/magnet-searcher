class HttpError(Exception):
    def __init__(self, error_code, error_msg):
        super().__init__(self)
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return f'error type:http error; error code:{self.error_code}; error msg:{self.error_msg}'
