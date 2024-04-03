from typing import Union
import uvicorn
from fastapi import FastAPI
from router.llm.llm_call import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 라우터 포함
app.include_router(router)

# Uvicorn으로 FastAPI 애플리케이션 실행 (개발용)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)