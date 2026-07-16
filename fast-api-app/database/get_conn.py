from fastapi import Request
from fastapi import Depends
from typing import Annotated
import psycopg

def get_connection(request: Request):
    with request.app.state.pool.connection() as conn:
        yield conn

Conn = Annotated[psycopg.Connection, Depends(get_connection)]
