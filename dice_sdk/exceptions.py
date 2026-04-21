class DiceSendError(Exception):
    def __init__(self, message, details=None):
        self.message = message
        self.details = details
        super().__init__(message)   

class DiceAuthError(DiceSendError):
    pass

class DiceTokenExpiredError(DiceSendError):
    pass

class DiceNewIPError(DiceSendError):
    pass

class DiceTemplateError(DiceSendError):
    pass

class DiceValidationError(DiceSendError):
    pass

class DiceConnectionError(DiceSendError):
    pass