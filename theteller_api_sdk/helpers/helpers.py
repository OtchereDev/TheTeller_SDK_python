from random import choices
from string import digits
import base64

def generateTransactionId() -> str:
        selected_digits= choices(digits,k=12)
        return "".join(selected_digits)


def generateHeader(self):
        auth_token = f'{self.client.apiuser}:{self.client.API_Key}'
        auth_token_byte = auth_token.encode("ascii") 
        return {
            "content-type":"application/json",
            "Authorization": f"Basic {base64.b64encode(auth_token_byte).decode()}",
            "Cache-Control": "no-cache"
        }