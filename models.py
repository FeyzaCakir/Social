from sqlalchemy import Column,Integer,String,ForeignKey,Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    username= Column(String,unique=True,index=True)
    email= Column(String,unique=True,index=True)
    password= Column(String)
    posts= relationship("Post", back_populates="owner")
    
class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,index=True)
    title= Column(String)
    content=Column(Text)
    media_url= Column(String, nullable=True)
    owner_id= Column(Integer,ForeignKey("users.id"))
    owner= relationship("User", back_populates="posts")