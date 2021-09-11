import re
from theteller_api_sdk.types.currencyType import ALL_CURRENCY, CURRENCY

from validators.url import url
from theteller_api_sdk.types.r_switchTypes import CARD_RSWITCH
from helpers.helpers import generateTransactionId,generateHeader
from payments import Payments
from core import core
from errors import errors
import requests
from validators import email
from datetime import datetime

class CardPayment(Payments):
    def __init__(self, client: core.Client) -> None:
        if type(client) != core.Client:
            raise errors.InvalidClient
        super().__init__(client)

    def generateRequestBody(self,r_switch,card_holder,
                            card_holder_email,card_pan,
                            expire_month,expire_year,cvv,
                            amount,currency,description,
                            redirect_url,):
        return {
            "processing_code":"000000",
            "r-switch":CARD_RSWITCH.get(r_switch),
            "transaction_id":generateTransactionId(),
            "merchant_id": self.client.API_Key,
            "pan":card_pan,
            "3d_url_response":redirect_url,
            "exp_month":expire_month,
            "exp_year":expire_year,
            "cvv":cvv,
            "desc":description,
            "amount":f"{amount}",
            "currency":CURRENCY.get(currency),
            "card_holder":card_holder,
            "customer_email":card_holder_email
        }
    

    def createCardPayment(self,r_switch,card_holder,
                        card_holder_email,card_pan,
                        expire_month,expire_year,cvv,
                        amount,currency,description,
                        redirect_url):

        current_date= datetime.now()

        if not CARD_RSWITCH.get(r_switch):
            raise errors.InvalidRSwitch

        if len(card_holder)<2:
            raise errors.InvalidCardHolderName

        if (current_date.year > expire_year) or (current_date.year >= expire_year and current_date.month > expire_month ):
            raise errors.InvalidCard

        if (len(cvv) != 3 or len(cvv) != 4) and not re.match(r"^([0-9]+){3,4}$",card_pan):
            raise errors.InvalidCard

        if len(card_pan) != 19 and not re.match(r"^([0-9]+){19}$",card_pan):
            raise errors.InvalidCard

        if len(description) ==0:
            raise errors.DescriptionRequired

        if not url(redirect_url):
            raise errors.InvalidRedirectUrl

        if not email(card_holder_email):
            raise errors.InvalidEmail

        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType

        if  not currency or not currency in ALL_CURRENCY:
            raise errors.InvalidCurrency

        
        baseUrl = self.client.environment.getBaseUrl()
        endpoint="v1.1/transaction/process"
        headers=generateHeader(self)

        body=self.generateRequestBody(
                            r_switch,card_holder,
                            card_holder_email,card_pan,
                            expire_month,expire_year,cvv,
                            amount,currency,description,
                            redirect_url
                            )

        request= requests.post(f"{baseUrl}/{endpoint}",headers=headers,json=body)

        if request.status_code==200:
            data=request.json()

            if url(data.reason):
                {
                    "status": data.get("status"),
                    "is_vbn_required": True,
                    "vbn_redirect_url": data.get("redirect_url")
                }

            return {
                    "transaction_id":data.get("transaction_id"),
                    "status": data.get("status"),
                    "message": data.get("reason"),
                    "is_vbn_required":False
                }

        return {
            "status" : request.status_code,
            "message": f"An Error({request.status_code}), could not handle for payment of funds"
        }


    def cardReversalRequestBody(self,transaction_id,amount):
        return { 
            "merchant_id": self.client.API_Key,
            "transaction_id": transaction_id,
            "amount": f"{amount}"
        }

    def cardReversal(self,transaction_id,amount):

        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType

        if not re.match(r"^([0-9]+){3,4}$",transaction_id):
            raise errors.InvalidTransactionId

        baseUrl=self.client.environment.getBaseUrl()
        endpoint='rest/resources/card/reversal'
        headers=generateHeader(self)

        request_data=self.cardReversalRequestBody(transaction_id,amount)

        request=requests.post(f"{baseUrl}/{endpoint}",headers=headers,json=request_data)

        if request.status_code==200:
            data=request.json()

            return {
                    "transaction_id":data.get("transaction_id"),
                    "status": data.get("status"), 
                    "message": data.get("status")
            }

        
        return {
            "status" : request.status_code,
            "message": f"An Error({request.status_code}), could not handle for reversal of funds"
        }

