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

echo "REMOTE_CLOUD_HOSTED = true"  > ~/.streamlit/secrets.toml
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

echo "CLOUD_HOST = 'st-media-server.herokuapp.com'"  > ~/media_server.example.toml 
echo "LOCAL_HOST = 'localhost'"  >> ~/media_server.example.toml
echo "PORT = $PORT"  >> ~/media_server.example.toml
echo "MEDIA_TYPES = ["  >> ~/media_server.example.toml
echo "    'image/jpg',"  >> ~/media_server.example.toml
echo "    'image/jpeg',"  >> ~/media_server.example.toml
echo "    'image/png',"  >> ~/media_server.example.toml
echo "    'image/gif',"  >> ~/media_server.example.toml
echo "]"  >> ~/media_server.example.toml
echo "[MEDIA_SOURCES.'LOCAL 1']"  >> ~/media_server.example.toml
echo "media_folder = './images'"  >> ~/media_server.example.toml
echo "media_filter = 'unsplash'"  >> ~/media_server.example.toml
echo "[MEDIA_SOURCES.'LOCAL 2']"  >> ~/media_server.example.toml
echo "media_folder = './images'"  >> ~/media_server.example.toml
echo "media_filter = 'wallpaper'"  >> ~/media_server.example.toml
echo "[MEDIA_SOURCES.LINKS]"  >> ~/media_server.example.toml
echo "media_links = ["  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/mOEqOtmuPG8/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/g-krQzQo9mI/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/Q6UehpkBSnQ/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/iP8ElEhqHeY/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/q140lHKzXZY/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/Mxqvo8hhY1s/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/7_WyzplsaSE/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/fk50kc-DzSg/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/CFi7_hCXecU/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/Dymu1WiZVko/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/PHyF2mCMei0/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/ON6Xw8XEUQ8/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/D--HVF4qV0k/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/rn-0OotfzFA/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/tf3DfXxfvWE/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/aUkgcLurvQo/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/-IMlv9Jlb24/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/ESEnXckWlLY/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/mOcdke2ZQoE/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/GPPAjJicemU/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/JFeOy62yjXk/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/kEgJVDkQkbU/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/i9Q9bc-WgfE/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/tIL1v1jSoaY/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/-G3rw6Y02D0/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/xP_AGmeEa6s/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/4iTVoGYY7bM/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/mBQIfKlvowM/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/A-11N8ItHZo/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/kOqBCFsGTs8/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/8DMuvdp-vso/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/-YHSwy6uqvk/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/UC0HZdUitWY/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/kcA-c3f_3FE/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/eeqbbemH9-c/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/MqT0asuoIcU/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/ZuIDLSz3XLg/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/Mzy-OjtCI70/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/fdlZBWIP0aM/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "    'https://unsplash.com/photos/awj7sRviVXo/download?force=true&w=640',"  >> ~/media_server.example.toml
echo "]"  >> ~/media_server.example.toml
echo "media_filter = 'unsplash'"  >> ~/media_server.example.toml

