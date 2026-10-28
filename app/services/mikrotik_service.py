from app.core.config import get_settings


class MikrotikService:
    def _connect(self):
        settings = get_settings()
        if not settings.mikrotik_host:
            return None
        from librouteros import connect

        return connect(
            host=settings.mikrotik_host,
            username=settings.mikrotik_username,
            password=settings.mikrotik_password,
            port=settings.mikrotik_port,
        )

    def hotspot_users(self) -> list[dict]:
        api = self._connect()
        if api is None:
            settings = get_settings()
            return [{"host": settings.mikrotik_host, "port": settings.mikrotik_port, "users": []}]
        users = list(api.path("ip", "hotspot", "user"))
        api.close()
        return users

    def add_hotspot_user(self, username: str, password: str, profile: str) -> dict:
        api = self._connect()
        if api is None:
            return {"username": username, "profile": profile, "status": "queued"}
        api.path("ip", "hotspot", "user").add(name=username, password=password, profile=profile)
        api.close()
        return {"username": username, "profile": profile, "status": "created"}

    def remove_hotspot_user(self, username: str) -> dict:
        api = self._connect()
        if api is None:
            return {"username": username, "status": "queued"}
        for user in api.path("ip", "hotspot", "user").select("id", "name"):
            if user.get("name") == username:
                api.path("ip", "hotspot", "user").remove(user["id"])
        api.close()
        return {"username": username, "status": "removed"}
