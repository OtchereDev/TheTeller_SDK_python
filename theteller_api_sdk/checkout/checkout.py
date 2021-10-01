
import typing
from theteller_api_sdk.core import core
from theteller_api_sdk.helpers.helpers import generateHeader, generateTransactionId
from theteller_api_sdk.errors import errors
from validators import email,url
import requests


class Checkout():
    def __init__(self,client:core.Client)->None:
        if(type(client)!=core.Client):
            raise errors.InvalidClient

        self.client=client

    def generateRequestBody(self,description,amount,redirect_url,customer_email) -> "dict[str, typing.Any]":
        return {
            "merchant_id":self.client.merchant_id,
            "transaction_id":generateTransactionId(),
            "desc":description,
            "amount":f"{amount}",
            "redirect_url":redirect_url,
            "email":customer_email
        }


    def createCheckout(self,description:str,
                        amount:typing.Union[int,float],
                        redirect_url:str,
                        customer_email:str)->"dict[str,typing.Union[str,int]]":
        
        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType

        if not email(customer_email):
            raise errors.InvalidEmail

        if not url(redirect_url):
            raise errors.InvalidRedirectUrl

        if len(description)==0:
            raise errors.DescriptionRequired

        baseUri=self.client.environment.getBaseUrl()
        endpoint="checkout/initiate"

        headers= generateHeader(self)

        request_data=self.generateRequestBody(description,amount,redirect_url,customer_email)

        print("ee: ",request_data, headers,baseUri,endpoint)

        request = requests.post(f'{baseUri}/{endpoint}',data=request_data,headers=headers)

        if (request.status_code==200):
            data=request.json()
            return {
                "status":data.get("status"),
                "token": data.get("token"),
                "checkout_url": data.get("checkout_url")
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
                "status":   data.get("status"),
                "message": data.get("reason"),
                "r_switch": data.get("r_switch"),
                "subscriber_number": data.get("subscriber_number"),
                "amount": data.get("amount")
            }

        else:
            return {
                "status": request.status_code,
                "message":f"An Error({request.status_code} happened)"
            }

