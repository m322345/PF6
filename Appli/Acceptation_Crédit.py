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
        pred = request_prediction(MODEL_URI, str(user_id))
        st.write(pred)
#        st.write(
#            'le risque est de {:.2f}'.format(pred))

if __name__ == '__main__':
    main()