import requests
import json 
from .baseline_schemas import *
import os 
import pandas as pd

# 라우터 및 body 값에 넣어줄 pydantic
from fastapi import APIRouter

# config
from config.create import CompletionExecutor
from config.get_api import * 

# 개인 key
host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp = issued_keys()

# FastAPI 라우터 설정

router = APIRouter(prefix="/baseline",
                    tags=["baseline-section"],
                   responses={404:{"description":"Not Found"}}
                   )

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
    preset_text = [{"role":"system","content":"- 제품명과 블로그 제목을 통해 블로그 머릿말 6개까지 생성\n\n\n제품명 : 맥북 \n블로그 제목 :맥북프로16인치 구입기 (MacBook Pro 16)\n블로그 머릿말 :\\n - 전문가용 고성능 노트북 맥북프로16인치\\n - 4K 고해상도 레티나 디스플레이 탑재\\n - USB-C 타입 단자로 연결성 강화\\n 키보드 백라이트 기능 지원\\n - 맥북 프로 m1 14인치 (Pro) 장점 단점 리뷰\\n - 맥북프로 M1 PRO 14인치 1년 후기, M2 기변은 보류\\n -애플 M3 Pro는 소문대로 역대급 똥망일까? 맥북프로 14인치 스페이스 블랙 언빡싱!"},{"role":"user","content":"제품명: 애플워치\n블로그 제목 : 애플워치 SE 40mm 실버 알루미늄 케이스와 스포츠 루프 개봉기(Apple Watch SE)"},{"role":"assistant","content":"블로그 머릿말 : \n\n- 가성비 좋은 애플워치SE 입문용으로 딱!\n- 심전도 측정이 가능한 애플워치 시리즈6 가격 비교\n- 애플워치 에르메스 에디션 줄질하기 좋은 스마트 워치 추천\n- 애플워치 7세대 41mm GPS 나이키 에디션 운동할 때 필수템\n- 애플워치 se 44mm gps vs 셀룰러 고민 해결해드림\n- 애플워치 울트라 49mm 티타늄 케이스 남자 손목에 어울리는 다이버 워치"}
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
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    execute = completion_executor.execute(request_data)
    result = dict(pd.DataFrame(execute["result"]["message"]["content"].split("-")[1:])[0].str.strip())
    return result