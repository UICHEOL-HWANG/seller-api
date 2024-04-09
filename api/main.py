from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#router 
from router.baseline.baseline import router as content_router
from router.keyword.keyword import router as keywor_router
from router.review_content.review_create import router as review_router
from router.rekeyword.rekeyword import router as rekeyword_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 라우터 포함
app.include_router(content_router)
app.include_router(keywor_router)
app.include_router(review_router)
app.include_router(rekeyword_router)

# Uvicorn으로 FastAPI 애플리케이션 실행 (개발용)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)