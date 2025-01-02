from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}