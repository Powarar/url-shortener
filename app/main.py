from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main_page():
    return {"data": "default"}