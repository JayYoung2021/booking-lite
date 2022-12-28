from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import (
    user_router,
    room_router,
    order_router,
    token_router,
    admin_me_router,
    admin_router,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_me_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(order_router)
app.include_router(token_router)


@app.get("/")
def root():
    raise HTTPException(status_code=418, detail="I'm a teapot")
