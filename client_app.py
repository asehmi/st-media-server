import sys
import requests
import json
import time
import base64
from itertools import cycle

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
# hide_streamlit_styles()

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

if 'MEDIA_LIST_SORT' not in state:
    state.MEDIA_LIST_SORT = True
if 'MEDIA_LIST_DATE_SORT' not in state:
    state.MEDIA_LIST_DATE_SORT = True
if 'MEDIA_LIST_SORT_ASC' not in state:
    state.MEDIA_LIST_SORT_ASC = False

if 'NUM_IMAGES' not in state:
    state.NUM_IMAGES = int(st.secrets['DEFAULT_NUM_IMAGES'])
if 'NUM_COLS' not in state:
    state.NUM_COLS = 5
if 'IMG_W' not in state:
    state.IMG_W = 512

if 'USE_PRESET' not in state:
    state.USE_PRESET = True
if 'PRESETS' not in state:
    state.PRESETS = st.secrets['DISPLAY_PRESETS']['presets']
if 'PRESET_DEFAULT_INDEX' not in state:
    state.PRESET_DEFAULT_INDEX = st.secrets['DISPLAY_PRESETS']['default_index']

if 'SHOW_CAPTIONS' not in state:
    state.SHOW_CAPTIONS = False

# --------------------------------------------------------------------------------

MEDIA_SERVER_HOST = \
    st.secrets['MEDIA_SERVER_CLOUD_HOST'] if (
        st.secrets['REMOTE_CLOUD_HOSTED']
    ) else (
        st.secrets['MEDIA_SERVER_LOCAL_HOST']
    )
MEDIA_SERVER_PORT = st.secrets['MEDIA_SERVER_PORT']
HTTP_PROTOCOL = 'https' if st.secrets['REMOTE_CLOUD_HOSTED'] else 'http'
BASE_URL = f'{HTTP_PROTOCOL}://{MEDIA_SERVER_HOST}:{MEDIA_SERVER_PORT}'

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

    # Can use either of these job specs below

    # [1] sys.executable ensures we use the same Python environment that Streamlit is running under
    job = [f'{sys.executable}', 'media_server.py', MEDIA_SERVER_HOST, str(MEDIA_SERVER_PORT)]

    # [2] For Streamlit cloud I'm trying to run uvicorn directly to avoid importing uvicorn
    # in media_server.py which seemed to fail!
    # job = ['uvicorn', 'media_server:app', '--host', MEDIA_SERVER_HOST, '--port', str(MEDIA_SERVER_PORT)]

    # server thread will remain active as long as streamlit thread is running, or is manually shutdown
    thread = threading.Thread(name='Media Server', target=_run, args=(job,), daemon=False)
    thread.start()

    time.sleep(5)
    state.MEDIA_SERVER_STARTED = True

    st.experimental_rerun()

# If the FastAPI media server is remote hosted then we don't want to start it locally,
# But, we do want to say it is running!
if (not state.MEDIA_SERVER_STARTED) and (not st.secrets['REMOTE_CLOUD_HOSTED']):
    launch_media_server()
else:
    state.MEDIA_SERVER_STARTED = True

# --------------------------------------------------------------------------------

@st.experimental_memo()
def get_media_sources():
    return json.loads(requests.get(f'{BASE_URL}/media_sources').text)['media_sources']

@st.experimental_memo()
def get_media_list(
    media_source='DEFAULT', 
    media_filter=None, 
    sort_flag=False, 
    sort_by_date_flag=True, 
    ascending=False
):
    filter_param  = f'filter_string={media_filter}' if media_filter else ''
    sort_param  = f'sort_flag={sort_flag}'
    sort_by_date_param  = f'sort_by_date_flag={sort_by_date_flag}'
    ascending_param  = f'ascending={ascending}'
    params = f'{sort_param}&{sort_by_date_param}&{ascending_param}'
    params = f'{filter_param}&{params}' if filter_param else params
    media_list_resp = json.loads(requests.get(f'{BASE_URL}/media_list/{media_source}?{params}').text)
    media_list = media_list_resp['media_list']
    media_filter = media_list_resp['media_filter']
    return media_list, media_filter

def initialize_media_resources():
    state.MEDIA_SOURCES = get_media_sources()
    if state.MEDIA_SOURCES:
        state.MEDIA_SOURCE = list(state.MEDIA_SOURCES.keys())[0]
        state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(
            media_source=state.MEDIA_SOURCE,
            media_filter=None, 
            sort_flag=state.MEDIA_LIST_SORT,
            sort_by_date_flag=state.MEDIA_LIST_DATE_SORT,
            ascending=state.MEDIA_LIST_SORT_ASC
        )

if state.MEDIA_SERVER_STARTED and (not state.MEDIA_SOURCE):
    initialize_media_resources()

# --------------------------------------------------------------------------------

@st.experimental_memo(show_spinner=False, max_entries=10000, ttl=3600)
def get_media(source, media):
    media_bytes = requests.get(f'{BASE_URL}/media/{source}/{media}').content
    return media_bytes

@st.experimental_memo(show_spinner=False, max_entries=10000, ttl=3600)
def get_media_b64(source, media):
    media_bytes = requests.get(f'{BASE_URL}/media/{source}/{media}').content
    media_b64 = base64.b64encode(media_bytes).decode('utf-8')
    return media_b64

def get_media_full_path(source, media):
    media_full_path = json.loads(
        requests.get(f'{BASE_URL}/media_full_path/{source}/{media}').text
    )['media_full_path']
    return media_full_path

# --------------------------------------------------------------------------------

def _recycle_media_service_cb():
    requests.get(f'{BASE_URL}/shutdown')
    state.MEDIA_SERVER_STARTED = False
    state.MEDIA_SOURCE = None
    state.NUM_IMAGES = int(st.secrets['DEFAULT_NUM_IMAGES'])
    state.SHOW_CAPTIONS = False
    state.MEDIA_FILTER = None
    state.MEDIA_LIST_SORT = True
    state.MEDIA_LIST_DATE_SORT = True
    state.MEDIA_LIST_SORT_ASC = False
    get_media_sources.clear()
    get_media_list.clear()
    time.sleep(1)

def _set_media_source_cb():
    state.MEDIA_SOURCE = state['media_source']
    state.NUM_IMAGES = state['num_images']
    state.SHOW_CAPTIONS = state['show_captions']
    state.MEDIA_FILTER = None
    state.MEDIA_LIST_SORT = True
    state.MEDIA_LIST_DATE_SORT = True
    state.MEDIA_LIST_SORT_ASC = False
    state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(
        media_source=state.MEDIA_SOURCE, 
        media_filter=state.MEDIA_FILTER, 
        sort_flag=state.MEDIA_LIST_SORT,
        sort_by_date_flag=state.MEDIA_LIST_DATE_SORT,
        ascending=state.MEDIA_LIST_SORT_ASC
    )

def _set_media_controls_cb():
    state.MEDIA_SOURCE = state['media_source']
    state.MEDIA_FILTER = state['media_filter']
    state.MEDIA_LIST_SORT = state['media_list_sort']
    state.MEDIA_LIST_DATE_SORT = state['media_list_date_sort']
    state.MEDIA_LIST_SORT_ASC = state['media_list_sort_asc']
    state.MEDIA_LIST, state.MEDIA_FILTER = get_media_list(
        media_source=state.MEDIA_SOURCE, 
        media_filter=state.MEDIA_FILTER, 
        sort_flag=state.MEDIA_LIST_SORT,
        sort_by_date_flag=state.MEDIA_LIST_DATE_SORT,
        ascending=state.MEDIA_LIST_SORT_ASC
    )

# Prevents double clicking to make widget state stick
def _set_use_preset_cb():
    state.USE_PRESET = state['use_preset']

# Prevents double selecting to make widget state stick
def _set_preset_default_index_cb():
    state.PRESET_DEFAULT_INDEX = state.PRESETS.index(state['preset_choice'])
    # print(state.PRESET_DEFAULT_INDEX)

# --------------------------------------------------------------------------------

def main():
    c1, c2, c3 = st.sidebar.columns([3,3,2])
    c1.image('./images/app_logo.png')
    c2.write('&nbsp;')
    c2.image('./images/a12i_logo_grey.png')

    # NOTE: number_input widgets are sometimes prone to misinterpreting state values as float, so I force them to be int

    with st.sidebar:
        with st.form(key='media_selection_form', clear_on_submit=False):
            state.MEDIA_SOURCE = st.selectbox(
                '✨ Select media source', 
                options=list(state.MEDIA_SOURCES.keys()),
                key='media_source'
            )
            state.NUM_IMAGES = st.number_input(
                'Max images', 10, int(st.secrets['MAX_NUM_IMAGES']), int(state.NUM_IMAGES), 
                100, key='num_images')
            state.SHOW_CAPTIONS = st.checkbox('Captions', state.SHOW_CAPTIONS, key='show_captions')
            if st.form_submit_button('Apply', on_click=_set_media_source_cb):
                st.experimental_rerun()

        with st.expander('📅 Sort settings', expanded=False):
            with st.form(key='media_controls_form', clear_on_submit=False):
                state.MEDIA_FILTER = st.text_input('🔎 Filter keyword', state.MEDIA_FILTER, key='media_filter')
                c1, c2 = st.columns(2)
                state.MEDIA_LIST_SORT = c1.checkbox('Sort', state.MEDIA_LIST_SORT, key='media_list_sort')
                state.MEDIA_LIST_SORT_ASC = c2.checkbox('Ascending', state.MEDIA_LIST_SORT_ASC, disabled=(not state.MEDIA_LIST_SORT), key='media_list_sort_asc')
                state.MEDIA_LIST_DATE_SORT = c1.checkbox('By date', state.MEDIA_LIST_DATE_SORT, disabled=(not state.MEDIA_LIST_SORT), key='media_list_date_sort')
                st.caption('Sort by date and ascending only work if sort is enabled')
                if st.form_submit_button('Apply', on_click=_set_media_controls_cb):
                    st.experimental_rerun()

        with st.expander('👀 Layout settings', expanded=True):
            state.USE_PRESET = st.checkbox('Show presets', state.USE_PRESET, on_change=_set_use_preset_cb, key='use_preset')
            if state.USE_PRESET:
                preset_choice = st.selectbox(
                    'Choose a preset', options=state.PRESETS,
                    index=state.PRESET_DEFAULT_INDEX,
                    on_change=_set_preset_default_index_cb,
                    help='Number of columns and image width',
                    key='preset_choice'
                )
                state.NUM_COLS = int(preset_choice.split(',')[0])
                state.IMG_W = int(preset_choice.split(',')[1])
            else:
                state.NUM_COLS = st.number_input('Number columns', 1, 80, int(state.NUM_COLS), 1)
                state.IMG_W = st.number_input('Image width', 32, 3200, int(state.IMG_W), 32)

        if (state.MEDIA_SERVER_STARTED) and (not st.secrets['REMOTE_CLOUD_HOSTED']):
            with st.expander('🌀 Recycle media server'):
                st.caption('Use this to reload external media config (toml) file changes')
                st.button(
                    'Recycle',
                    help='Be sure you really want to do this!',
                    on_click=_recycle_media_service_cb,
                )

    media_list, _media_filter = get_media_list(
        media_source=state.MEDIA_SOURCE,
        media_filter=state.MEDIA_FILTER,
        sort_flag=state.MEDIA_LIST_SORT,
        sort_by_date_flag=state.MEDIA_LIST_DATE_SORT,
        ascending=state.MEDIA_LIST_SORT_ASC
    )
    images = {media: media for media in media_list[:int(state.NUM_IMAGES)]}

    cols = cycle(st.columns(int(state.NUM_COLS)))
    for img, caption in images.items():
        if not 'http' in img:
            image_bytes = get_media(source=state.MEDIA_SOURCE, media=img)
            image = image_bytes
        else:
            image = img

        try:
            if state.SHOW_CAPTIONS:
                next(cols).image(image, width=int(state.IMG_W), output_format='auto', caption=caption)
            else:
                next(cols).image(image, width=int(state.IMG_W), output_format='auto')
        except Exception as ex:
            print(f'Skipping {caption}\n', str(ex))
            pass

# -----------------------------------------------------------------------------

def about():
    st.sidebar.markdown('---')
    st.sidebar.info('''
        (c) 2022. CloudOpti Ltd. All rights reserved.
        
        [GitHub repo](https://github.com/asehmi/st-media-server)
    ''')

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    about()
