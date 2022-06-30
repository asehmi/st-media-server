# FastAPI media server and Streamlit client app example

    date: "2022-06-30"
    author:
        name: "Arvindra Sehmi"
        url: "https://www.linkedin.com/in/asehmi/"
        mail: "vin [at] thesehmis.com"
        avatar: "https://twitter.com/asehmi/profile_image?size=original"
    related: https://github.com/asehmi/st-media-service is a similar pure Streamlit version of this application

## Overview

This Streamlit app renders an image grid from images served from a simple `FastAPI` media server. The media server is started automatically from the Streamlit app on its own port and the same host as the Streamlit app.

### Demo app

![Demo](./images/st-media-server-demo.gif)

### Try the demo app yourself

Clone the repo and run it locally. Launching FastAPI in Streamlit Cloud hasn't worked for me due to port binding issues, so instead use a hosting service that supports custom servers and ports, or build a Docker image. There are a few Streamlit Docker templates around if you search the Streamlit discussion forum.

To deploy on Heroku you must configure a `Procfile` and `setup.sh`, and separate the frontend and backend deployments.

However, if you prefer a monolithic pure Streamlit version of this application, then please see my [st-media-service](https://github.com/asehmi/st-media-service). (The really cool thing about FastAPI is that it's easy to rip it out leaving a Python object that can be used directly in a Python client application, which is how `st-media-service` came about.)

## Installation

```bash
$ cd st-media-server
$ pip install -r requirements.txt
```

## Usage

Run the included app to see how the Streamlit + FastAPI media server works:

```bash
$ streamlit run client_app.py
```

The demo client app is easily customised.

## Configuration

Media sources compatible with Streamlit's `st.image()` API are configured in `media_server.toml`. If this `toml` file isn't present the example `media_server.example.toml` is loaded instead. It should be obvious how to create your own server `toml` file. Note that two modes are supported, namely _local files_ (using the `media_folder` key) and _web links_ (using the `media_links` key). They are mutually exclusive and can't be intermixed.

Configure the server `CLOUD_HOST`, `LOCAL_HOST` and `PORT` in the server `toml` file (used by `media_server.py`) and the equivalents in `.streamlit/secrets.toml` (used by `client_app.py`). Note, set `RELEASE` to `false` in `.streamlit/secrets.toml` for local machine deployments of the client and server solution.

**.streamlit/secrets.toml**

```bash
# Set remote cloud hosted key to false for local machine deployments
REMOTE_CLOUD_HOSTED = false

# Assign the cloud host AFTER you know the deployment URL
# ( To deploy on Heroku you must configure a 'Procfile' and 'setup.sh',
#   and separate the frontend and backend deployments. Launching FastAPI in
#   Streamlit Cloud hasn't worked for me due to port binding issues. )
MEDIA_SERVER_CLOUD_HOST = '<user-repo-app-key>.herokuapp.com'
MEDIA_SERVER_LOCAL_HOST = 'localhost'
MEDIA_SERVER_PORT = 8888

MAX_NUM_IMAGES = 3000
DEFAULT_NUM_IMAGES = 1000

# presets = Number of columns, Pixel width presets
# default_index = index of default to start with
[DISPLAY_PRESETS]
presets = [
    '1, 2560',
    '2, 1280',
    '3, 850',
    '4, 640',
    '5, 512',
    '10, 256',
    '20, 128',
    '40, 64'
]
default_index = 4
```

**media_server.toml**

```bash
# Singular values come above the key group values below to prevent them combining

# Assign the cloud host AFTER you know the deployment URL
# ( To deploy on Heroku you must configure a 'Procfile' and 'setup.sh',
#   and separate the frontend and backend deployments. Launching FastAPI in
#   Streamlit Cloud hasn't worked for me due to port binding issues. )
CLOUD_HOST = '<user-repo-app-key>.herokuapp.com'
LOCAL_HOST = 'localhost'

PORT = 8888

MEDIA_TYPES = [
    'image/jpg',
    'image/jpeg',
    'image/png',
    'image/gif',
]

[MEDIA_SOURCES.'LOCAL 1']
media_folder = './images'
media_filter = 'unsplash'

[MEDIA_SOURCES.'LOCAL 2']
media_folder = './images'
media_filter = 'wallpaper'

[MEDIA_SOURCES.LINKS]
media_links = [
    'https://unsplash.com/photos/mOEqOtmuPG8/download?force=true&w=640',
    'https://unsplash.com/photos/g-krQzQo9mI/download?force=true&w=640',
    'https://unsplash.com/photos/Q6UehpkBSnQ/download?force=true&w=640',
    'https://unsplash.com/photos/iP8ElEhqHeY/download?force=true&w=640',
]
media_filter = 'unsplash'
```

If you update the media server `toml` whilst the client app is running, then restart/recycle the media server using the control provided in the client app.

# References

- [FastAPI](https://fastapi.tiangolo.com/)
- [Quickly Develop Highly Performant APIs with FastAPI & Python](https://livecodestream.dev/post/quickly-develop-highly-performant-apis-with-fastapi-python/)
- [Shutting down the uvicorn server master from a FastAPI worker](https://github.com/tiangolo/fastapi/issues/1509)

---

If you enjoyed this app, please consider starring this repository.

Thanks!

Arvindra