import streamlit as st
import pandas as pd
import requests
from pathlib import Path

def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}
    data_json = {'data': data}
    response = requests.request(method='GET', headers=headers, url=model_uri+'request/'+data)
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))
    return response.json()

def main():
    #Url Api
    MODEL_URI = 'https://ocp7-api.onrender.com/'
    #fichier données
    pathData = str(Path(__file__).parent)+'/Data/'
    ClientsDatabase = pd.read_csv(pathData+'ClientsDatabase.csv')
    ClientsList = ClientsDatabase['SK_ID_CURR'].tolist()
    #Menu deroulant
    user_id = st.sidebar.selectbox('Recherche client',ClientsList)
    predict_btn = st.sidebar.button('Calcul du risque')
    st.title('Risque de Faillite d\'un Crédit')

    if predict_btn:
        with st.spinner("waiting"):
            pred = request_prediction(MODEL_URI, str(user_id))
            if type(pred) == dict:
                st.write(f"Prédiction pour le client {pred['client_id']}")
                st.write(f"le risque d'impayés est de {pred['risk']:.2f}")
                st.write(f"La demande de crédit est {pred['status']}")

if __name__ == '__main__':
    main()