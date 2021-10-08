
import typing
from theteller_api_sdk.core import core
from theteller_api_sdk.helpers.helpers import generateHeader, generateTransactionId
from theteller_api_sdk.errors import errors
from validators import email,url
import requests
import json
import http.client


class Checkout():
    def __init__(self,client:core.Client)->None:
        if(type(client)!=core.Client):
            raise errors.InvalidClient

        self.client=client

    def generateRequestBody(self,description,amount,redirect_url,customer_email) -> "dict[str, typing.Any]":
        init_amount = str(round(amount,2)*100)
        formatted_amount = init_amount.zfill(12)
        
        return {
            "merchant_id":self.client.merchant_id,
            "transaction_id":generateTransactionId(),
            "desc":description,
            "amount":formatted_amount,
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
        endpoint="/checkout/initiate"

        headers= generateHeader(self)

        request_data=self.generateRequestBody(description,amount,redirect_url,customer_email)

        conn = http.client.HTTPSConnection(baseUri)

        payload=json.dumps(request_data)
        conn.request("POST", endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read().decode()
        data=json.loads(data)

        if (data.get("code")==200):

            return {
                "status":data.get("status"),
                "token": data.get("token"),
                "checkout_url": data.get("checkout_url")
            }
        
        return  {
            "status" : 400,
            "message": data
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

