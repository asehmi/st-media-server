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
echo "font = \"sans serif\""  >> ~/.streamlit/config.toml
echo "[runner]"  >> ~/.streamlit/config.toml
echo "fastReruns = false"  >> ~/.streamlit/config.toml
echo "MEDIA_SERVER_HOST = \"localhost\""  >> ~/.streamlit/secrets.toml
echo "MEDIA_SERVER_PORT = 8888"  >> ~/.streamlit/secrets.toml
