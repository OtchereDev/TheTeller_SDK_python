from random import choices
from string import digits
import base64

def generateTransactionId() -> str:
        selected_digits= choices(digits,k=12)
        return "".join(selected_digits)


def generateHeader(self):
        auth_token = f'{self.client.apiuser}:{self.client.API_Key}'
        message_bytes = auth_token.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
         
        return {
            "Content-Type":"application/json",
            "Authorization": f"Basic {base64_message}",
            "Cache-Control": "no-cache"
        }