from fastapi import FastAPI, HTTPException, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

# 資料庫連線設定
DB_USERNAME = "root"
DB_PASSWORD = "qwertyuiop123"
DB_HOST = "localhost"
DB_NAME = "world"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# 設定 SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 密碼加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定義 User 資料表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    password = Column(String(100))

# 建立資料表
Base.metadata.create_all(bind=engine)

# 啟動 FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源（開發時使用，正式環境請設置特定網域）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 模型：使用者註冊資料
class UserCreate(BaseModel):
    name: str
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')  # 使用 Field 和 pattern 驗證電話號碼格式
    email: EmailStr  # 郵箱格式
    password: str

    class Config:
         from_attributes = True

# 密碼哈希加密
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# API：用戶註冊
@app.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    # 檢查郵箱是否已經註冊
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="該 Email 已經註冊過")

    # 加密密碼
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, phone=user.phone, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    return {"message": "用戶註冊成功", "user_id": new_user.id}

# 啟動伺服器
# 在終端機執行： uvicorn main:app --reload

