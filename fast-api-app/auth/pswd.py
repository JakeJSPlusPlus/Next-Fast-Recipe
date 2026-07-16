from psycopg.rows import class_row
from pwdlib import PasswordHash
import os
import dotenv
import psycopg
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from fastapi import Request, Depends
from typing import Annotated

from database.get_conn import Conn


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    password: str



"""
  Set PEPPER in .env (Optional)
  Set SECRET in .env (openssl rand -hex 32)

"""

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
_ = dotenv.load_dotenv(env_path)

PEPPER = os.getenv("PEPPER")



password_hash = PasswordHash.recommended()

def verify_password(password: str, hash: str) -> bool:
    if PEPPER is None:
        return password_hash.verify(password, hash)
    return password_hash.verify(password + PEPPER, hash)

def get_password_hash(password: str) -> str:
    if PEPPER is None:
        return password_hash.hash(password)
    return password_hash.hash(password + PEPPER)

def get_user(conn: psycopg.Connection, username: str | None) -> User | None:
    with conn.cursor(row_factory=class_row(User)) as cur:
        _ = cur.execute("SELECT * FROM users WHERE username = %s", (username))
        if cur.rowcount == 0:
            return None
        return cur.fetchone()

def authenticate_user(conn: psycopg.Connection, username: str, password: str) -> User | None:
    user = get_user(conn, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user




if __name__ == "__main__":
    print(env_path)
