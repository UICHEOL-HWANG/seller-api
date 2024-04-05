# library
import requests
import json 
from fastapi import APIRouter
import pandas as pd 

# module
from .review_schemas import * 
from config.create import CompletionExecutor 
from config.get_api import * 

# access_key
host_tmp, api_key_tmp, api_key_primary_val_tmp, request_id_tmp = issued_keys()


router = APIRouter(prefix="/review",
                    tags=["review-section"],
                   responses={404:{"description":"Not Found"}}
                   )

@router.post("/create_review")
async def create_review_post(request : ContentCreateModel):
    productname = request.productname
    contenttitle = request.contenttitle
    keyword = request.keyword
    outline = request.outline
    preset_text = [{"role":"system","content":"제품명과 블로그 제목 핵심키워드를 입력 받으면 그에 맞는 리뷰 아웃라인에는(-)하이픈으로 구분시켜줌 \n\r\n제품명:맥북\r\n블로그 제목:애플 노트북 추천, 맥북 에어 M1칩 리뷰 (Feat. 맥린이)\r\n키워드:맥북,맥북프로,아이패드중고,애플맥북,맥북중고\r\n아웃라인: -가성비 좋은 맥북을 찾는다면 맥북에어 13인치가 정답 -최신형 M1칩 탑재한 고성능 노트북 -뛰어난 휴대성으로 언제 어디서나 작업 가능 -터치 ID로 간편하게 잠금 해제 및 로그인\r\n내용: -가성비 좋은 맥북을 찾는다면 맥북에어 13인치가 정답\n\n평소 관심 있게 지켜보던 맥북에어 m1칩 모델 드디어 구매했어요.맥북 시리즈 중에서도 가격 대비 성능 가장 우수해서 망설임 없이 선택했답니다.이번에 새로 출시된 신형모델인데 쿠팡에서 카드 할인 적용하면 100만원 초반대에 살 수 있거든요.윈도우 설치 필요없는 완전한 윈도우 머신 찾고 계신다면 이만한 게 없을 거예요.\n\n\n- 최신형 M1칩 탑재한 고성능 노트북\n\n애플 자체 개발 프로세서인 M1칩 장착되어 있는데 이게 어마어마한 스펙이더라고요.\r\n기존 인텔 CPU보다 훨씬 더 빠른 속도 자랑하는데다 배터리 효율도 높아져서 하루 종일 써도 끄떡없어요. 심지어 발열현상 거의 없기 때문에 장시간 이용해도 불편함 전혀 느껴지지 않더라고요.\r\n\n\n- 뛰어난 휴대성으로 언제 어디서나 작업 가능\r\n\n\n무게 1.29kg밖에 되지 않아서 백팩에 넣고 다니기 부담스럽지 않아요.크기도 적당해서 들고 다닐 때 큰 불편함 못 느꼈네요.장소 구애받지 않고 일할 수 있다는 점이 저에게는 매우 매력적이었어요.\n"},{"role":"user","content":"제품명:손흥민축구화\n블로그제목:손흥민 축구화 리뷰 \n키워드:축구화,국가대표,손흥민,흥민이,축알남\n아웃라인: -국가대표 손흥민의 축구화,- 손흥민이 가장 아끼던 축구화는?, -손흥민이 좋아하는 축구화?, -손흥민이 즐겨신는 축구화"},{"role":"assistant","content":"내용 :\n\n- 국가대표 손흥민의 축구화\n\n대한민국 축구 역사상 최고의 선수라 해도 과언이 아닌 손흥민 선수! 그런 손흥민 선수가 경기장에서 신는 축구화라면 당연히 많은 사람들의 관심을 끌겠죠? 이번 포스팅에서는 손흥민 선수가 실제로 착용하는 축구화에 대해 알아보겠습니다.\n\n- 손흥민이 가장 아끼던 축구화는?\n\n손흥민 선수가 가장 아끼는 축구화는 아디다스의 X 시리즈입니다. 이 축구화는 손흥민 선수가 어린 시절부터 꾸준히 착용해 온 것으로 유명한데요. 특히 2018년 러시아 월드컵에서 신었던 X 18+ 모델은 손흥민 선수에게 큰 행운을 가져다 준 것으로 알려져 있습니다.\n\n- 손흥민이 좋아하는 축구화?\n\n손흥민선수가 좋아하는 축구화는 나이키의 머큐리얼 베이퍼 14 엘리트 FG 입니다. 스피드와 민첩성을 강조한 디자인으로, 가볍고 유연한 소재로 제작되어 빠른 움직임에도 안정적인 지지력을 제공합니다. 또 스터드가 높아서 잔디 위에서 빠르게 방향을 전환할 수 있고, 순간적인 가속력을 높일 수 있어요.\n\n- 손흥민이 즐겨신는 축구화 ?\n\n손흥민 선수가 최근 자주 신는 축구화는 푸마의 퓨처 5.1 넷핏 HG/AG 입니다. 발을 감싸는 듯한 디자인으로 편안한 착용감을 제공하며, 다양한 색상과 패턴으로 자신만의 개성을 표현할 수 있는 제품이에요. 경량화 된 소재 덕분에 무게 또한 가벼워 체력 소모를 줄일 수 있으며, 내구성이 뛰어나서 오랜 시간 착용해도 손상이 적은 편이죠."}
                   ,{"role":"user","content":f"제품명:{productname}\r\n블로그제목:{contenttitle}\r\n키워드:{keyword}\r\n아웃라인:{outline}"}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 2800,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    
    
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    execute_date = completion_executor.execute(request_data)
    result_dct = {}
    result_dct["content"] = execute_date["result"]["message"]["content"].split(":")[1].strip()
    return result_dct





