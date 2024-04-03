from pydantic import BaseModel

# BaseModel
class CategoryRequestModel(BaseModel):
    category: str


class ProductNameModel(BaseModel):
    productname : str

class BlogPostNameModel(BaseModel):
    productname : str
    contenttitle : str
    
class ContentCreateModel(BaseModel):
    productname : str 
    contenttitle : str