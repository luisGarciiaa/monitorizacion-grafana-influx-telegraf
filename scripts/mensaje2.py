import requests

url= "https://httpstat.us/403"
alias="prueba/403"
keywords = "frontend\,errorprueba"

try:
    response = requests.get(url, timeout=2)
    if response.status_code == 200:
        print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=200,message=\"OK\"")
    else:
        # Almacena el contenido de la respuesta en caso de error
        error_message = response.text.replace('"', '\\"')  # Escapa comillas en el mensaje
        print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code={response.status_code},message=\"{error_message}\"")
except requests.exceptions.Timeout:
    print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=408,message=\"Timeout\"")
except requests.exceptions.RequestException as e:
    # Almacena el mensaje de error en caso de que haya una excepción en la solicitud
    error_message = str(e).replace('"', '\\"')  # Escapa comillas en el mensaje
    print(f"http_response,url={url},source=url,nombre=\"{alias}\",keywords=\"{keywords}\" status_code=500,message=\"{error_message}\"")
