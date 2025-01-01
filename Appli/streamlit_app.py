import streamlit as st
import pandas as pd
import requests

def request_prediction(model_uri, data):
    headers = {"Content-Type": "application/json"}
    data_json = {'data': data}
    response = requests.request(method='POST', headers=headers, url=model_uri, json=data_json)
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))
    return response.json()

def main():
    MODEL_URI = 'http://127.0.0.1:5000/invocations'

    user_id = st.sidebar.selectbox(
        'Recherche client',
        ['2332344', '234324325', '24344535'])
    st.title('Risque Faillite Credit')
#    longitude = st.number_input('Longitude du secteur',
#                                value=-119., step=1.)

    predict_btn = st.button('Calcul du risque')
    if predict_btn:
        data = [[user_id]]
        pred = request_prediction(MODEL_URI, data)[0]
        st.write(
            'le risque est de {:.2f}'.format(pred))

if __name__ == '__main__':
    main()