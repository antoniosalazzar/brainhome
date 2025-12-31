from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, items

api_router = APIRouter()

# Incluir los routers de los endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])

@api_router.get("/ping")
async def ping():
    return {"pong": True}

