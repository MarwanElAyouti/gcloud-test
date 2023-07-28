from fastapi import APIRouter, Depends

from friendlyeats.routers.rating import router as rating_router
from friendlyeats.routers.restaurant import router as restaurant_router
from friendlyeats.services.jwt import get_auth_user

router = APIRouter()

router.include_router(restaurant_router)
router.include_router(rating_router)


@router.get("/health")
async def health():
    return {"status": "success"}


@router.get("/test_jwt")
async def test_jwt(user: dict = Depends(get_auth_user)):
    return {"status": "Authentication Passed"}
