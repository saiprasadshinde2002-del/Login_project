from fastapi import FastAPI
from db.base import Base
from db.session import engine
from api.routes_auth import router as auth_router
from api.routes_users import router as users_router

app = FastAPI(title="FastAPI + Postgres + Celery")

# Create tables on startup (use Alembic in real projects)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
