import re
import requests
from theteller_api_sdk.types.r_switchTypes import MOBILE_RSWITCH
from theteller_api_sdk.helpers.helpers import generateHeader, generateTransactionId
from payments.payments import Payments
from core import core
from errors import errors

class MobileMoneyPayment(Payments):
    def __init__(self, client: core.Client) -> None:
        super().__init__(client)

    def generateRequestBody(self,amount,description,subscriber_number,r_switch):

        return {
            "amount" : f"{amount}",
            "processing_code" : "000200",
            "transaction_id" : generateTransactionId(),
            "desc" : description,
            "merchant_id" : self.client.API_Key,
            "subscriber_number" : subscriber_number ,
            "r-switch" : MOBILE_RSWITCH.get(r_switch)
        }

    def createMobileMoneyPayment(self,amount,description,subscriber_number,r_switch):

        if (r_switch and not MOBILE_RSWITCH.get(r_switch)):
            raise errors.InvalidRSwitch

        if (len(subscriber_number) != 10 or len(subscriber_number) != 12) and not re.match(r"^([0-9]+){10,12}$",subscriber_number):
            raise errors.InvalidSubscriberNumber

        if len(description) ==0:
            raise errors.DescriptionRequired

        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType
        
        baseUrl=self.client.environment.getBaseUrl()
        endpoint="v1.1/transaction/process"
        headers=generateHeader(self)

        body=self.generateRequestBody(amount,description,subscriber_number,r_switch)

        request=requests.post(f"{baseUrl}/{endpoint}",headers=headers,json=body)

        if request.status_code==200:
            data=request.json()

            return {
                    "transaction_id":data.get("transaction_id"),
                    "status": data.get("status"),
                    "message": data.get("reason")
                }

        return {
            "status" : request.status_code,
            "message": f"An Error({request.status_code}), could not handle for payment of funds"
        }
