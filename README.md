# FastAPI Social Media Backend

A **FastAPI-based social media backend application** that provides user authentication and post management with optional media uploads.
The system demonstrates **REST API design, database modeling with SQLAlchemy ORM, token-based authentication, file upload handling, and frontend integration via JavaScript.**

This project combines:

* **FastAPI** for high-performance API development
* **SQLAlchemy ORM** for relational database operations
* **Pydantic** for data validation
* **Jinja2 templates** for rendering HTML pages
* **Vanilla JavaScript** for client-side API consumption
* **SQLite** as the database

---

# System Architecture

The application follows a **layered architecture** separating responsibilities into different modules.

```
project/
│
├── main.py            # FastAPI application and API endpoints
├── database.py        # Database connection and SQLAlchemy session
├── models.py          # SQLAlchemy ORM models
├── schemas.py         # Pydantic schemas (data validation & serialization)
├── crud.py            # Database operations layer
│
├── templates/         # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── static/
│   ├── js/
│   │   ├── login.js
│   │   ├── register.js
│   │   └── dashboard.js
│   └── uploads/       # Uploaded media files
│
└── social.db          # SQLite database
```

This architecture separates:

* **API logic (main.py)**
* **database models (models.py)**
* **data validation schemas (schemas.py)**
* **database operations (crud.py)**

which improves maintainability and scalability.

---

# Core Technologies

| Technology           | Purpose                                 |
| -------------------- | --------------------------------------- |
| FastAPI              | High-performance Python web framework   |
| SQLAlchemy           | ORM for relational database interaction |
| SQLite               | Lightweight relational database         |
| Pydantic             | Data validation and serialization       |
| Passlib              | Password hashing utilities              |
| Jinja2               | HTML template rendering                 |
| JavaScript Fetch API | Client-side API communication           |
| CORS Middleware      | Cross-origin request handling           |

---

# Database Layer

Database configuration is defined in **database.py**.

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./social.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

### Session Management

```
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

Each request receives a **database session dependency**:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This ensures:

* automatic connection cleanup
* safe transaction handling

---

# Database Models

Database models are defined using **SQLAlchemy ORM**.

## User Model

```
User
│
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password
└── posts (relationship)
```

Example:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    posts = relationship("Post", back_populates="owner")
```

---

## Post Model

```
Post
│
├── id
├── title
├── content
├── media_url
└── owner_id (ForeignKey -> users.id)
```

Example:

```python
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    media_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
```

Each post belongs to a user through a **foreign key relationship**.

---

# Data Validation Layer

**Pydantic schemas** enforce request and response validation.

Example:

```
PostBase
│
├── title
├── content
└── media_url
```

Response schema:

```python
class Post(PostBase):
    id: int
    owner_id: int
```

Advantages:

* automatic request validation
* automatic API documentation
* type safety

---

# Authentication Mechanism

Authentication is implemented using a **token-based system**.

Login endpoint:

```
POST /login
```

Example response:

```
{
  "access_token": "fake-jwt-token",
  "user_id": 1
}
```

Client stores the token in **localStorage**.

```
localStorage.setItem("token", data.access_token)
```

Each protected request sends the token via **Authorization header**:

```
Authorization: Bearer fake-jwt-token
```

Server validates token using dependency:

```python
def get_current_user(...)
```

If validation fails:

```
HTTP 401 Unauthorized
```

---

# REST API Endpoints

## Authentication

### Register User

```
POST /register
```

Creates a new user account.

---

### Login

```
POST /login
```

Returns a token and user ID.

---

## Post Management

### Create Post

```
POST /posts
```

Supports **multipart form data** for media uploads.

Fields:

```
title
content
media_file (optional)
```

Uploaded files are saved to:

```
/static/uploads/
```

---

### Get Posts

```
GET /posts
```

Query parameters:

```
skip
limit
```

Used for pagination.

---

### Delete Post

```
DELETE /posts/{post_id}
```

Authorization rule:

* Only the **post owner** can delete their post.

---

# File Upload Handling

Media files are uploaded using **FastAPI UploadFile**.

Example:

```python
media_file: UploadFile = File(None)
```

File saving logic:

```python
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(media_file.file, buffer)
```

Saved file path is stored as:

```
/static/uploads/<filename>
```

Supported media:

* images
* videos

---

# Frontend Integration

Frontend pages interact with the API via **JavaScript Fetch API**.

Example request:

```javascript
fetch("/posts", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`
  },
  body: formData
})
```

The dashboard script handles:

* authentication check
* loading posts
* creating posts
* deleting posts
* file uploads

---

# CORS Configuration

The API enables **Cross-Origin Resource Sharing**:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

This allows frontend clients to access the API from different origins.

---

# Running the Application

### Install Dependencies

```
pip install fastapi uvicorn sqlalchemy passlib python-multipart jinja2
```

### Start Server

```
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Alternative documentation:

```
http://127.0.0.1:8000/redoc
```

---

# Key Backend Concepts Demonstrated

This project demonstrates:

* FastAPI dependency injection
* SQLAlchemy ORM modeling
* relational database design
* token-based authentication
* REST API architecture
* file upload handling
* frontend-backend API integration
* CORS configuration
* modular backend structure

---

# Possible Improvements

Future enhancements could include:

* real JWT authentication
* password hashing
* comment system
* likes / reactions
* pagination and infinite scroll
* user profiles
* Docker deployment
* PostgreSQL integration
