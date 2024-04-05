from dotenv import load_dotenv
import os 

# api key 환경변수 설정
# load_dotenv("/home/ubuntu/seller-api/api/router/llm/.env")
load_dotenv(r"C:\Users\UICHEOL_HWANG\Desktop\seller\api\config\.env")

def issued_keys():
    host_tmp = os.getenv('host_key')
    api_key_tmp= os.getenv('api')
    api_key_primary_val_tmp = os.getenv('val')
    request_id_tmp = os.getenv('request')
    return host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp

def naver_issued_keys():
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")
    secrets = os.getenv("SECRET_KEY")
    customer_id = os.getenv("CUSTOMER_ID")
    
    return base_url,api_key,secrets,customer_id

