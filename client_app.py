from itertools import cycle
import requests
import json
import time
import base64

import streamlit as st

import streamlit_debug
streamlit_debug.set(flag=False, wait_for_client=True, host='localhost', port=8765)

# --------------------------------------------------------------------------------
# Set Streamlit page style

st.set_page_config(layout='wide', initial_sidebar_state='auto')

from style import set_page_container_style, hide_streamlit_styles
set_page_container_style(
    max_width = 1100, max_width_100_percent = True,
    padding_top = 30, padding_right = 0, padding_left = 30, padding_bottom = 0,
    color = 'white', background_color = 'black',
)
#hide_streamlit_styles()

# --------------------------------------------------------------------------------

state = st.session_state

if 'MEDIA_SERVER_STARTED' not in state:
    state.MEDIA_SERVER_STARTED = False
if 'MEDIA_SOURCES' not in state:
    state.MEDIA_SOURCES = []
if 'MEDIA_SOURCE' not in state:
    state.MEDIA_SOURCE = None
if 'MEDIA_FILTER' not in state:
    state.MEDIA_FILTER = None
if 'MEDIA_LIST' not in state:
    state.MEDIA_LIST = []

# --------------------------------------------------------------------------------

MEDIA_SERVER_HOST = st.secrets['MEDIA_SERVER_HOST']
MEDIA_SERVER_PORT = st.secrets['MEDIA_SERVER_PORT']
BASE_URL = f'http://{MEDIA_SERVER_HOST}:{MEDIA_SERVER_PORT}'

# --------------------------------------------------------------------------------

def launch_media_server():

    if state.MEDIA_SERVER_STARTED:
        return

    import subprocess
    import threading

    def _run(job):
        print (f'\nRunning job: {job}\n')
        proc = subprocess.Popen(job)
        proc.wait()
        return proc

    job = ['python', 'media_server.py', MEDIA_SERVER_HOST, str(MEDIA_SERVER_PORT)]

    # server thread will remain active as long as streamlit thread is running, or is manually shutdown
    thread = threading.Thread(name='Media Server', target=_run, args=(job,), daemon=False)
    thread.start()

    time.sleep(5)
    state.MEDIA_SERVER_STARTED = True

    st.experimental_rerun()

if not state.MEDIA_SERVER_STARTED:
    launch_media_server()

# --------------------------------------------------------------------------------

@st.experimental_memo()
def get_media_sources():
    return json.loads(requests.get(f'{BASE_URL}/media_sources').text)['media_sources']

@st.experimental_memo()
def get_media_list(media_source='DEFAULT', media_filter=None):
    filter  = f'?filter={media_filter}' if media_filter else ''
    media_list_resp = json.loads(requests.get(f'{BASE_URL}/media_list/{media_source}{filter}').text)
    media_list = media_list_resp['media_list']
    media_filter = media_list_resp['media_filter']
    return media_list, media_filter

def initialize_media_resources():
    state.MEDIA_SOURCES = get_media_sources()
    if state.MEDIA_SOURCES:
        state.MEDIA_SOURCE = list(state.MEDIA_SOURCES.keys())[0]
        state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(media_source=state.MEDIA_SOURCE)

if state.MEDIA_SERVER_STARTED and (not state.MEDIA_SOURCE):
    initialize_media_resources()

# --------------------------------------------------------------------------------

@st.experimental_memo(show_spinner=False, max_entries=10000, ttl=3600)
def get_media_b64(source, media):
    media_bytes = requests.get(f'{BASE_URL}/media/{source}/{media}').content
    media_b64 = base64.b64encode(media_bytes).decode('utf-8')
    return media_b64

# --------------------------------------------------------------------------------

def _restart_media_server_cb():
    requests.get(f'{BASE_URL}/shutdown')
    state.MEDIA_SERVER_STARTED = False
    state.MEDIA_SOURCE = None
    state.MEDIA_FILTER = None
    get_media_sources.clear()
    get_media_list.clear()
    time.sleep(1)

def _set_media_source_cb():
    state.MEDIA_SOURCE = state['media_source']
    state.MEDIA_FILTER = None
    state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(media_source=state.MEDIA_SOURCE, media_filter=state.MEDIA_FILTER)

def _set_media_filter_cb():
    state.MEDIA_SOURCE = state['media_source']
    state.MEDIA_FILTER = state['media_filter']
    state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(media_source=state.MEDIA_SOURCE, media_filter=state.MEDIA_FILTER)

# --------------------------------------------------------------------------------

c1, c2, c3 = st.sidebar.columns([3,3,2])
c1.image('./images/app_logo.png')
c2.write('&nbsp;')
c2.image('./images/a12i_logo_grey.png')

st.sidebar.subheader('Settings')

with st.sidebar:
    with st.form(key='media_selection_form', clear_on_submit=False):
        state.MEDIA_SOURCE = st.selectbox(
            '✨ Select media source', 
            options=list(state.MEDIA_SOURCES.keys()),
            key='media_source'
        )
        if st.form_submit_button('Apply', on_click=_set_media_source_cb):
            st.experimental_rerun()

    with st.form(key='media_filter_form', clear_on_submit=False):
        state.MEDIA_FILTER = st.text_input('🔎 Filter media', state.MEDIA_FILTER, key='media_filter')
        if st.form_submit_button('Apply', on_click=_set_media_filter_cb):
            st.experimental_rerun()

num_cols = int(st.sidebar.number_input('Number columns', 1, 7, 5, 1))
img_w = int(st.sidebar.number_input('Image width', 50, 2000, 400, 10))
max_images = int(st.sidebar.number_input('Max images', 10, 2000, 1000, 100))

with st.sidebar.expander('⚙️ Media server'):
    st.button(
        '🌀 Restart',
        help='Be sure you really want to do this!',
        on_click=_restart_media_server_cb,
    )

media_list, _media_filter = get_media_list(media_source=state.MEDIA_SOURCE, media_filter=state.MEDIA_FILTER)
base_url = f'{BASE_URL}/media/{state.MEDIA_SOURCE}/' if not 'http' in media_list[0] else ''
images = {f'{base_url}{media}': media for media in media_list[:max_images]}

cols = cycle(st.columns(num_cols))
for img, caption in images.items():
    try:
        next(cols).image(img, width=img_w, output_format='auto', caption=caption)
    except:
        pass
