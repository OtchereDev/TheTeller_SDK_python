
import typing
from core import core
from random import choices
from string import digits
from errors import errors
from validators import email,url
import requests
import base64

class Checkout():
    def __init__(self,client:core.Client)->None:
        if(client!=core.Client):
            raise errors.InvalidClient

        self.client=client

    def generateTransactionId() -> str:
        return choices(digits,k=12)


    def generateRequestBody(self,description,amount,redirect_url,customer_email) -> "dict[str, typing.Any]":
        return {
            "merchant_id":self.client.merchant_id,
            "transaction_id":self.generateTransactionId(),
            "desc":description,
            "amount":amount,
            "redirect_url":redirect_url,
            "email":customer_email
        }


    def createCheckout(self,description:str,
                        amount:typing.Union[int,float],
                        redirect_url:str,
                        customer_email:str)->"dict[str,typing.Union[str,int]]":
        
        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType

        if not email.email(customer_email):
            raise errors.InvalidEmail

        if not url.url(redirect_url):
            raise errors.InvalidRedirectUrl

        if type(amount) == int: 
            new_amount = int(amount)  
        else:
             new_amount=float(amount)

        baseUri=self.client.environment.getBaseUrl()

        headers={
            "content-type":"application/json",
            "Authorization": f"Basic {base64.b64encode(f'{self.client.apiuser}:{self.client.API_Key}')}",
            "Cache-Control": "no-cache"
        }

        request_data=self.generateRequestBody(description,new_amount,redirect_url,customer_email)

        request = requests.post(f'{baseUri}/checkout/initiate',json=request_data,headers=headers)

        if (request.status_code==200):
            data=request.json()
            return {
                "status":data.status,
                "token": data.token,
                "checkout_url": data.checkout_url
            }
        
        return  {
            "status" : request.status_code,
            "message": f"An Error({request.status_code}), could not handle for checkout"
        }


    def verifyCheckout(self,transactionId:str)->"dict[str,typing.Union[str,int]]":
        baseUri= self.client.environment.getBaseUrl()
        headers={
            "Content-Type": "application/json",
            "Merchant-Id": self.client.merchant_id,
            "Cache-Control": "no-cache"

        }

        request=requests.post(f"{baseUri}/v1.1/users/transactions/{transactionId}/status",headers==headers)

        if request.status_code==200:
            data=request.json()
            return {
                "status":   data.status,
                "message": data.reason,
                "r_switch": data.r_switch,
                "subscriber_number": data.subscriber_number,
                "amount": data.amount
            }

        else:
            return {
                "status": request.status_code,
                "message":f"An Error({request.status_code} happened)"
            }

