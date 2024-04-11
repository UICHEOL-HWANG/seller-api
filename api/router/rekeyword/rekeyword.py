# library 
import hashlib,hmac,base64
import time
import json
from fastapi import APIRouter
import re 

# Module 
from .rekeyword_schemas import *
from config.get_api import * 
from config.crawl import * 

# access_key
host_tmp, api_key_tmp, api_key_primary_val_tmp, request_id_tmp = issued_keys()

router = APIRouter(prefix="/re_keyword",
                    tags=["rekeyword-section"],
                   responses={404:{"description":"Not Found"}}
                   )

@router.post("/generate_rekeyowrd")
async def generate_keyword(request: RekeywordRequests):
    keyword = request.keyword
    keyword = keyword.replace(" ","")
    hintKeywords = [keyword]
    
    resultdf = getresults(hintKeywords)
    resultdf['monthlyPcQcCnt'] = resultdf['monthlyPcQcCnt'].apply(lambda x: re.sub("<", "", x) if "<" in str(x) else x)
    resultdic = resultdf.loc[:4, ["relKeyword", "monthlyPcQcCnt", "compIdx"]].to_dict()
    
    return resultdic