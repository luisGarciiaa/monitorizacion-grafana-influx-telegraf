# Guía de Instalación y Configuración del Sistema de Monitorización (Influxdb_v2, Telegraf y Grafana)
---
# 1.Guía de Instalación y Configuración de InfluxDB v2

## Descripción General
Esta guía detalla los pasos para instalar y configurar **InfluxDB v2** en servidores Linux usando binarios. InfluxDB v2 se utilizará para almacenar las métricas recolectadas por Telegraf y permitirá la visualización de los datos en Grafana.

---

## 1. Instalación de InfluxDB v2

### Requisitos
- **Sistema Operativo**: Linux (64 bits). Para servidores de 32 bits o con otra arquitectura, consulta la página oficial de [InfluxData Downloads](https://portal.influxdata.com/downloads) para descargar la versión adecuada.

### Pasos de Instalación

1. **Descargar el archivo binario de InfluxDB v2**: 

    ```bash
    wget https://download.influxdata.com/influxdb/releases/influxdb2-2.7.10_linux_amd64.tar.gz
    ```


2. **Descomprimir el archivo descargado**:

    ```bash
    tar xvfz influxdb2-2.7.10_linux_amd64.tar.gz
    ```

    Esto crea una carpeta llamada `influxdb2-2.7.10` que contiene los binarios de InfluxDB. Navega a `influxdb2-2.7.10/usr/bin` y podrás ver el ejecutable `influxd`.

3. **Iniciar el servidor de InfluxDB**:

    ```bash
    cd influxdb2-2.7.10/usr/bin
    ./influxd
    ```

    InfluxDB se iniciará en el puerto `8086`. Puedes verificar su funcionamiento accediendo a [http://localhost:8086](http://localhost:8086) desde un navegador web. Puedes cancelar la ejecucion con ctrl + C.


---

## 2. Configuración Inicial
### **A. Escritorio con Navegador Web**

1. **Abrir la Interfaz de Configuración**: Accede a [http://localhost:8086](http://localhost:8086) en un navegador.

2. **Crear Usuario Administrador y Configuración Inicial**:

    - **Nombre de usuario**: Elige un nombre de usuario personalizado.
    - **Contraseña**: Configura una contraseña segura de tu elección.
    - **Organización**: Introduce un nombre descriptivo, como `MiOrganización`.
    - **Bucket**: Especifica un nombre para el bucket principal, como `MiBucket`.

---

Esta configuración inicial solo se realiza la primera vez que inicias InfluxDB v2. Después de configurar estos valores, podrás acceder a InfluxDB utilizando el nombre de usuario y la contraseña que hayas definido.


3. **Completar la Configuración**: Haz clic en **Continuar** para finalizar la configuración inicial.

---

## 3. Configuración de API y Token de Acceso

Para permitir la conexión desde Telegraf u otras aplicaciones externas, necesitas un token de acceso.

1. Dirígete a **Data > Tokens** en la interfaz de InfluxDB.
2. **Crear un nuevo token** para tu organización. Guarda este token en un lugar seguro, ya que será necesario para las conexiones externas.

---

## 4. Configuración de Retención de Datos

1. Navega a **Data > Buckets** en la interfaz de InfluxDB.
2. Selecciona el bucket que creaste durante la configuración inicial (ej. `MiBucket`).
3. Ajusta la **Retención de Datos** según sea necesario, por ejemplo, 30 días o 90 días, dependiendo de tus requisitos.

---

## 5. Comprobación de la IP del Servidor y Preparación para la Conexión Externa de Telegraf

Para que otros servidores puedan enviar métricas a este servidor InfluxDB desde Telegraf, sigue estos pasos:

1. **Comprobar la IP del Servidor**:
   - Ejecuta el siguiente comando para obtener la dirección IP de la máquina donde está corriendo InfluxDB:
   
     ```bash
     hostname -I
     ```
   
   - Apunta la dirección IP obtenida, ya que la necesitarás para configurarla en los agentes Telegraf externos.

2. **Anotar Parámetros para Telegraf Externo**:
   - Anota los siguientes valores, ya que serán necesarios para configurar la conexión de Telegraf en los servidores externos:
     - **IP del Servidor InfluxDB**: La dirección IP obtenida en el paso anterior.
     - **Bucket**: El bucket donde deseas almacenar las métricas, por ejemplo, `MiBucket`.
     - **Token**: El token de autenticación para InfluxDB.
     - **Organización**: La organización configurada, como `MiOrganización`.

3. **Ejemplo de Configuración de Telegraf Externo(no hace falta configurar esto ahora)**:
   - En el siguiente apartado instalaremos telegraf en los servidores y escribiremos algo asi para configurar el destino de las metricas. Por lo que debes guardar la informacion.

     ```ini
     [[outputs.influxdb_v2]]
       urls = ["http://<IP_DEL_SERVIDOR_INFLUXDB>:8086"]
       token = "<mi_token>"
       organization = "<MiOrganización>"
       bucket = "<MiBucket>"
     ```


--- 


### B. Servidores sin Entorno Gráfico

#### 1. Descargar e Instalar el Cliente CLI

El cliente CLI de InfluxDB no se incluye en el paquete principal y debe descargarse por separado. Sigue estos pasos:

1. **Descargar el paquete del cliente CLI de InfluxDB**:
   ```bash
   wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-amd64.tar.gz
   ```

2. **Descomprimir el archivo descargado**:
   ```bash
   tar xvfz influxdb2-client-2.7.5-linux-amd64.tar.gz
   ```

3. **Mover el binario `influx` a un directorio incluido en tu variable `PATH`**:
   ```bash
   sudo mv influx /usr/local/bin/
   ```

4. **Verificar la instalación del cliente CLI**:
   ```bash
   influx version
   ```

Esto confirmará que el cliente CLI se instaló correctamente.

---

#### 2. Iniciar el servidor de InfluxDB

Ejecuta el siguiente comando para iniciar InfluxDB en el servidor: Este paso es necesario para poder configurar influxdb y que la CLI pueda comunicarse con influxdb

```bash
cd influxdb2-2.7.10/usr/bin
./influxd &
```

InfluxDB se ejecutará en el puerto `8086` por defecto. Deja este proceso corriendo en segundo plano(&) o abre otra terminal mientras este corre.

---

#### 3. Configuración Inicial mediante CLI

El cliente CLI de InfluxDB (`influx`) te permite realizar la configuración inicial sin necesidad de un navegador web. Sigue estos pasos:

1. **Acceder al CLI de InfluxDB**:
   
   Asegúrate de que el servidor `influxd` esté corriendo y luego ejecuta el cliente CLI desde cualquier terminal:
   
   ```bash
   influx setup
   ```

2. **Introducir los parámetros iniciales**:

   Durante la ejecución del comando `setup`, se te pedirá que introduzcas los siguientes valores:

   - **Nombre de usuario**: Introduce un nombre de usuario para el administrador.
   - **Contraseña**: Especifica una contraseña segura.
   - **Nombre de la organización**: Proporciona un nombre para la organización, por ejemplo, `MiOrganización`.
   - **Nombre del bucket**: Define un bucket para almacenar los datos (como nombre de la bbdd), como `MiBucket`.
   - **Duración de retención de datos** (en horas): Introduce el número de horas para la retención de datos. Si no deseas configurar una retención específica, puedes introducir `0` (sin límite de retención).


**te preguntara si todo es correcto(y/n)**  
    aceptamos


---

#### 4. Obtener el Token de Acceso

Si necesitas recuperar el token generado durante la configuración inicial, ejecuta el siguiente comando:

```bash
influx auth list
```

Esto mostrará una lista de tokens disponibles, junto con sus permisos. Copia el token que corresponda a tu configuración.desde que comienza el token hasta == .Este parametro sera necesario para telegraf.

---


#### 5. Configurar InfluxDB como un Servicio

Para que InfluxDB se ejecute automáticamente cada vez que el servidor se inicie, puedes configurarlo como un servicio del sistema.

1. **Crear un archivo de servicio para systemd**:
   ```bash
   sudo nano /etc/systemd/system/influxdb.service
   ```

   Añade el siguiente contenido al archivo:
   ```ini
   [Unit]
   Description=InfluxDB Service
   After=network.target

   [Service]
   ExecStart=/ruta/completa/a/influxd
   Restart=always
   User=tu_usuario

   [Install]
   WantedBy=multi-user.target
   ```

   Reemplaza `/ruta/completa/a/influxd` con la ruta completa donde está ubicado el binario `influxd`.

2. **Recargar los servicios de systemd**:
   ```bash
   sudo systemctl daemon-reload
   ```

3. **Habilitar el servicio para que se inicie automáticamente**:
   ```bash
   sudo systemctl enable influxdb
   ```

4. **Iniciar el servicio**:
   ```bash
   sudo systemctl start influxdb
   ```

5. **Verificar el estado del servicio**:
   ```bash
   sudo systemctl status influxdb
   ```

---

Con esta guía, has instalado y configurado InfluxDB v2 en un entorno sin interfaz gráfica, listo para recibir y almacenar métricas. Y estara configurado como servicio. Cuando configuremos Telegraf, necesitaremos el nombre del bucket, el nombre de la organización, el token y la IP del servidor donde está corriendo InfluxDB.




























# Guía de Instalación y Configuración de Telegraf en Servidores

## Descripción General
Esta parte del documento explica los pasos para instalar y configurar el agente **Telegraf** para la recolección de métricas en servidores de Linux, con envío de datos a **InfluxDB** y la posterior visualizacion en **Grafana**. El propósito es simplificar el proceso de despliegue.

---

## 1. Instalación de Telegraf

### Requisitos
- **Sistema Operativo**: Linux (64 bits). Si tu servidor es de 32 bits, consulta la página oficial de [InfluxData Downloads](https://portal.influxdata.com/downloads) para descargar la versión adecuada.

### Pasos de Instalación
1. **Descargar el archivo binario de Telegraf**: 

    ```bash
    wget https://dl.influxdata.com/telegraf/releases/telegraf-1.32.2_linux_amd64.tar.gz
    ```
    

2. **Descomprimir el archivo descargado**:

    ```bash
    tar xf telegraf-1.32.2_linux_amd64.tar.gz
    ```

    Esto crea una carpeta llamada `telegraf-1.32.2/` con los binarios de Telegraf.

---

## 2. Configuración de Telegraf

Para configurar Telegraf, generaremos un archivo de configuración que incluya algunas de las métricas clave (CPU, memoria, disco) y el destino de los datos en InfluxDB v2.

1. **Acceder al directorio de Telegraf**:

    ```bash
    cd telegraf-1.32.2/usr/bin
    ```

2. **Generar el archivo de configuración `telegraf.conf`**:

    ```bash
    ./telegraf -sample-config -input-filter cpu:mem:disk -output-filter influxdb_v2 > telegraf.conf
    ```

    - `-sample-config`: Crea un archivo de configuración con ejemplos.
    - `-input-filter cpu:mem:disk`: Selecciona los plugins de input para monitorizar CPU, memoria y disco.
    - `-output-filter influxdb_v2`: Especifica InfluxDB v2 como el destino de las métricas.

## 3. Configuración de Parámetros en `telegraf.conf`

Para una configuración adecuada, vamos a dividir los parámetros en dos secciones: **Parámetros de Salida** y **Parámetros de Entrada**.

### Parámetros de Salida (`[[outputs]]`)

1. **Abrir `telegraf.conf` para editar**: (yo uso nano pero elija el que prefiera)

    ```bash
    nano telegraf.conf
    ```

2. **Buscar la sección de salida (`[[outputs]]`)**:
   - Usa un atajo en `nano` para buscar rápidamente la sección `[[outputs]]`:

     ```bash
     Ctrl + W y escribe [[outputs
     ```

3. **Configurar los parámetros de salida para InfluxDB v2**:
   En la sección `[[outputs.influxdb_v2]]`, define los valores de conexión hacia InfluxDB, los cuales hemos apuntado antes y tenemos a mano. Incluyendo la URL del servidor, el token de acceso, la organización y el bucket de almacenamiento:

   ```ini
   [[outputs.influxdb_v2]]
     urls = ["http://direccion_ip_influxdb:8086"]
     token = "mi_token"
     organization = "mi_organizacion"
     bucket = "mi_bucket"




# Parámetros de Entrada (`[[inputs]]`)

Los parámetros de entrada (`inputs`) son responsables de recoger las métricas que queremos monitorizar. En este documento, explicaremos cómo configurar tanto los plugins predefinidos como los personalizados (como `http_response` y `exec`).

---

## 1. Localizar la sección de entrada (`[[inputs]]`)

Usa el siguiente atajo en `nano` para localizar rápidamente la sección `[[inputs]]` en el archivo `telegraf.conf`:

```bash
Ctrl + W y escribe [[inputs
```
## 2. Configurar los plugins predefinidos

Al generar el archivo `telegraf.conf`, los plugins de entrada básicos como `cpu`, `mem` y `disk` ya están definidos. Puedes revisarlos pero no hace falta modificarlos en principio.


## 3. Configurar los plugins personalizados

Para monitorizar respuestas HTTP o ejecutar scripts específicos, debemos configurar los plugins `http_response` y `exec`. exec lo usaremos para obtener la respuesta de las urls a monitorizar.

### Configuración del plugin `http_response`

Este plugin permite monitorizar el tiempo de respuesta de URLs específicas. Se configura como sigue:

```ini
[[inputs.http_response]]
  urls = ["https://api.github.com/", "https://postman-echo.com/get"] # URLs a monitorizar.
  interval = "10s"                     # Intervalo de consulta.
  method = "GET"                       # Método de solicitud HTTP.
  response_timeout = "5s"              # Tiempo máximo de espera.
  name_override = "http_response_time" # Personaliza el nombre de la métrica.
```

### Configuración del plugin `exec`

Este plugin permite ejecutar scripts externos para recolectar métricas específicas. En este caso, utilizamos scripts en Python para obtener mensajes de error y respuestas HTTP.

#### Ejemplo de configuración para un script de Python:
Estos son ejemplos reales en mi ordenador personal.
```ini
[[inputs.exec]]
  commands = ["python3 /home/luisgarcia/tfg/scripts/mensaje.py"] # Ruta absoluta del script.
  interval = "60s"                                              # Intervalo de ejecución.
  timeout = "10s"                                               # Tiempo máximo de espera.
  data_format = "influx"                                        # Formato de datos.
  name_override = "http_response"                               # Nombre común para la métrica.
  
  [inputs.exec.tags]
    url = "http://primero.com" # Etiqueta para identificar la URL procesada.
```

#### Ejemplo para una segunda URL:

```ini
[[inputs.exec]]
  commands = ["python3 /home/luisgarcia/tfg/scripts/mensaje2.py"]
  interval = "60s"
  timeout = "10s"
  data_format = "influx"
  name_override = "http_response"
  
  [inputs.exec.tags]
    url = "http://segundo.com"
```


## Uso del Script en Python para Monitorizar APIs

El script al que hemos llamado en telegraf.conf, es el siguiente, esta escrito en Python, permite monitorizar el estado y la respuesta de una API. Es útil para identificar errores, medir tiempos de respuesta y registrar cualquier fallo o comportamiento inesperado. El script utiliza la biblioteca `requests` para realizar solicitudes HTTP y está diseñado para ser altamente configurable. A continuacion un resumen del funcionamiento, la configuracion y el codigo ejemplo:

### Resumen del Funcionamiento del Script

1. **Solicita la URL**:  
   El script realiza una solicitud HTTP a la URL configurada utilizando la biblioteca `requests`.

2. **Manejo de Respuestas**:
   - Si la API responde correctamente (código 200), imprime un mensaje de éxito.
   - Si ocurre un error (por ejemplo, códigos 404 o 500), registra el mensaje de error.

3. **Manejo de Errores**:
   - En caso de tiempo de espera agotado, muestra un mensaje indicando el timeout.
   - Si ocurre algún otro problema de red, captura la excepción y registra el error.

Este script permite monitorizar el estado de las APIs y detectar rápidamente problemas en las respuestas.


### Configuración para Adaptar el Script

El script está diseñado para que sea fácil de personalizar. A continuación, se explican las partes clave que se pueden modificar:

1. **URL a Monitorizar**:
   - Cambia la variable `url` por la dirección de tu API. Puedes usar diferentes URLs para probar su funcionamiento.

2. **Tiempo de Espera (Timeout)**:
   - Ajusta el tiempo de espera según las características de tu API:
     ```python
     response = requests.get(url, timeout=5)  # Cambia 5 por el tiempo deseado en segundos
     ```


### Ejemplo del Script en Python

A continuación, se presenta el script completo que puedes usar como base:

```python
import requests

url = "http://example.com/api"  # Cambia esto por la URL que deseas monitorizar

try:
    response = requests.get(url, timeout=2)
    if response.status_code == 200:
        print(f"http_response,url={url} status_code=200,message=\"OK\"")
    else:
        # Almacena el contenido de la respuesta en caso de error
        error_message = response.text.replace('"', '\\"')  # Escapa comillas en el mensaje
        print(f"http_response,url={url} status_code={response.status_code},message=\"{error_message}\"")
except requests.exceptions.Timeout:
    print(f"http_response,url={url} status_code=408,message=\"Timeout\"")
except requests.exceptions.RequestException as e:
    # Almacena el mensaje de error en caso de que haya una excepción en la solicitud
    error_message = str(e).replace('"', '\\"')  # Escapa comillas en el mensaje
    print(f"http_response,url={url} status_code=500,message=\"{error_message}\"")
````

ejecutar telegraf. ahora podemos ejecutar telegraf y desde influx podremos ver las metricas configuradas en telegraf.


## 4. Ejecutar Telegraf

Ahora que hemos configurado `telegraf.conf`, podemos ejecutar Telegraf y enviar las métricas configuradas a InfluxDB. Esto permitirá monitorear las métricas desde la base de datos.

### Pasos para Ejecutar Telegraf

1. **Navegar a la Carpeta de Telegraf**:
   - Ve al directorio donde se encuentra el binario de Telegraf. Por ejemplo:
     ```bash
     cd telegraf-1.32.2/usr/bin
     ```

2. **Ejecutar Telegraf**:
   - Usa el siguiente comando para ejecutar Telegraf con la configuración definida en `telegraf.conf`:
     ```bash
     ./telegraf --config telegraf.conf
     ```

### Verificación

- Una vez ejecutado, Telegraf comenzará a enviar las métricas a InfluxDB.
- Puedes verificar que las métricas están siendo recibidas correctamente desde la interfaz de InfluxDB, accediendo a **Data Explorer** y ejecutando una consulta para revisar las métricas.





### 5 Configurar Telegraf como un Servicio

#### Descripción General

Esta guía explica cómo configurar **Telegraf** como un servicio utilizando **systemd** en sistemas Linux. Al configurarlo como un servicio, **Telegraf** se ejecutará automáticamente cada vez que el servidor se inicie, asegurando que las métricas se recojan y envíen continuamente a **InfluxDB** sin necesidad de intervención manual.

---

#### 1. Crear un archivo de servicio para systemd

1. Abre un terminal y crea un archivo de servicio para Telegraf en el directorio de configuración de systemd:
   ```bash
   sudo nano /etc/systemd/system/telegraf.service
   ```

2. Añade el siguiente contenido al archivo:
   ```ini
   [Unit]
   Description=Telegraf Service
   After=network.target

   [Service]
   ExecStart=/ruta/completa/a/telegraf --config /ruta/completa/a/telegraf.conf
   Restart=always
   User=tu_usuario

   [Install]
   WantedBy=multi-user.target
   ```

   - **`ExecStart`**: Especifica la ruta completa al binario de Telegraf y al archivo de configuración (`telegraf.conf`). Por ejemplo:
     ```bash
     ExecStart=/home/luisgarcia/telegraf-1.32.2/usr/bin/telegraf --config /home/luisgarcia/telegraf-1.32.2/usr/bin/telegraf.conf
     ```
   - **`User`**: Cambia `tu_usuario` por el usuario que ejecutará el servicio (por ejemplo, `luisgarcia`).

---

#### 2. Recargar systemd

Después de guardar el archivo, recarga los demonios de **systemd** para que el nuevo archivo de servicio sea reconocido:
```bash
sudo systemctl daemon-reload
```

---

#### 3. Habilitar el servicio para inicio automático

Habilita el servicio para que se ejecute automáticamente cada vez que el servidor arranque:
```bash
sudo systemctl enable telegraf
```

---

#### 4. Iniciar el servicio de Telegraf

Inicia el servicio de Telegraf manualmente para comprobar que funciona correctamente:
```bash
sudo systemctl start telegraf
```

---

#### 5. Verificar el estado del servicio

Revisa el estado del servicio para confirmar que está corriendo sin problemas:
```bash
sudo systemctl status telegraf
```

Si el servicio se está ejecutando correctamente, deberías ver una salida indicando que está activo (`Active: active (running)`).

---

#### 6. Logs del servicio

Para depurar problemas o verificar que Telegraf está funcionando correctamente, puedes consultar los logs del servicio:
```bash
sudo journalctl -u telegraf -f
```

Esto mostrará los eventos en tiempo real relacionados con el servicio de Telegraf.

---

#### 7. Notas adicionales

- **Permisos de usuario**: Asegúrate de que el usuario especificado en `User` tenga permisos para acceder al archivo de configuración (`telegraf.conf`) y ejecutar cualquier script asociado.
- **Plugins personalizados**: Si estás utilizando plugins como `exec`, asegúrate de que las rutas especificadas en los comandos son accesibles y tienen los permisos correctos.
- **Prueba del servicio**: Después de configurar, realiza una consulta en InfluxDB para confirmar que las métricas están siendo enviadas correctamente.

Con esta configuración, Telegraf estará listo para ejecutarse automáticamente y garantizar una recolección continua de métricas.










# Guía de Instalación y Configuración de Grafana

## Descripción General
Esta guía detalla los pasos para instalar y configurar **Grafana** en servidores Linux. Grafana se utilizará para visualizar los datos almacenados en InfluxDB v2 y generados por Telegraf.

---

## 1. Instalación de Grafana

### Requisitos
- **Sistema Operativo**: Linux (64 bits). Para otras arquitecturas o sistemas, consulta la página oficial de [Grafana Downloads](https://grafana.com/grafana/download).
- **InfluxDB v2**: Asegúrate de que InfluxDB esté instalado y funcionando antes de configurar Grafana.

### Pasos de Instalación

1. **Descargar el archivo binario de Grafana**:

    ```bash
    wget https://dl.grafana.com/enterprise/release/grafana-enterprise-11.3.0+security-01.linux-amd64.tar.gz
    ```
    


2. **Descomprimir el archivo descargado**:

    ```bash
    tar -zxvf grafana-enterprise-11.3.0+security-01.linux-amd64.tar.gz
    ```

    Esto crea una carpeta llamada `grafana-v11.3.0` con los binarios de Grafana.

3. **Iniciar el servidor de Grafana**:

    ```bash
    cd grafana-v11.3.0/bin
    ./grafana-server
    ```

    Grafana se iniciará en el puerto `3000` por defecto. Puedes verificar su funcionamiento accediendo a [http://localhost:3000](http://localhost:3000) desde un navegador web.

---

## 2. Configuración Inicial de Grafana

1. **Acceso a la Interfaz Web**:
   - Abre un navegador web y accede a [http://localhost:3000](http://localhost:3000).

2. **Inicio de Sesión**:
   - **Usuario predeterminado**: `admin`
   - **Contraseña predeterminada**: `admin`
   - Cambia la contraseña predeterminada al iniciar sesión por primera vez.

3. **Configurar la Fuente de Datos**:
   - Una vez dentro de la interfaz de Grafana:
     1. Ve a **Settings (Configuración)** > **Data Sources (Fuentes de Datos)**.
     2. Haz clic en **Add Data Source**.
     3. Selecciona **InfluxDB** como fuente de datos.

4. **Configurar los Detalles de Conexión**:
   - Rellena los campos con los datos de tu servidor InfluxDB:
     - **URL**: `http://IP_DEL_SERVIDOR_INFLUXDB:8086`
     - **Organization**: El nombre de tu organización, como `MiOrganización`.
     - **Bucket**: El bucket configurado en InfluxDB, como `MiBucket`.
     - **Token**: El token de acceso generado en InfluxDB.

5. **Probar la Conexión**:
   - Haz clic en el botón **Save & Test** para verificar la conexión con InfluxDB.
   - Si todo está configurado correctamente, aparecerá un mensaje indicando que la conexión fue exitosa.

---

## Configuración del Correo en Grafana (`grafana.ini`)

Para configurar el envío de notificaciones por correo desde Grafana, debes modificar el archivo `grafana.ini`. A continuación, te explico los pasos:

### Pasos para Configurar el Correo SMTP

1. **Copiar y Renombrar el Archivo `default.ini`**:
   - En la carpeta `grafana/conf`, encontrarás un archivo llamado `default.ini`. Este archivo contiene la configuración base.
   - Haz una copia y renómbrala como `grafana.ini`:
     ```bash
     cp default.ini grafana.ini
     ```

2. **Editar la Sección `[smtp]` en `grafana.ini`**:
   - Abre el archivo `grafana.ini` para editarlo:
     ```bash
     nano grafana.ini
     ```
   - Busca la sección `[smtp]` y configura los siguientes parámetros:
     ```ini
     [smtp]
     enabled = true
     host = smtp.gmail.com:587
     user = tu_correo@gmail.com
     password = contraseña_por_token
     cert_file =
     key_file =
     skip_verify = true
     from_address = tu_correo@gmail.com
     from_name = grafana
     ehlo_identity = grafana.local
     startTLS_policy = OpportunisticStartTLS
     enable_tracing = false
     ```

   - **Nota importante**: Para obtener la contraseña por token:
     1. Ve a tu cuenta de Google y genera una contraseña específica para aplicaciones.
     2. Usa esta contraseña en el campo `password`.

3. **Guardar y Aplicar los Cambios**:
   - Guarda los cambios en `grafana.ini` y cierra el editor.
   - Si Grafana ya está en ejecución, corta la ejecución actual.
   - Ve al directorio principal de Grafana (`grafana-v11.2.0`) y ejecuta el siguiente comando para iniciar Grafana con la configuración actualizada:
     ```bash
     ./bin/grafana-server --config conf/grafana.ini
     ```

4. **Probar el Correo**:
   - Ve a **Configuration > Notification Channels** en la interfaz de Grafana.
   - Configura un canal de notificación con el correo configurado y realiza una prueba para verificar que funciona.
   - 
   

## 3. Importar un Dashboard en Grafana

Después de configurar Grafana y conectar las fuentes de datos, el siguiente paso es importar un dashboard predefinido para visualizar los datos. A continuación, se detallan los pasos para importar un dashboard desde un archivo JSON, como los que se pueden encontrar en repositorios de GitHub.

### Pasos para Importar un Dashboard

1. **Accede a la Sección de Dashboards**:
   - En la barra lateral izquierda de Grafana, selecciona **"Dashboards"**.
   - En la parte superior derecha, haz clic en el botón azul **"New"**.

2. **Selecciona la Opción "Import"**:
   - En el menú desplegable, selecciona la opción **"Import"**.

3. **Carga el Archivo JSON**:
   - Desde la página de importación, tienes dos opciones para cargar el dashboard:
     - **Subir un archivo JSON**:
       - Haz clic en **"Upload JSON file"** y selecciona el archivo JSON del dashboard que deseas importar.
     - **Pegar el JSON**:
       - Si tienes el código JSON, pégalo directamente en el cuadro de texto proporcionado.

4. **Configura el Dashboard Importado**:
   - Se te pedirá que selecciones o confirmes la **fuente de datos** asociada al dashboard. Asegúrate de elegir la fuente correcta (por ejemplo, InfluxDB configurado previamente).

5. **Haz clic en "Import"**:
   - Una vez que hayas configurado la fuente de datos, haz clic en el botón **"Import"**.

6. **Verifica el Dashboard Importado**:
   - El dashboard aparecerá inmediatamente en tu lista de dashboards.
   - Ábrelo y verifica que los datos se estén mostrando correctamente según las métricas configuradas.

### Notas Adicionales

- **Dónde Encontrar Dashboards JSON**:
  - Puedes encontrar el dashboard en github/dashboards
  
---




# Añadir un Nuevo Servidor o Servicio al Sistema de Monitorización

## 1. Añadir un Nuevo Servidor
Para añadir un nuevo servidor al sistema de monitorización, únicamente debes instalar y configurar **Telegraf** en el servidor que desees monitorizar. Asegúrate de que Telegraf esté configurado para enviar las métricas a la base de datos InfluxDB. Esto es posible porque los dashboards de Grafana permiten seleccionar cualquier servidor configurado en la base de datos.

Sigue estos pasos:
1. Instala **Telegraf** en el nuevo servidor.
2. Configura el archivo `telegraf.conf` para que envíe las métricas relevantes a la base de datos InfluxDB.
3. Verifica que los datos estén llegando correctamente a la base de datos.

Para más detalles, consulta la sección de configuración de **Telegraf** en este manual.

---

## 2. Añadir un Nuevo Servicio
### Opciones de Servicios:
- **Servicios Web (URLs)**
- **Contenedores Docker**

El proceso para añadir un nuevo servicio depende de si deseas monitorizar un servicio web o un contenedor Docker. A continuación, se detalla cómo hacerlo.

### 2.1 Monitorización de Servicios Web (URLs)
1. Crea un nuevo archivo Python en la carpeta de scripts del sistema, siguiendo esta plantilla:

```python
import requests

# Define la URL del servicio
url = "https://example.com"
# Define un alias descriptivo para el servicio
alias = "servicio_ejemplo"
# Define las palabras clave asociadas al servicio
keywords = "frontend\,backend\,ejemplo"

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
```

### Modificación de Variables y Configuración

#### **Monitorización de Servicios Web**

1. **Modifica las variables en la plantilla**:
   - **`url`**: Especifica la URL del servicio a monitorizar.
   - **`alias`**: Asigna un nombre descriptivo al servicio.
   - **`keywords`**: Define las palabras clave asociadas al servicio para facilitar los filtros en Grafana.

2. **Añade el script al archivo de configuración de Telegraf (`telegraf.conf`) como un plugin exec**:
   ```ini
   [[inputs.exec]]
     commands = ["python3 /ruta/al/script.py"]  # Comando que se ejecutará periódicamente (asegúrate de que la ruta al script sea correcta).
     interval = "30s"  # Intervalo de ejecución del script (cada 30 segundos en este caso).
     timeout = "10s"  # Tiempo máximo permitido para que el script se ejecute antes de interrumpirlo.
     data_format = "influx"  # Formato esperado para los datos generados (InfluxDB en este caso).
     name_override = "http_response"  # Nombre base de la medición almacenada en la base de datos.

     [inputs.exec.tags]
       url = "https://example.com"  # URL del servicio que se está monitorizando.
   ```
### Monitorización de Contenedores Docker

1. **Crea un nuevo archivo Python en la carpeta de scripts del sistema**:
   Utiliza la siguiente plantilla:

   ```python
   import docker

   # Define las variables del contenedor
   target_container_name = "nombre_del_contenedor"
   alias = "alias_contenedor"
   keywords = "docker\,contenedor\,ejemplo"

   try:
       client = docker.DockerClient(base_url='unix://var/run/docker.sock')
       container = client.containers.get(target_container_name)
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
   ```
   
   ### Modifica las variables en la plantilla

1. **Variables**:
   - **`target_container_name`**: Especifica el nombre del contenedor Docker a monitorizar.
   - **`alias`**: Asigna un nombre descriptivo al contenedor.
   - **`keywords`**: Define las palabras clave asociadas al contenedor.

2. **Configuración en Telegraf**:
   Añade el script al archivo de configuración de Telegraf (`telegraf.conf`) como un plugin `exec`:

   ```ini
   [[inputs.exec]]
     commands = ["python3 /ruta/al/script_docker.py"]  # Comando para ejecutar el script de monitorización del contenedor Docker.
     interval = "30s"  # Intervalo de ejecución del script (cada 30 segundos).
     timeout = "10s"  # Tiempo máximo permitido para que el script se ejecute antes de interrumpirlo.
     data_format = "influx"  # Formato esperado para los datos generados (InfluxDB en este caso).
     name_override = "http_response"  # Nombre base de la medición almacenada en la base de datos.

     [inputs.exec.tags]
       url = "docker"  # Etiqueta que indica que los datos provienen de un contenedor Docker.

   ```
  









