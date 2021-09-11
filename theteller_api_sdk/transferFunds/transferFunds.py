
from theteller_api_sdk.types.r_switchTypes import GENERAL_RSwitch
from theteller_api_sdk.types.accountTypes import ACCOUNT_BANKS, ACCOUNT_ISSUERS, ALL_BANKS, ALL_NETWORKS
import typing

import requests
from core import core
from errors import errors
from helpers.helpers import generateHeader, generateTransactionId


class TransferFunds():
    def __init__(self,client: core.Client,) -> None:
        if type(client) != core.Client:
            raise errors.InvalidClient
        self.client=client


    def generateMobileBody(
                    self,
                    pass_code:str,
                    account_issuer:str,
                    account_number:str,
                    description:str,
                    amount:typing.Union[int,float],
                    r_switch:str="FLT",

                    ):

        return {

            "account_number": account_number,
            "account_issuer":account_issuer,
            "merchant_id": self.client.API_Key,
            "transaction_id":generateTransactionId(),
            "processing_code":"404000",
            "amount": f"{amount}",
            "r-switch":r_switch,
            "desc":description,
            "pass_code":pass_code
        }


    def generateBankBody(self,
                    pass_code:str,
                    account_bank:str,
                    account_number:str,
                    description:str,
                    amount:typing.Union[int,float],
                    r_switch:str="FLOAT",):
        return {

            "account_number":account_number,
            "account_bank":account_bank,
            "account_issuer":"GIP",
            "merchant_id":self.client.merchant_id,
            "transaction_id":generateTransactionId(),
            "processing_code":"404020",
            "amount":f"{amount}",
            "r-switch":GENERAL_RSwitch.get(r_switch),
            "desc":description,
            "pass_code":pass_code
        }

    
    def createTransfer(self,
                        transaction_type:typing.Literal["BANK","MOBILE MONEY"],
                        pass_code,
                        description,
                        amount,
                        account_number:typing.Union[int,float],
                        r_switch:typing.Optional[str]="FLOAT",
                        account_bank:typing.Optional[str]=None,
                        account_issuer:typing.Optional[str]=None,
            
                        
                    ):

        baseUri=self.client.environment.getBaseUrl()

        endpoint = "v1.1/transaction/process" 

        headers = generateHeader(self)

        if transaction_type not in ["BANK","MOBILE TRANSFER"]:
            raise errors.InvalidTransactionType

        if len(description) ==0:
            raise errors.DescriptionRequired

        if len(pass_code) ==0:
            raise errors.InvalidPassCode

        if type(amount) not in [int,float]:
            raise errors.InvalidAmountType

        if not GENERAL_RSwitch.get(r_switch):
            raise errors.InvalidRSwitch

        if type=="BANK":
            if len(account_bank)==0 and account_bank not in ALL_BANKS:
                raise errors.AccountBankRequired
            
            request_data=self.generateBankBody(pass_code,
                                                ACCOUNT_BANKS.get(account_bank),
                                                account_number,
                                                description,
                                                amount,
                                                r_switch,)

        if type=="MOBILE TRANSFER":
            if len(account_issuer)==0 and account_issuer not in ALL_NETWORKS:
                raise errors.AccountIssuerRequired

            request_data = self.generateMobileBody(
               
                pass_code,
                ACCOUNT_ISSUERS.get(account_issuer),
                account_number,
                description,
                amount,
                r_switch,

                )

        request = requests.post(f'{baseUri}/{endpoint}',json=request_data,headers=headers)

        if (request.status_code==200):
            data=request.json()
            return {
                "status":data.get("status"),
                "account_name": data.get("account_name"),
                "reference_id": data.get("reference_id"),

            }
        
        return  {
            "status" : request.status_code,
            "message": f"An Error({request.status_code}), could not handle for transfer of funds"
        }


    def compleTransfer(self,referenceId):
        
        if len(referenceId) ==0:
            raise errors.ReferenceIdRequired

        baseUrl=self.client.environment.getBaseUrl()
        endpoint='v1.1/transaction/bank/ftc/authorize'
        headers=generateHeader(self)
        body={
            "merchant_id" : self.client.merchant_id,
            "reference_id" : referenceId
        }

        res = requests.post(f"{baseUrl}/{endpoint}",headers=headers,data=body)

        if (res.status==200):
            data=res.json()
            return data

        return {
            "status":"Error",
            "message":f"An Error ({res.status} occurred), could not complete the transfer"
        }

