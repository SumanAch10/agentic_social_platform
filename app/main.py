# from routes import routes
from fastapi import FastAPI
from app.routes.auth_router import router as auth_router
from app.routes.post_router import router as post_router
from app.models import models
from app.db.db import Base,engine

app = FastAPI()
Base.metadata.create_all(bind = engine)

app.include_router(auth_router)
app.include_router(post_router)



