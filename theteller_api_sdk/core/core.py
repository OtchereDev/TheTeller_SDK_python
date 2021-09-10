from errors import errors
from core.environment import Environment


class Client():
    """Global client for transaction"""
    def __init__(self, merchant_id:str, api_key:str,apiuser:str,environment:Environment):
        if (environment != Environment):
            raise errors.InvalidEnvironment
        self.merchant_id=merchant_id
        self.API_Key=api_key
        self.apiuser=apiuser
        self.environment=environment
