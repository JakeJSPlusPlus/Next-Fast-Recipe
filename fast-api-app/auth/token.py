from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import os
import dotenv
from datetime import datetime, timedelta, timezone
from psycopg.connection import Connection
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from auth.pswd import User, get_user, authenticate_user
from database.get_conn import Conn


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
_ = dotenv.load_dotenv(env_path)

SECRET = os.getenv("SECRET", "")
if not SECRET or SECRET == "":
    raise ValueError("SECRET not set in environment")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# add scopes to oauth2_scheme if using scopes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={"": ""})

def create_access_token(data: dict[str, str | int | float | datetime], expires_delta: timedelta | None = None) -> str:
    """
       Creates an access token using the provided data and expiration delta.
    """
    if not SECRET:
        raise ValueError("SECRET not set in environment")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], conn: Connection) -> User:
    if not SECRET:
        raise ValueError("SECRET not set in environment")
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(conn, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    conn: Conn,
) -> Token:
    user = authenticate_user(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
