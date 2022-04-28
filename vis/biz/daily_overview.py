import streamlit as st
import pandas as pd
import numpy as np
import requests

TOKEN = 'p.eyJ1IjogIjU2NTlmNjAxLThlY2MtNGM3Ny04M2IxLTQ2YTM5NzlmOGUyOCIsICJpZCI6ICI3YzRkN2QwNi1mMWZiLTQ3ZTYtYWQ0Yy0xNWZlZDdiODViMGYifQ.97zvFCQqrA1uLyWT6OUrFNvIEITse_l8uE1V4R4Jwu8'


params = {
    'token': TOKEN
}

latest_status_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_latest_status.json'
delivered_count_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_delivered_count.json'
status_history_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_status_history.json'

st.title('Parcel Status Dashboard')

@st.cache
def get_delivered_count():
    delivered_count_response = requests.get(delivered_count_api, params=params)
    delivered_count_response_json = delivered_count_response.json()
    delivered_count = delivered_count_response_json['data'][0]['count()']
    return delivered_count

st.metric(label='Parcels Delivered', value=get_delivered_count())