from pydantic import BaseModel #otomatik olarak tip kontrolü ve doğrulama yapar
from typing import Optional,List

class PostBase(BaseModel):
    title: str
    content: str
    media_url: Optional[str]=None
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    owner_id:int
    class Config:
        orm_mode=True

class UserBase(BaseModel):
    username:str
    email: str
    
    class Config:
        orm_mode:True    
    
class UserCreate(UserBase):
    password:str
    
class User(UserBase):
    id:int
    post: List[Post]=[]
    
    class Config:
        orm_mode:True
        
        