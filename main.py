from fastapi import FastAPI, HTTPException

import models
from database import engine
from routers import routers_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routers_user.router)


@app.get("/")
def root():
    raise HTTPException(status_code=418, detail="I'm a teapot")
