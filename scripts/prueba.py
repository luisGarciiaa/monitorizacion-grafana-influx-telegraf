import requests

#url = "http://example.com/api"#url = "https://jsonplaceholder.typicode.com/invalid_endpoint"
url = "https://httpstat.us/404"  # URL que genera un error 404 con un mensaje en HTML
url= "https://httpstat.us/403"
url = "https://httpstat.us/500"
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