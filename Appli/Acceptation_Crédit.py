import streamlit as st
import pandas as pd
import requests
import shap
#import lightgbm as lgb
#from lightgbm import LGBMClassifier
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
    pathDb = str(Path(__file__).parent)+'/../Api/Data/Db/'
    pathMod = str(Path(__file__).parent)+'/../Api/Data/Model/'
    ClientsDatabase = pd.read_csv(pathDb+'ClientDatabase.csv')
    ClientsList = ClientsDatabase['SK_ID_CURR'].tolist()
    #Menu deroulant
    user_id = st.sidebar.selectbox('Recherche client',ClientsList)
    predict_btn = st.sidebar.button('Calcul du risque')
    st.sidebar.divider()
    st.sidebar.page_link("https://www.ewd.fr/Formation/Data/P7/Drift_du_Modèle.html", label='Visualisation Data Drift')
    
    st.title('Calcul Risque d\'un Crédit')

    if predict_btn:
        with st.spinner("Merci de patienter l\'api est en cours de démarrage... "):
            pred = request_prediction(MODEL_URI, str(user_id))
            if type(pred) == dict:
                if "error" in pred:
                    st.write(f"")
                    st.write(f"Erreur {pred['error']}")
                else:
                    st.write(f"")
                    st.write(f"Prédiction de risque de faillite pour le client {pred['client_id']}")
                    st.write(f"le risque d'impayés est de {pred['risk']:.2f}")
                    st.write(f"La demande de crédit est {pred['status']}")
                    voirFeatureImpoLocale = st.button('Voir les riasons')

    if voirFeatureImpoLocale:
        shap.plots.waterfall(shap_values[0], max_display=14)

if __name__ == '__main__':
    main()