import requests
import json

# Ruta absoluta al archivo de configuración
config_file = "/ruta/absoluta/a/archivo.json"

try:
    # Carga la configuración
    with open(config_file, "r") as f:
        services = json.load(f)

    # Itera sobre cada servicio y realiza la monitorización
    for service in services:
        url = service["url"]
        alias = service["alias"]
        keywords = service["keywords"]

        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=200,message=\"OK\"")
            else:
                error_message = response.text.replace('"', '\\"')
                print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code={response.status_code},message=\"{error_message}\"")
        except requests.exceptions.Timeout:
            print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=408,message=\"Timeout\"")
        except requests.exceptions.RequestException as e:
            error_message = str(e).replace('"', '\\"')
            print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=500,message=\"{error_message}\"")
except Exception as e:
    print(f"Error al cargar el archivo de configuración: {e}")
