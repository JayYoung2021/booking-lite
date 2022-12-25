from fastapi import FastAPI, HTTPException

import models
from database import engine
from routers import user_router, room_router, order_router, token_router, user_me_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(room_router)
app.include_router(order_router)
app.include_router(token_router)
app.include_router(user_me_router)


@app.get("/")
def root():
    raise HTTPException(status_code=418, detail="I'm a teapot")
