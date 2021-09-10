"""
This file contains all the type of error that are raised in this SDK
"""

class Error(Exception):
    pass

class InvalidClient(Error):
    pass

class InvalidAmountType(Error):
    pass

class InvalidEmail(Error):
    pass

class InvalidRedirectUrl(Error):
    pass

class InvalidEnvironment(Error):
    pass