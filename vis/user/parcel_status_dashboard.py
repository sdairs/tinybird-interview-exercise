import streamlit as st
import pandas as pd
import numpy as np
import requests

TOKEN = 'p.eyJ1IjogIjU2NTlmNjAxLThlY2MtNGM3Ny04M2IxLTQ2YTM5NzlmOGUyOCIsICJpZCI6ICI3YzRkN2QwNi1mMWZiLTQ3ZTYtYWQ0Yy0xNWZlZDdiODViMGYifQ.97zvFCQqrA1uLyWT6OUrFNvIEITse_l8uE1V4R4Jwu8'

# e1fdc9c3-42b9-4475-b49d-b23adbb9d8f4

params = {
    'token': TOKEN,
    'package_id': '0'
}

latest_status_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_latest_status.json'
status_history_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_status_history.json'

st.title('Track my parcel')

package_id = st.text_input(label="Enter you parcel ID here")
st.write('Searching for parcel: ', package_id)


@st.cache
def get_parcel_status(package_id):
    if package_id == '':
        return ""
    else:
        params = {
            'token': TOKEN,
            'package_id': package_id
        }
        status_response = requests.get(latest_status_api, params=params)
        status_response_json = status_response.json()
        status = status_response_json['data'][0]['status'].upper()
        status_updated_at = status_response_json['data'][0]['status_updated_at']
        return '''
        <p style="font-size: 50px;color: {colour};">{status}</p>
        <p style="font-size:20px;">{status_updated_at}</p>
        '''.format(colour='red' if status != 'DELIVERED' else 'green', status=status, status_updated_at=status_updated_at)


st.markdown(get_parcel_status(package_id), unsafe_allow_html=True)

st.subheader('History')


def get_parcel_history(package_id):

    if package_id == '':
        return ""
    else:
        params = {
            'token': TOKEN,
            'package_id': package_id
        }
    history_response = requests.get(status_history_api, params=params)
    history_response_json = history_response.json()
    data = pd.DataFrame(history_response_json['data'])
    return data


st.table(get_parcel_history(package_id))
