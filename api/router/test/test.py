from fastapi import APIRouter 

router = APIRouter(prefix="/test",
                   tags=["test"],
                   responses={404:{"description":"Not Found"}}
                   )

@router.get("/test")
async def get_test():
    return {"Hello": "World"}