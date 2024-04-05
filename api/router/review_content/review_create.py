# library
import requests
import json 
from fastapi import APIRouter


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
    preset_text = [{"role":"system","content":"제품명과 블로그 제목 핵심키워드를 입력 받으면 그에 맞는 리뷰 아웃라인에는(-)하이픈으로 구분시켜주고 리뷰 생성에는 느낌표(!)로 구분 내용만 출력\n제품명:맥북\n블로그 제목:애플 노트북 추천, 맥북 에어 M1칩 리뷰 (Feat. 맥린이)\n키워드:맥북,맥북프로,아이패드중고,애플맥북,맥북중고\n아웃라인: -가성비 좋은 맥북을 찾는다면 맥북에어 13인치가 정답! -최신형 M1칩 탑재한 고성능 노트북 -뛰어난 휴대성으로 언제 어디서나 작업 가능 -터치 ID로 간편하게 잠금 해제 및 로그인\n내용: -가성비 좋은 맥북을 찾는다면 맥북에어 13인치가 정답!\n!평소 관심 있게 지켜보던 맥북에어 m1칩 모델 드디어 구매했어요.\n맥북 시리즈 중에서도 가격 대비 성능 가장 우수해서 망설임 없이 선택했답니다.\n이번에 새로 출시된 신형모델인데 쿠팡에서 카드 할인 적용하면 100만원 초반대에 살 수 있거든요.윈도우 설치 필요없는 완전한 윈도우 머신 찾고 계신다면 이만한 게 없을 거예요.\n-최신형 M1칩 탑재한 고성능 노트북\n!애플 자체 개발 프로세서인 M1칩 장착되어 있는데 이게 어마어마한 스펙이더라고요.\n기존 인텔 CPU보다 훨씬 더 빠른 속도 자랑하는데다 배터리 효율도 높아져서 하루 종일 써도 끄떡없어요. 심지어 발열현상 거의 없기 때문에 장시간 이용해도 불편함 전혀 느껴지지 않더라고요.\n-뛰어난 휴대성으로 언제 어디서나 작업 가능\n!무게 1.29kg밖에 되지 않아서 백팩에 넣고 다니기 부담스럽지 않아요.\n크기도 적당해서 들고 다닐 때 큰 불편함 못 느꼈네요.장소 구애받지 않고 일할 수 있다는 점이 저에게는 매우 매력적이었어요.\n\n\n"},{"role":"user","content":"제품명:손흥민 축구화\n블로그 제목:아디다스 손흥민 축구화 X 스피드플로우 + 퓨어컷 TF 인조잔디 풋살화 리뷰.\n키워드:손흥민,축구,국가대표,월드컵,EPL\n아웃라인: -손흥민 선수가 착용하는 아디다스 대표 축구화, -가볍고 유연한 소재로 빠른 움직임 가능, -안정적인 지지력과 스터드 배열로 잔디 위에서 최적의 성능 발휘, -다양한 컬러와 사이즈로 선택의 폭 넓음"},{"role":"assistant","content":"내용 : \n-손흥민 선수가 착용하는 아디다스 대표 축구화\n !얼마 전 끝난 카타르 월드컵에서 우리나라 국가대표 손흥민 선수가 신고 뛰었던 바로 그 축구화예요.세계적인 선수가 신는 제품이라 그런지 디자인부터 남다르더라고요.실제로 보니 더 멋있어서 한눈에 반했답니다.\n \n -가볍고 유연한 소재로 빠른 움직임 가능\n !초경량 소재로 만들어져 있어서 무게감 거의 느껴지지 않을 정도로 가벼워요.신발 전체적으로 유연하게 설계되어 있어서 빠른 방향 전환이나 순간적인 가속에도 발이 밀리지 않고 안정적으로 움직일 수 있어요.\n \n -안정적인 지지력과 스터드 배열로 잔디 위에서 최적의 성능 발휘\n !발의 아치 부분을 받쳐주는 서포트 시스템이 내장되어 있어서 발을 단단하게 고정시켜 줘요.스터드 배열도 잔디 상태에 맞게 최적화되어 있어서 미끄러짐 없이 자유롭게 움직일 수 있답니다.\n \n -다양한 컬러와 사이즈로 선택의 폭 넓음\n !컬러는 화이트, 블랙, 블루 등 다양하게 나와서 취향에 맞게 선택할 수 있어요.사이즈도 폭넓게 나와서 발 크기에 상관없이 누구나 신을 수 있고요.저는 개인적으로 깔끔한 화이트 컬러가 마음에 들어서 그걸로 골랐는데 실물이 더 예쁘더라고요."},{"role":"user","content":"제품명: 에어팟 맥스 \n블로그 제목: 에어팟 맥스 리뷰 남깁니다 \n키워드: 에어팟맥스,이어폰\n아웃라인 : - 가성비 좋은 에어팟맥스, - 에어팟 맥스 가벼움, - 안정적인 착용감과 노이즈 캔슬링, 다양한 컬러"},{"role":"assistant","content":"내용 : \n-가성비 좋은 에어팟맥스\n!애플에서 출시한 헤드폰 중에서는 비교적 저렴한 가격대에 속하지만 성능 면에서는 결코 뒤지지 않아요.노이즈 캔슬링 기능이 뛰어나서 주변 소음을 완벽하게 차단해 주고 음질도 선명하고 풍부해요.\n\n-에어팟 맥스 가벼움\n!무게가 약 384g으로 가벼워서 장시간 착용해도 불편함이 없어요.또 헤드밴드가 부드럽게 늘어나서 머리 크기에 맞게 조절할 수 있고 이어컵이 회전하기 때문에 착용감이 좋아요.\n\n-안정적인 착용감과 노이즈 캔슬링\n!착용감이 좋아서 운동할 때나 이동할 때도 편하게 사용할 수 있어요. 또 노이즈 캔슬링 기능이 뛰어나서 주변 소음을 완벽하게 차단해 주기 때문에 음악이나 영상에 집중할 수 있어요.\n\n-다양한 컬러\n!컬러는 그레이, 그린, 블루, 핑크, 실버 총 5가지로 다양하게 나와서 취향에 맞게 선택할 수 있어요.디자인도 깔끔하고 세련되어서 패션 아이템으로도 활용할 수 있어요."}
                  ,{"role":"user","content":f"제품명:{productname} \n블로그 제목:{contenttitle}\n키워드:{keyword} \n아웃라인:{outline}"}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 2600,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    return completion_executor.execute(request_data)







