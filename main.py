from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import create_engine, Column, Integer, String, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

    UserID = Column(Integer, primary_key=True, index=True)  # 使用 UserID 而不是 id
    name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    age = Column(Integer, nullable=True)  # 若年齡欄位允許為空
    preferences = Column(JSON, nullable=True)  # 假設偏好設置為 JSON 類型
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")  # 預設創建時間

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
         from_attributes = True  # 確保與 SQLAlchemy 模型的屬性匹配

# Pydantic 模型：登入資料
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
         from_attributes = True  # 確保與 SQLAlchemy 模型的屬性匹配

# 密碼加密
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 密碼驗證
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# API：用戶註冊
@app.post("/register")
async def register_user(user: UserCreate, request: Request):
    try:
        db = SessionLocal()
        # 檢查用戶是否已存在
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="該 Email 已經註冊過")

        hashed_password = get_password_hash(user.password)
        new_user = User(
            name=user.name,
            phone=user.phone,
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "用戶註冊成功", "user_id": new_user.UserID}  # 返回 UserID 而非 id

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        db.close()  # 確保資料庫會話關閉

# API：用戶登入
@app.post("/login")
async def login_user(user: UserLogin, request: Request):
    try:
        db = SessionLocal()
        # 查找用戶
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user:
            raise HTTPException(status_code=400, detail="用戶不存在")

        # 驗證密碼
        if not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="密碼錯誤")

        return {"message": "登入成功", "user_id": existing_user.UserID}

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    finally:
        db.close()  # 確保資料庫會話關閉
 #  cd "C:\Users\lunnn\OneDrive\桌面"
           #uvicorn main:app --reload       

