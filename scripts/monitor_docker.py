import docker
import json

# Ruta absoluta al archivo de configuración
config_file = "/ruta/absoluta/a/archivodocker.json"

try:
    # Carga la configuración
    with open(config_file, "r") as f:
        containers = json.load(f)

    # Conecta al cliente Docker
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    # Itera sobre cada contenedor y realiza la monitorización
    for container_info in containers:
        container_name = container_info["container_name"]
        alias = container_info["alias"]
        keywords = container_info["keywords"]

        try:
            container = client.containers.get(container_name)
            container_status = container.status

            if container_status == "running":
                print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=200,message=\"OK\"")
            else:
                print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=500,message=\"{container_status}\"")
        except docker.errors.NotFound:
            print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=404,message=\"Not Found\"")
        except docker.errors.DockerException as e:
            error_message = str(e).replace('"', '\\"')
            print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=500,message=\"{error_message}\"")
except Exception as e:
    print(f"Error al cargar el archivo de configuración: {e}")
