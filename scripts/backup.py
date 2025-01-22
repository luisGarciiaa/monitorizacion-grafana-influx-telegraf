import os
import requests
import zipfile
from datetime import datetime

# Configuración general, al final del script, modificar periodo, granularidad y bucket
INFLUX_URL = "http://localhost:8086/api/v2/query"  # Cambia según tu configuración
INFLUX_TOKEN = "" #actualiza tu token
ORG = "" #actualiza tu organizacion
EXPORT_DIR = "./backups" #modifica a tu ruta destino

def query_influx(bucket, query):
    """Ejecuta una consulta en InfluxDB y devuelve los resultados."""
    print(f"Ejecutando consulta para bucket '{bucket}':\n{query}")  # Depuración de la consulta
    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",
        "Content-Type": "application/vnd.flux",
        "Accept": "application/csv"  # Asegúrate de recibir los datos en formato legible
    }
    params = {"org": ORG}  # Añade el parámetro org aquí
    response = requests.post(INFLUX_URL, headers=headers, params=params, data=query)
    if response.status_code != 200:
        print(f"Error en la consulta: {response.text}")  # Depuración en caso de error
        raise Exception(f"Error al consultar InfluxDB: {response.text}")
    print(f"Resultado de la consulta:\n{response.text[:500]}")  # Muestra los primeros 500 caracteres del resultado
    return response.text


def get_unique_hosts(bucket):
    """Obtiene todos los hosts únicos del bucket."""
    query = f'''
        from(bucket: "{bucket}")
          |> range(start: -30d)
          |> filter(fn: (r) => exists r["host"])
          |> keep(columns: ["host"])
          |> group()
          |> distinct(column: "host")
    '''
    result = query_influx(bucket, query)
    print("Resultado de la consulta para obtener hosts únicos:\n", result)  # Para depuración

    # Procesa el resultado correctamente
    hosts = []
    for line in result.split("\n")[1:]:  # Omite la cabecera
        columns = line.split(",")
        if len(columns) > 3:  # Verifica que haya suficientes columnas
            hosts.append(columns[3].strip())  # Limpia espacios en el valor
    print(f"Hosts únicos encontrados: {hosts}")  # Depuración de los hosts encontrados
    return hosts


def save_to_zip(data, filename):
    """Guarda los datos en un archivo ZIP, incluyendo la fecha en los nombres de los archivos CSV."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    zip_path = os.path.join(EXPORT_DIR, filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Fecha y hora actual
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for name, content in data.items():
            # Agregar la fecha al nombre del archivo CSV
            csv_filename = f"{name}_{timestamp}.csv"
            file_path = os.path.join(EXPORT_DIR, csv_filename)
            
            # Escribir contenido en el archivo CSV
            with open(file_path, 'w') as f:
                f.write(content)
            
            # Añadir el archivo CSV al ZIP
            zf.write(file_path, os.path.basename(file_path))
            
            # Eliminar el archivo temporal
            os.remove(file_path)
    return zip_path



def export_backup(bucket, period, granularity):
    """Exporta datos históricos de CPU, memoria, disco, estado de servicios y Docker y los guarda en un ZIP."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"backup_{timestamp}.zip"
    all_hosts = get_unique_hosts(bucket)

    print(f"Hosts encontrados en el bucket '{bucket}': {all_hosts}")
    
    queries = {}
    for host in all_hosts:
        # Consulta para CPU
        queries[f"cpu_{host}"] = f'''from(bucket: "{bucket}")
          |> range(start: -{period})
          |> filter(fn: (r) => r["host"] == "{host}")
          |> filter(fn: (r) => r["cpu"] == "cpu-total")
          |> filter(fn: (r) => r["_field"] == "usage_idle")
          |> aggregateWindow(every: {granularity}, fn: mean, createEmpty: false)
          |> map(fn: (r) => ({{
                r with _value: 100.0 - r._value
            }}))
          |> keep(columns: ["_time", "_value", "_measurement", "host"])
          |> yield(name: "mean")'''

        # Consulta para memoria
        queries[f"mem_{host}"] = f'''from(bucket: "{bucket}")
          |> range(start: -{period})
          |> filter(fn: (r) => r["_measurement"] == "mem")
          |> filter(fn: (r) => r["_field"] == "free" or r["_field"] == "used")
          |> filter(fn: (r) => r["host"] == "{host}")
          |> aggregateWindow(every: {granularity}, fn: mean, createEmpty: false)
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
                _time: r._time,
                _value: float(v: r["used"]) / (float(v: r["free"]) + float(v: r["used"])) * 100.0,
                host: r.host
            }}))
          |> keep(columns: ["_time", "_value", "_measurement", "host"])
          |> yield(name: "mean")'''

        # Consulta para disco
        queries[f"disk_{host}"] = f'''from(bucket: "{bucket}")
          |> range(start: -{period})
          |> filter(fn: (r) => r["_measurement"] == "disk")
          |> filter(fn: (r) => r["_field"] == "used" or r["_field"] == "free")
          |> filter(fn: (r) => r["host"] == "{host}")
          |> aggregateWindow(every: {granularity}, fn: sum, createEmpty: false)
          |> group(columns: ["host"])
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
                _time: r._time,
                _value: float(v: r["used"]) / (float(v: r["used"]) + float(v: r["free"])) * 100.0,
                host: r.host
            }}))
          |> keep(columns: ["_time", "_value", "host"])
          |> yield(name: "mean")'''

    # Consulta para servicios (serie temporal)
    queries["services"] = f'''from(bucket: "{bucket}")
          |> range(start: -{period})
          |> filter(fn: (r) => r["_measurement"] == "servicio_gen")
          |> filter(fn: (r) => r["_field"] == "status_code")
          |> aggregateWindow(every: {granularity}, fn: last, createEmpty: false)
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> keep(columns: ["_time", "url", "status_code"])
          |> yield(name: "time_series")'''

    # Consulta para Docker (serie temporal)
    queries["docker"] = f'''from(bucket: "{bucket}")
          |> range(start: -{period})
          |> filter(fn: (r) => r["_measurement"] == "docker_gen")
          |> filter(fn: (r) => r["_field"] == "status_code")
          |> aggregateWindow(every: {granularity}, fn: last, createEmpty: false)
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> keep(columns: ["_time", "nombre", "status_code"])
          |> yield(name: "docker_time_series")'''

    results = {}
    for query_name, query in queries.items():
        print(f"Exportando datos para: {query_name}")  # Depuración
        results[query_name] = query_influx(bucket, query)
        print(f"Datos obtenidos para {query_name}: {results[query_name][:500]}")  # Muestra los primeros 500 caracteres

    # Guardar resultados en un archivo ZIP
    zip_path = save_to_zip(results, zip_filename)
    print(f"Backup guardado en: {zip_path}")


# Ejecuta el script
if __name__ == "__main__":
    # Parámetros configurables
    bucket = "nuevoBucket"  # escoge el nombre de tu bucket
    period = "2d"  # periodo desde el cual hacer el backup
    granularity = "1h"  # Media cada 1 hora
    export_backup(bucket, period, granularity)
