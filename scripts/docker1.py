import docker

# Define las palabras clave asociadas al contenedor
target_container_name = "mongodb"
alias = "mongodb"
keywords = "docker\,real\,mongodb"

try:
    # Conecta al cliente Docker
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    # Intenta obtener el contenedor por su nombre
    container = client.containers.get(target_container_name)
    container_status = container.status

    if container_status == "running":
        print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=200,message=\"OK\"")
    else:
        print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=500,message=\"{container_status}\"")

except docker.errors.NotFound:
    # Si no se encuentra el contenedor
    print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=404,message=\"Not Found\"")

except docker.errors.DockerException as e:
    # Manejo de errores generales de Docker
    error_message = str(e).replace('"', '\\"')  # Escapa comillas en el mensaje
    print(f"http_response,nombre=\"{alias}\",source=docker,keywords=\"{keywords}\" status_code=500,message=\"{error_message}\"")
