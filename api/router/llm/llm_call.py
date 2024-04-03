import requests
import json 
from dotenv import load_dotenv
from .llm_schemas import *
import os 

# api key 환경변수 설정
load_dotenv("/home/ubuntu/seller-api/api/router/llm/.env")

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

@router.post("/generate-product-name") 
async def generate_product_name(request: CategoryRequestModel): # pydantic 내에서 정의한 CategoryRequestModel 을 가리킴 
    category_name = request.category
    preset_text = [{"role":"system","content":"- 상품명 생성을 위해 특정 키워드를 입력했을 때, 상품에 어울리는 상품명 생성 \n\n\n카테고리명: 사과\n상품명: 고당도 홍로 사과 3kg 달콤한 가정용\n다른키워드: 1. 황금사과 2. 선물세트 3. 5kg 4. 청송 5. 못난이 6. 시나노골드 7. 꿀사과 8. 부사 9. 10kg 10. 감홍"},{"role":"user","content":"카테고리명: 커피\n상품명:\n다른키워드:"},{"role":"assistant","content":"카테고리명: 커피\n상품명 : 콜롬비아 수프리모 원두커피 200g 고소한 당일 로스팅\n다른키워드 : 1. 케냐AA 2. 예가체프 3. 디카페인 4. 에스프레소 5. 더치커피 6. 핸드드립 7. 대용량 8. 콜드브루 9. 모카포트 10. 아메리카노"},{"role":"user","content":"카테고리명: 노트북\r\n상품명:\r\n다른키워드:"},{"role":"assistant","content":"카테고리명: 노트북\n상품명 : 삼성 갤럭시북2 프로 15인치 인텔 i7 가벼운 대학생 노트북\n다른키워드 : 1. 맥북프로 2. 그램 3. 게이밍노트북 4. 사무용노트북 5. 울트라북 6. 태블릿 7. 윈도우 11 8. 가성비 9. 리퍼비시 10. 중고"},
     {"role": "user", "content": f"카테고리명:{category_name}\n상품명:\n다른키워드:"}]
    # 프롬프팅 학습 후 content 값에 api 요청을 통해 사용자 입력값 넣어줌
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


@router.post("/generate-post")
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


@router.post("/generate-content")
async def generate_content(requests: ContentCreateModel):
    product_name = requests.productname
    content_title = requests.contenttitle 
    preset_text = [{"role":"system","content":"- 제품명과 블로그 제목 그리고 머릿말을 기준으로 블로그 리뷰 내용 작성 \n\n\n제품명 : 맥북 \n블로그 제목 : 애플 노트북 추천, 맥북 에어 M1칩 리뷰 (Feat. 맥린이)\n머릿말1 : 가성비 좋은 맥북을 찾는다면? 맥북에어 13인치가 정답!\n내용1 : 평소 관심 있게 지켜보던 맥북에어 m1칩 모델 드디어 구매했어요.\\n맥북 시리즈 중에서도 가격 대비 성능 가장 우수해서 망설임 없이 선택했답니다.\\n이번에 새로 출시된 신형모델인데 쿠팡에서 카드 할인 적용하면 100만원 초반대에 살 수 있거든요.\\n윈도우 설치 필요없는 완전한 윈도우 머신 찾고 계신다면 이만한 게 없을 거예요.\n머릿말2:최신형 M1칩 탑재한 고성능 노트북\n내용2 : 애플 자체 개발 프로세서인 M1칩 장착되어 있는데 이게 어마어마한 스펙이더라고요.\n기존 인텔 CPU보다 훨씬 더 빠른 속도 자랑하는데다 배터리 효율도 높아져서 하루 종일 써도 끄떡없어요.\\n심지어 발열현상 거의 없기 때문에 장시간 이용해도 불편함 전혀 느껴지지 않더라고요."},{"role":"user","content":"제품명 : 키친아트 1인용 캠핑 밥솥 \n블로그 제목:키친아트 1인용 캠핑 밥솥 추천합니다~\n머릿말1: 컴팩트한 사이즈로 휴대가 간편한 키친아트1인용캠핑밥솥\n머릿말2: 최대 12시간 보온 기능으로 언제든지 따뜻한 밥 먹을 수 있음"},{"role":"assistant","content":"제품 명 : 키친아트 1인용 캠핑 밥솥\n제목 : 혼자서도 맛있는 밥을 해먹자! 키친아트 1인용 미니 전기밥솥\n머리말1 : 가볍게 떠나는 캠핑 여행에도 따끈한 밥 한끼를 포기할 수 없다면?\n내용1 : 작고 귀여운 크기와 가벼운 무게로 어디든 부ㅔ담없이 들고 다닐 수 있는 제품이에요. \\n작지만 알찬 구성품들로 취사부터 보온까지 가능해 야외에서도 갓 지은 밥을 즐길 수 있어요.\n머리말2 : 작지만 강한 화력으로 빠르고 맛있는 밥 완성\n내용2 : 쾌속취사 모드를 지원하여 단 15분만에 맛있는 밥이 완성됩니다. \\n최대 12시간 보온기능으로 언제어디서든 따뜻하고 맛있는 밥을 드실 수 있습니다."},{"role":"user","content":"제품명: 애플워치\n블로그 제목: 애플워치 6세대 40mm 스페이스그레이 알루미늄케이스 블랙스포츠밴드 리뷰\n머리말1:심박수 측정 및 혈중 산소포화도 체크 가능한 애플워치 시리즈6\n머리말2:다양한 운동 종목 지원하는 스포츠밴드 탑재"},{"role":"assistant","content":"제품명 : 애플워치 6세대\n블로그 제목 : 건강 관리 필수템! 애플워치 6세대 40mm GPS+셀룰러 모델 후기\n머리말1 : 손목 위 주치의 역할 똑똑히 해내는 스마트 워치\n내용1 : 심전도(ECG)측정 ,혈중 산소 포화도 측정 등 다양한 건강 모니터링 기능 제공해요.  \n언제 어디서나 내 몸 상태 실시간 확인 할 수 있어서 너무 편리하더라고요.\n애플케어 플러스 가입 시에는 무상 수리 2회 보장 받을 수 있으니 참고하세요.\n머리말2 : 다양한 운동 모드 지원하는 스포츠 밴드\n내용2 : 요가, 필라테스, 러닝, 사이클링 등 각종 운동 모드 지원하며 활동링 통해 일일 활동량 체계적으로 관리할 수 있어요.\n방수 등급 높아서 수영이나 샤워할 때도 착용 가능하니 활용도 정말 높더라고요.\n무게 가볍고 두께 얇아서 일상생활 속에서 착용해도 거슬림 전혀 없어요."},{"role":"user","content":"제품명: \r클래식무테안경 \n블로그 제목 : 클래식 무테 안경 리뷰"},{"role":"assistant","content":"제품명 : 클래식 무테 안경\n블로그 제목 : 지적인 매력 뿜뿜! 클래식 무테 안경 스타일링\n머리말1 : 깔끔하고 세련된 디자인으로 남녀 모두에게 사랑받는 아이템\n내용1 : 군더더기 없이 깔끔한 디자인으로 어떤 룩에나 잘 어울려요.\n특히 정장이나 셔츠 같은 포멀한 룩에 매치하면 더욱 멋스러워 보여요.\n소재나 컬러에 따라 다양한 분위기 연출할 수 있다는 것도 장점이에요.\n머리말2 : 렌즈 교체 용이해 실용적인 아이템\n내용2 : 렌즈 교체가 용이해 시력 변화나 용도에 따라 자유롭게 바꿀 수 있어요.\n자외선 차단 기능 갖춘 렌즈 선택하면 눈 건강에도 도움이 돼요.\n코받침이나 다리 부분 조절 가능해 착용감도 편안해요."},
                   {"role":"user","content":f"제품명:{product_name}\n블로그 제목:{content_title}"}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 1952,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    completion_executor = CompletionExecutor(host_tmp,api_key_tmp,api_key_primary_val_tmp,request_id_tmp)
    return completion_executor.execute(request_data)