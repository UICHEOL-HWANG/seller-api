from pydantic import BaseModel

# BaseModel
class CategoryRequestModel(BaseModel):
    product : str
    title : str


class ProductNameModel(BaseModel):
    productname : str

class BlogPostNameModel(BaseModel):
    productname : str
    contenttitle : str
    
class ContentCreateModel(BaseModel):
    productname : str 
    contenttitle : str
    