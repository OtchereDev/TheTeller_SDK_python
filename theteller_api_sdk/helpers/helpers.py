from random import choices
from string import digits
import base64

def generateTransactionId() -> str:
        return choices(digits,k=12)


def generateHeader(self):
        return {
            "content-type":"application/json",
            "Authorization": f"Basic {base64.b64encode(f'{self.client.apiuser}:{self.client.API_Key}')}",
            "Cache-Control": "no-cache"
        }