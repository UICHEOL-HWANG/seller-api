import requests
import json 
from dotenv import load_dotenv
from .llm_schemas import *
import os 

# api key 환경변수 설정
# load_dotenv("/home/ubuntu/seller-api/api/router/llm/.env")
load_dotenv(r"C:\Users\UICHEOL_HWANG\Desktop\seller\api\router\llm\.env")

host_tmp = os.getenv('host_key')
api_key_tmp= os.getenv('api')
api_key_primary_val_tmp = os.getenv('val')
request_id_tmp = os.getenv('request')

# 라우터 및 body 값에 넣어줄 pydantic
from fastapi import APIRouter

# clova Api request 
class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id
        
        

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
        }
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            return json.loads(r.text)
        # requests로 요청 받은 값 json 반환


# FastAPI 라우터 설정
router = APIRouter()
# prefix 설계 예정


@router.post("/generate-post-name")
async def generate_blog_post_name(request : ProductNameModel):
    product_name = request.productname
    preset_text = [{"role":"system","content":"-제품명에 따른 블로그 제목 생성 생성 제목에 하이픈(-)은 무조건 붙어줘야함 \n\n\n제품명:맥북\n블로그 제목:-맥북에어 M1칩 탑재한 애플의 노트북 개봉기\n-애플 맥북 에어 13인치 M1 2020년형 256GB 실버 후기 추천 Macbook Air Apple A2337\n맥북에어 M1 13인치 노트북 추천 및 개봉기\n\n\n\n제품명: 맥북 \n블로그 제목:- 맥북프로16인치 구입기\n - 애플 맥북에어 M1 13인치 2020 스페이스그레이 256GB 후기\n -맥북에어 M1 13인치 개봉기 및 구매 후기"},{"role":"user","content":"제품명: 맥북"},{"role":"assistant","content":"블로그 제목 : \n- 맥북 프로 14인치 M1 Max 2021 고급형 성능, 가격, 디자인 분석!\n- 맥북 프로 vs 맥북 에어 선택 가이드와 장단점 비교하기\n- 맥북에서 윈도우 사용하기? 패러렐즈 데스크톱 17 구독 및 설치 방법"},{"role":"user","content":"제품명: 애플워치"},{"role":"assistant","content":"블로그 제목 :\n-애플워치 SE 40mm GPS 실버 알루미늄 케이스 화이트 스포츠 밴드 개봉기 및 일주일 사용 후기\n-애플워치 시리즈 6 44mm 나이키 에디션 언박싱 및 초기 설정 방법 \n- 애플워치로 아이폰 잠금해제하기"},
    {"role":"user","content":f"제품명: {product_name}"}]
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
    
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    return completion_executor.execute(request_data)


@router.post("/generate-post-outline")
async def generate_post_content(request : BlogPostNameModel):
    product_name = request.productname
    title_name = request.contenttitle
    preset_text =[{"role":"system","content":"- 제품명과 블로그 제목을 통해 블로그 머릿말 생성 \n\n\n제품명 : 맥북 \n블로그 제목 :맥북프로16인치 구입기 (MacBook Pro 16)\n블로그 머릿말 :\\n - 전문가용 고성능 노트북 맥북프로16인치\\n - 4K 고해상도 레티나 디스플레이 탑재\\n - USB-C 타입 단자로 연결성 강화\\n 키보드 백라이트 기능 지원"},{"role":"user","content":"제품명: 애플워치\n블로그 제목 : 애플워치 SE 40mm 실버 알루미늄 케이스와 스포츠 루프 개봉기(Apple Watch SE)"},{"role":"assistant","content":"블로그 머릿말 :\n- 스마트 워치 시장 점유율 1위 애플워치SE\n- 건강 관리 및 다양한 운동 모드 지원\n- 아이폰과의 연동으로 편리한 사용성 제공\n- 세련된 디자인과 다양한 스트랩 선택 가능"},{"role":"user","content":"제품명 : 기계식 키보드\n블로그 제목 : 콕스 CK87 게이트론 LED 게이밍 기계식 키보드 갈축"},{"role":"assistant","content":"블로그 머릿말 :\n- 가성비 좋은 텐키리스 기계식 키보드 추천\n- 경쾌한 타건감의 게이트론 스위치 적용\n- 화이트 단일 LED 백라이트로 깔끔한 디자인\n- 스텝스컬쳐2 설계로 편안한 타이핑 환경 제공"},
     {"role":"user","content":f"제품명: {product_name} \n블로그 제목 :{title_name} "}]
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
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    return completion_executor.execute(request_data)


@router.post("/generate-keyword")
async def generate_category(request: CategoryRequestModel):
    product_name = request.product
    title_name = request.title
    
    
    preset_text =[{"role":"system","content":"제품명과 블로그 제목을 통해 키워드 생성  키워드는 하이픈(-)으로 구분\n제품명: 맥북\n블로그 제목: -애플 노트북 추천, 맥북 에어 M1칩 리뷰\n키워드 추천: -맥북 -맥북프로 -아이패드중고,애플맥북 -맥북중고"},{"role":"user","content":"제품명:밥솥\n블로그 제목:쿠쿠 압력밥솥 리뷰"},{"role":"assistant","content":"키워드 추천 : -밥솥 -쿠쿠압력밥솥 -전기밥솥추천 -압력밥솥가격"},{"role":"user","content":"제품명:오렌지\n블로그 제목: 천혜향 맛있는 리뷰"},{"role":"assistant","content":"키워드 추천 : -오렌지 -천혜향 -한라봉 -황금향"}
                  ,{"role":"user","content":f"제품명:{product_name}\n블로그 제목:{title_name}"}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 256,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    return completion_executor.execute(request_data)