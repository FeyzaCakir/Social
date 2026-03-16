from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException

def get_user_by_email(db: Session,email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user= models.User(
        username= user.username,
        email= user.email,
        password= user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def create_post(db: Session, post_data: dict, user_id: int):
    db_post = models.Post(
        title=post_data["title"],
        content=post_data["content"],
        media_url=post_data.get("media_url"),
        owner_id=user_id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int=0, limit: int=10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def delete_post(db:Session,post_id:int, user_id:int):
    post=db.query(models.Post).filter(models.Post.id== post_id).first()
    
    if not post:
        return {"error":"Post bulunamadı"}
    
    if post.owner_id != user_id:
        return {"error":"Bu göderiyi silmeye yetkiniz yok"}
    
    db.delete(post)
    db.commit()
    return {"message":"Post silindi."}