import streamlit as st
import pandas as pd
import requests
import shap
#import lightgbm as lgb
#from lightgbm import LGBMClassifier
from pathlib import Path
import pickle


def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}
    data_json = {'data': data}
    response = requests.request(method='GET', headers=headers, url=model_uri+'request/'+data)
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))
    return response.json()


def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


def visualize_importance(modele, id, donnees):
    """calcule la feature importance du modele"""
    X = DropColumns(donnees)
    prediction = lambda x: modele.predict_proba(x)[:, 1]
    moyennes = X.mean().values.reshape((1, X.shape[1]))
    explainer = shap.Explainer(prediction, moyennes)
    shap_values_single = explainer(Client(id,donnees), max_evals=1131)
    shap_values = explainer(X, max_evals=1417)
    return shap_values_single, shap_values


def DropColumns(dataset):
    """enleve """
    if 'SK_ID_CURR' in dataset.columns:
        dataset = dataset.drop(['SK_ID_CURR'], axis=1)
    if 'TARGET' in dataset.columns:
        dataset = dataset.drop(['TARGET'], axis=1)
    return dataset


def loadModel(modelPath):
    """retourne le modèle"""
    return pickle.load( open(modelPath, "rb" ) )


def Client(id,dataset):
    """retourne les informations du client"""
    return DropColumns(dataset.loc[dataset.SK_ID_CURR == id])


def set_state(i):
    st.session_state.etat = i


def main():
    #Url Api
    MODEL_URI = 'https://ocp7-api.onrender.com/'
    #fichier données
    pathDb = str(Path(__file__).parent)+'/../Api/Data/Db/'
    pathMod = str(Path(__file__).parent)+'/../Api/Data/Model/'
    ClientsDatabase = pd.read_csv(pathDb+'ClientDatabase.csv')
    ClientsList = ClientsDatabase['SK_ID_CURR'].tolist()
    if 'etat' not in st.session_state:
        st.session_state.etat = 0
    #Menu deroulant
    user_id = st.sidebar.selectbox('Recherche client',ClientsList)
    predict_btn = st.sidebar.button('Calcul du risque', on_click=set_state, args=[user_id])
    st.sidebar.divider()
    st.sidebar.page_link("https://www.ewd.fr/Formation/Data/P7/Drift_du_Modèle.html", label='Visualisation Data Drift')
    
    st.title('Calcul Risque d\'un Crédit')

    if st.session_state.etat != 0:
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
                    voirFeatureImpoLocale = st.button('Voir les raisons')

                    if voirFeatureImpoLocale:
                        model = loadModel(pathDb+'model.pkl')
                        shap_values_single, shap_values = visualize_importance(model, user_id, ClientsDatabase)
                        st_shap(shap.plots.waterfall(shap_values_single[0], max_display=10))
                        st_shap(shap.summary_plot(shap_values, max_display=10))

if __name__ == '__main__':
    main()