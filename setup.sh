mkdir -p ~/.streamlit/
echo "[general]"  > ~/.streamlit/credentials.toml
echo "email = \"vin@thesehmis.com\""  >> ~/.streamlit/credentials.toml
echo "[server]"  > ~/.streamlit/config.toml 
echo "headless = true"  >> ~/.streamlit/config.toml
echo "port = $PORT"  >> ~/.streamlit/config.toml
echo "enableCORS = true"  >> ~/.streamlit/config.toml
echo "[theme]"  >> ~/.streamlit/config.toml
echo "backgroundColor = \"black\""  >> ~/.streamlit/config.toml
echo "secondaryBackgroundColor = \"black\""  >> ~/.streamlit/config.toml
echo "textColor = \"#DCDCDC\""  >> ~/.streamlit/config.toml
echo "font = \"monospace\""  >> ~/.streamlit/config.toml
echo "[runner]"  >> ~/.streamlit/config.toml
echo "fastReruns = false"  >> ~/.streamlit/config.toml

echo "REMOTE_CLOUD_HOSTED = true"  >> ~/.streamlit/secrets.toml
echo "MEDIA_SERVER_CLOUD_HOST = 'st-media-server.herokuapp.com'"  >> ~/.streamlit/secrets.toml
echo "MEDIA_SERVER_LOCAL_HOST = 'localhost'"  >> ~/.streamlit/secrets.toml
echo "MEDIA_SERVER_PORT = $PORT"  >> ~/.streamlit/secrets.toml
echo "MAX_NUM_IMAGES = 3000"  >> ~/.streamlit/secrets.toml
echo "DEFAULT_NUM_IMAGES = 1000"  >> ~/.streamlit/secrets.toml
echo "[DISPLAY_PRESETS]"  >> ~/.streamlit/secrets.toml
echo "presets = ["  >> ~/.streamlit/secrets.toml
echo "    '1, 2560',"  >> ~/.streamlit/secrets.toml
echo "    '2, 1280',"  >> ~/.streamlit/secrets.toml
echo "    '3, 850',"  >> ~/.streamlit/secrets.toml
echo "    '4, 640',"  >> ~/.streamlit/secrets.toml
echo "    '5, 512',"  >> ~/.streamlit/secrets.toml
echo "    '10, 256',"  >> ~/.streamlit/secrets.toml
echo "    '20, 128',"  >> ~/.streamlit/secrets.toml
echo "    '40, 64'"  >> ~/.streamlit/secrets.toml
echo "]"  >> ~/.streamlit/secrets.toml
echo "default_index = 4"  >> ~/.streamlit/secrets.toml