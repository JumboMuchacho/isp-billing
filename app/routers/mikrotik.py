from fastapi import APIRouter
from pydantic import BaseModel

from app.services.mikrotik_service import MikrotikService

router = APIRouter(prefix="/mikrotik", tags=["mikrotik"])
mikrotik = MikrotikService()


class HotspotUserCreate(BaseModel):
    username: str
    password: str
    profile: str


@router.get("/users")
def list_hotspot_users():
    return mikrotik.hotspot_users()


@router.post("/users")
def create_hotspot_user(payload: HotspotUserCreate):
    return mikrotik.add_hotspot_user(payload.username, payload.password, payload.profile)
