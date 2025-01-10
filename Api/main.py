from typing import Optional
from fastapi import FastAPI
import lightgbm as lgb
from lightgbm import LGBMClassifier
import pandas as pd
import pickle

app = FastAPI()
seuil = 0.54
model = pickle.load( open( "Data/Model/model.pkl", "rb" ) )
ClientsDatabase = pd.read_csv("Data/Db/ClientDatabase.csv")

@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{client_id}")
def return_pred(client_id: int):
    ClientsDatabaseList = list(ClientsDatabase['SK_ID_CURR'].unique())

    if client_id not in ClientsDatabaseList:
        return {"error": "Client inconnu de notre base"}
    else:
        X = ClientsDatabase[ClientsDatabase['SK_ID_CURR'] == client_id]
        X = X.drop(['SK_ID_CURR','TARGET'], axis=1)
        risk = model.predict_proba(X)[:, 1][0]
        #tauxRisk = risk
        if risk > seuil:
            status = "Refusé"
        else:
            status = "Accordée"
        return {"client_id": client_id, "risk": risk, "status": status}