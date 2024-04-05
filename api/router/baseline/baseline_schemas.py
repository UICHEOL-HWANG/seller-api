from pydantic import BaseModel

# BaseModel

class ProductNameModel(BaseModel):
    productname : str

class BlogPostNameModel(BaseModel):
    productname : str
    contenttitle : str
