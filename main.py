from fastapi import FastAPI, HTTPException

from routers import routers_user

app = FastAPI()
app.include_router(routers_user.router)


@app.get("/")
def root():
    raise HTTPException(status_code=418, detail="I'm a teapot")
