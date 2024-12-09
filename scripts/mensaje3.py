import requests

#url = "https://httpstat.us/200?sleep=5000"
url = "http://localhost:27017/"
alias="mongodb"
keywords = "backend\,webserver\,real"

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

#CODIGO DE ABAJO PARA PRUEBAS CON TIPOS DE ERROR 
#DIFERENTES DEPENDIENDO DE LA URL

#url = "https://httpstat.us/404"  # URL que genera un error 404 con un mensaje en HTML
#url= "https://httpstat.us/403"
#url = "https://httpstat.us/500"
#url = "https://httpstat.us/200?sleep=5000"
'''
try:
    response = requests.get(url, timeout=1)  # Timeout de 3 segundos
    
    if response.status_code == 200:
        print("OK")
    else:
        # Si el código de estado no es 200, imprime el código y el contenido de la respuesta
        #print(f"Error: Código de estado {response.status_code}")
        print("Mensaje de error:", response.text)  # Imprime el contenido del mensaje de error

except requests.exceptions.Timeout:
    print("Timeout")
except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
'''
