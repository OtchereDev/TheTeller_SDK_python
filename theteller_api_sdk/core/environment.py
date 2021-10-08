import typing
from theteller_api_sdk.errors import errors

ENV_TYPE=typing.Literal["test","production"]

class Environment():
    def __init__(self,env_type:ENV_TYPE) -> None:
        if env_type not in ["test","production"]:
            raise errors.InvalidEnvironment
        self.type=env_type

    def getBaseUrl(self) -> str:
        if self.type=='test':
            return 'test.theteller.net'
        else:
            return 'prod.theteller.net'
