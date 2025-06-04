from fastapi import FastAPI

app = FastAPI(title="twX")

@app.get("/")
async def root():
    return {"hello": "world"}
