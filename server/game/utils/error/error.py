class ErrorResponse:

    def __init__(self, error_type, message):
        self.error_type = error_type
        self.error_msg = message

    # Returns the error message as a Python dict
    def message(self):
        return {
            "error": {
                "type": self.error_type,
                "message": self.error_msg,
            }
        }
