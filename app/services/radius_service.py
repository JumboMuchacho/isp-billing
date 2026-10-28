from app.core.config import get_settings


class RadiusService:
    def authorize(self, username: str) -> dict:
        settings = get_settings()
        return {
            "username": username,
            "host": settings.radius_host,
            "auth_port": settings.radius_auth_port,
            "decision": "access-accept",
        }

    def disconnect(self, username: str) -> dict:
        return {"username": username, "action": "disconnect", "status": "queued"}
