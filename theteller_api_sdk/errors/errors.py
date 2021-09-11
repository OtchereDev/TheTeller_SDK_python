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

class DescriptionRequired(Error):
    pass

class InvalidTransactionType(Error):
    pass

class AccountIssuerRequired(Error):
    pass

class AccountBankRequired(Error):
    pass

class InvalidPassCode(Error):
    pass

class ReferenceIdRequired(Error):
    pass

class InvalidRSwitch(Error):
    pass

class InvalidCardHolderName(Error):
    pass

class InvalidCard(Error):
    pass

class InvalidCurrency(Error):
    pass

class InvalidTransactionId(Error):
    pass

class InvalidSubscriberNumber(Error):
    pass