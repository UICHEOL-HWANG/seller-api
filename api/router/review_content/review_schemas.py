from pydantic import BaseModel

class ContentCreateModel(BaseModel):
    productname : str 
    contenttitle : str
    keyword : str 
    outline : str