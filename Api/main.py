from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{client}")
def read_item(item_id: int):
    risk = 0.64
    status = "Yes"
    return {"client": client, "risk": risk, "state": status}