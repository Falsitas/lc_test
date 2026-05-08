from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from starlette.responses import FileResponse, JSONResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from services.agent import LangChainTest

# uvicorn main:app --reload

# 설정
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 간단한 사용자 저장소 (실제로는 DB 사용)
users_db = {
    "admin": pwd_context.hash("admin123"),
    "user1": pwd_context.hash("password123"),
}

app = FastAPI()
agent = LangChainTest()

# 요청 모델
class QueryRequest(BaseModel):
    query: str

class LoginRequest(BaseModel):
    username: str
    password: str

# 함수들
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthCredentials = HTTPBearer()) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 라우트
@app.get("/")
async def root():
    return FileResponse("templates/index.html")

@app.post("/login/")
async def login(request: LoginRequest):
    """사용자 인증 및 토큰 발급"""
    # 사용자 확인
    if request.username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # 비밀번호 확인
    if not verify_password(request.password, users_db[request.username]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # 토큰 생성
    token = create_access_token(request.username)
    return {"token": token, "message": "Login successful"}

@app.post("/chat/")
async def run_chat(request: QueryRequest):
    response = agent.run_query(request.query)
    return {"response": response["messages"][-1].content}
