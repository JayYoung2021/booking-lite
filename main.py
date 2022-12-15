from fastapi import FastAPI, HTTPException

from routers import *

app = FastAPI()
app.include_router(routers_user.router)
app.include_router(routers_room.router)


@app.get("/")
def root():
    raise HTTPException(status_code=418, detail="I'm a teapot")
