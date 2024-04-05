from pydantic import BaseModel

class CategoryRequestModel(BaseModel):
    product : str
    title : str