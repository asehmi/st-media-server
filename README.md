# FastAPI media server and stream client app example

    date: "2022-06-27"
    author:
        name: "Arvindra Sehmi"
        url: "https://www.linkedin.com/in/asehmi/"
        mail: "vin [at] thesehmis.com"
        avatar: "https://twitter.com/asehmi/profile_image?size=original"
    related: N/A

## Overview

This Streamlit app renders an image grid from images served from a simple `FastAPI` media server. The media server is started automatically from the Streamlit app on its own port and the same host as the Streamlit app.

### Demo app

![Demo](./images/st-media-server-demo.gif)

### Try the demo app yourself

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/asehmi/streamlit-label-studio-frontend/app.py)

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

Configure the server `HOST` and `PORT` in the server `toml` file (used by `media_server.py`) and in `.streamlit/secrets.toml` (used by `client_app.py`).

If you update the server `toml` whilst the client app is running, then restart/recycle the media server using the control provided in the client app.

# References

- [FastAPI](https://fastapi.tiangolo.com/)
- [Quickly Develop Highly Performant APIs with FastAPI & Python](https://livecodestream.dev/post/quickly-develop-highly-performant-apis-with-fastapi-python/)
- [Shutting down the uvicorn server master from a FastAPI worker](https://github.com/tiangolo/fastapi/issues/1509)

---

If you enjoyed this app, please consider starring this repository.

Thanks!

Arvindra