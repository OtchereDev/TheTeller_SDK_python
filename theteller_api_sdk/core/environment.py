import typing
from errors import errors

ENV_TYPE=typing.Literal["test","production"]

class Environment():
    def __init__(self,env_type:ENV_TYPE) -> None:
        if env_type not in ["test","production"]:
            raise errors.InvalidEnvironment
        self.type=env_type

    def getBaseUrl(self) -> str:
        if self.type=='test':
            return 'https://test.theteller.net'
        else:
            return 'https://prod.theteller.net'
