from typing import Optional
from fastapi import FastAPI
import pandas as pd
import pickle

app = FastAPI()

model = pickle.load( open( "Data/Model/model.pkl", "rb" ) )
ClientsDatabase = pd.read_csv("Data/Db/ClientDatabase.csv")
#fichierClientPp = pd.read_csv('../Data/Db/ClientDatabasePp.csv')

@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{client_id}")
def return_pred(client_id: int):
    ClientsDatabaseList = list(ClientsDatabase['SK_ID_CURR'].unique())

    if client_id not in ClientsDatabaseList:
        return {"error": "Client inconnu de notre base"}
    else:
        #X = ClientsDatabase[ClientsDatabase['SK_ID_CURR'] == client_id]
        #X = X.drop(['SK_ID_CURR'], axis=1)
        #risk = model.predict_proba(X)[:, 1]
        risk = 0.64
        status = "Accordée"
        return {"client_id": client_id, "risk": risk, "status": status}