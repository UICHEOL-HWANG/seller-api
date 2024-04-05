import requests
import pandas as pd 
import hashlib,hmac,base64
import time
import json


from dotenv import load_dotenv 
import os 

load_dotenv("/home/ubuntu/seller-api/api/.env")

base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
secrets = os.getenv("SECRET_KEY")
customer_id = os.getenv("CUSTOMER_ID")


class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        
        hash.hexdigest()
        return base64.b64encode(hash.digest())
    

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}


def getresults(hintKeywords):
    
    BASE_URL = base_url
    API_KEY = api_key
    SECRET_KEY = secrets
    CUSTOMER_ID = customer_id


    uri = '/keywordstool'
    method = 'GET'

    params={}

    params['hintKeywords']=hintKeywords
    params['showDetail']='1'

    r=requests.get(BASE_URL + uri, params=params, 
                 headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    return pd.DataFrame(r.json()['keywordList'])