from fastapi import FastAPI, Depends, HTTPException, Request, Form,Header,File,UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
import models, schemas, crud
from database import engine, SessionLocal
from models import User
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import shutil
import os

# --------------------- Database ---------------------
models.Base.metadata.create_all(bind=engine) #SQLAlchemy ORM ile tanımlan tüm tabloları veritabanında oluşturmak için

def get_db():
    db = SessionLocal()
    try:
        yield db #Bu session, çağıran fonksiyona "geçici olarak" verilir
    finally:
        db.close()

def get_current_user(
    request: Request,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    # Eğer preflight (OPTIONS) isteği ise, kullanıcı doğrulama yapma
    if request.method == "OPTIONS":
        return None

    if not authorization:
        raise HTTPException(status_code=401, detail="Token Bulunamadı")

    token = authorization.replace("Bearer", "").strip()

    if token != "fake-jwt-token":
        raise HTTPException(status_code=401, detail="Token Geçersiz")

    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="User bulunamadı")

    print(f">> get_current_user başarılı: {user.username} (id={user.id})")
    return user


# --------------------- App Init ---------------------
app = FastAPI(redirect_slashes=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # her yerden izin
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, OPTIONS hepsi
    allow_headers=["*"],   # Authorization dahil tüm header'lar
)
# --------------------- Static & Templates ---------------------
app.mount("/static", StaticFiles(directory="static"), name="static") #ana uygulamaya başka bir uygulamayı veya dosya servislerini eklemek (montaj)
templates = Jinja2Templates(directory="templates")

# --------------------- HTML ROUTES ---------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ---------- API ENDPOINTLER ----------

class LoginRequest(BaseModel):
    email: str
    password: str

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.post("/login")
async def login_user(data: LoginRequest,db: Session=Depends(get_db)):
    
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404,detail="KULLANICI BULUNAMADI!")
    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Şifre hatalı")

    return {"access_token": "fake-jwt-token",
            "user_id":user.id
            }
    
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register", response_model=schemas.User)
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    # Önce email kontrolü
    db_user = crud.get_user_by_email(db, data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Kullanıcıyı DB’ye kaydet
    new_user = crud.create_user(db, schemas.UserCreate(
        username=data.username,
        email=data.email,
        password=data.password
    ))
    return new_user

@app.delete("/posts/{post_id}")
def delete_post(
    post_id:int,
    db:Session=Depends(get_db),
    current_user: models.User= Depends(get_current_user) 
):
    return crud.delete_post(db,post_id,current_user.id)

# --------------------- API ROUTES ---------------------
@app.options("/posts")
def options_posts():
    return Response(status_code=200)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_user(db, user)

@app.post("/posts", response_model=schemas.Post)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    media_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    media_url = None

    # Eğer dosya geldiyse kayıt et
    if media_file:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = f"{upload_dir}/{media_file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(media_file.file, buffer)

        media_url = f"/static/uploads/{media_file.filename}"

    # Veritabanına kaydet
    db_post = models.Post(
        title=title,
        content=content,
        media_url=media_url,
        owner_id=current_user.id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/posts", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)


# uvicorn main:app --reload