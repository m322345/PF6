from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{client_id}")
def return_pred(client_id: int):
    risk = 0.64
    status = "Yes"
    return {"client_id": client_id, "risk": risk, "state": status}