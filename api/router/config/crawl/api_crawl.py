import requests
import pandas as pd 
import hashlib,hmac,base64
import time

import json

from dotenv import load_dotenv 
import os 

from ...llm.llm_call import * 
from ...llm.llm_schemas import *

import re 

load_dotenv(r"/home/ubuntu/seller-api/api/.env")

host_tmp = os.getenv('host_key')
api_key_tmp= os.getenv('api')
api_key_primary_val_tmp = os.getenv('val')
request_id_tmp = os.getenv('request')

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



router = APIRouter(prefix="/keyword-test",
                    tags=["keyword-test"],
                   responses={404:{"description":"Not Found"}}
                   )

@router.post("/test-keyword")
def post_request_data(request:CategoryRequestModel):
    product_name = request.product
    title_name = request.title
    preset_text =[{"role":"system","content":"제품명과 블로그 제목을 통해 키워드 생성  키워드는 하이픈(-)으로 구분\n제품명: 맥북\n블로그 제목: -애플 노트북 추천, 맥북 에어 M1칩 리뷰\n키워드 추천: -맥북 -맥북프로 -아이패드중고,애플맥북 -맥북중고"},{"role":"user","content":"제품명:밥솥\n블로그 제목:쿠쿠 압력밥솥 리뷰"},{"role":"assistant","content":"키워드 추천 : -밥솥 -쿠쿠압력밥솥 -전기밥솥추천 -압력밥솥가격"},{"role":"user","content":"제품명:오렌지\n블로그 제목: 천혜향 맛있는 리뷰"},{"role":"assistant","content":"키워드 추천 : -오렌지 -천혜향 -한라봉 -황금향"}
                  ,{"role":"user","content":f"제품명:{product_name}\n블로그 제목:{title_name}"}]
    request_data = {
            'messages': preset_text,
            'messages.role':'user',
            'messages.content' : 'content',
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 256,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }
    
    completion_executor = CompletionExecutor(host_tmp, api_key_tmp, api_key_primary_val_tmp, request_id_tmp)
    response_data = completion_executor.execute(request_data)
    
    cleaned_data = [i.strip() for i in response_data["result"]["message"]["content"].split("-")[1:]]
    hintKeywords = cleaned_data
    
    resultdf = getresults(hintKeywords)
    resultdf['monthlyPcQcCnt'].apply(lambda x: re.sub("<", "", x) if "<" in str(x) else x)
    resultdic = resultdf.loc[:4, ["relKeyword", "monthlyPcQcCnt", "compIdx"]].to_dict()
    
    return resultdic

