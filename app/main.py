from fastapi import FastAPI
from app.routers import router

app = FastAPI(title="twX")


@app.get("/")
async def root():
    return {"hello": "world"}


app.include_router(router)
