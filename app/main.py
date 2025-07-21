# from routes import routes
from fastapi import FastAPI
from app.routes.auth_router import router
from app.models import models
from app.db.db import Base,engine

app = FastAPI()
Base.metadata.create_all(bind = engine)

app.include_router(router,prefix="/auth")


