from fastapi import FastAPI, Depends, APIRouter
from fastapi_plugin.fast_api_client import Auth0FastAPI
import os
import dotenv

router = APIRouter(prefix="/auth0")

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
_ = dotenv.load_dotenv(env_path)
AUTH_DOMAIN = os.getenv("AUTH0_DOMAIN")
if AUTH_DOMAIN is None:
    exit()
AUTH_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
if AUTH_AUDIENCE is None:
    exit()


auth0 = Auth0FastAPI(
    domain=AUTH_DOMAIN,
    audience=AUTH_AUDIENCE,
)

# General route structure - no auth needed
@router.get("/public")
async def public():
    return {"message": "Public"}

# Format for using protected routes - aka no scopes needed, but jwt claims are needed
@router.get("/protected")
async def protected(claims: dict[str, str | int | float] = Depends(auth0.require_auth())):
    return {"message": f"You are logged in as {claims.get("sub")}"}

# Format for using protected routes - aka jwt and specific scopes needed, in this case "read:messages"
@router.get("/scoped")
async def scoped(claims: dict[str, str | int | float] = Depends(auth0.require_auth(scopes="read:messages"))):
    return {"message": f"You are logged in as {claims.get("sub")} and have proper roles"}
