from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import admin, authentication, customers, mikrotik, packages, payments


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="BATMAN TECH Billing API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(authentication.router)
app.include_router(customers.router)
app.include_router(packages.router)
app.include_router(payments.router)
app.include_router(mikrotik.router)
app.include_router(admin.router)

app.mount("/portal", StaticFiles(directory="portal", html=True), name="portal")
app.mount("/admin-ui", StaticFiles(directory="admin", html=True), name="admin-ui")


@app.get("/")
def home():
    return {
        "business": "BATMAN TECH",
        "system": "Billing API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
