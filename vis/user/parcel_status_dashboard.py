from uuid import UUID
import streamlit as st
import pandas as pd
import requests
from time import perf_counter

# TINYBIRD CONFIG ---
TOKEN = 'p.eyJ1IjogIjU2NTlmNjAxLThlY2MtNGM3Ny04M2IxLTQ2YTM5NzlmOGUyOCIsICJpZCI6ICI3YzRkN2QwNi1mMWZiLTQ3ZTYtYWQ0Yy0xNWZlZDdiODViMGYifQ.97zvFCQqrA1uLyWT6OUrFNvIEITse_l8uE1V4R4Jwu8'

latest_status_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_latest_status.json'
status_history_api = 'https://api.tinybird.co/v0/pipes/parcel_tracking_status_history.json'

# HELPER FUNCTIONS ---


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

# STREAMLIT ---

# Sample UUID
# e1fdc9c3-42b9-4475-b49d-b23adbb9d8f4


st.set_page_config(page_title='Track Your Parcel - ACME Shipping', page_icon='images/acme_favico.png',
                   layout="centered", initial_sidebar_state="auto", menu_items=None)


def local_css(file_name):
    # Hack to load custom CSS in Streamlit
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("css/style.css")

# Page Header
st.image('images/acme_shipping_white.png')

st.title('Track Your Parcel')

# Parcel Tracking Section
tracking_code_container = st.container()

# Initialization
if 'valid_input' not in st.session_state:
    st.session_state['valid_input'] = False

print(st.session_state['valid_input'])


def track_button_click(package_id):
    # When the TRACK button is clicked, we validate that the Input was a valid uuid4
    # We store the result in SESSION STATE as this persists for the duration of the session
    if is_valid_uuid(package_id):
        st.session_state['valid_input'] = True
    else:
        st.session_state['valid_input'] = False


# Provides the tracking code Input box & TRACK button
with tracking_code_container:
    st.header('Enter your tracking code here')
    package_id = st.text_input(
        label='', max_chars=36, help='Your tracking code is located on your shipping receipt. It looks like "e1fdc9c3-42b9-4475-b49d-b23adbb9d8f4"',
        placeholder='Tracking code')
    st.button('Track', on_click=track_button_click,
              kwargs={'package_id': package_id})


@st.cache
def get_parcel_status(package_id):
    # Hit the Tinybird API to get the status of a parcel by id
    params = {
        'token': TOKEN,
        'package_id': package_id
    }
    start_time = perf_counter()
    status_response = requests.get(latest_status_api, params=params)
    end_time = perf_counter()
    print("Response in: {elapsed}".format(elapsed=end_time-start_time))
    status_response_json = status_response.json()
    status = status_response_json['data'][0]['status'].upper()
    status_updated_at = status_response_json['data'][0]['status_updated_at']
    return {
        'status': status,
        'status_updated_at': status_updated_at
    }
    
#  '''
# <p style="font-size: 50px;color: {colour};">{status}</p>
# <p style="font-size:20px;">{status_updated_at}</p>
# '''.format(colour='red' if status != 'DELIVERED' else 'green', status=status, status_updated_at=status_updated_at)


def get_parcel_history(package_id):
    # Hit the Tinybird API to get the full history of a parcel
    params = {
        'token': TOKEN,
        'package_id': package_id
    }
    start_time = perf_counter()
    history_response = requests.get(status_history_api, params=params)
    end_time = perf_counter()
    print("Response in: {elapsed}".format(elapsed=end_time-start_time))
    history_response_json = history_response.json()
    data = pd.DataFrame(history_response_json['data'])
    data.columns = ['Status','Time']
    data['Status'] = data['Status'].replace('_', ' ', regex=True)
    data['Status'] = data['Status'].str.upper()
    return data


if st.session_state['valid_input']:
    response_container = st.container()
    with response_container:
        parcel_status_container = st.container()
        with parcel_status_container:
            status = get_parcel_status(package_id)
            st.header("Parcel Status")
            status_col1,status_col2 = st.columns(2)
            with status_col1:
                st.text(status['status'])
            with status_col2:
                st.text(status['status_updated_at'])
            # st.markdown(, unsafe_allow_html=True)
        with st.expander("Show parcel history"):
            st.subheader('History')
            st.table(get_parcel_history(package_id))
