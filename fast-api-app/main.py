from fastapi import FastAPI, Request, Response
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from collections.abc import Awaitable, Callable
import os
import dotenv


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
_ = dotenv.load_dotenv(env_path)

APP_BASE_URL = os.getenv("API_BASE_URL")
# Uncomment if using auth0
# from auth.auth_providers.auth0 import router as auth0_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncConnectionPool("") as pool:
        app.state.pool = pool
        yield


app = FastAPI(lifespan=lifespan, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://{APP_BASE_URL}.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    response = await call_next(request)
    # Force HTTPS
    # Add any other headers or security measures
    response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    return response

# Uncomment if using auth0
# app.include_router(auth0_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
