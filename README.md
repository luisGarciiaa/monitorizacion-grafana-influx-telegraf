# Guía de Instalación y Configuración del Sistema de Monitorización (Influxdb_v2, Telegraf y Grafana)


---

# Índice de la Guía de Configuración del Sistema de Monitorización

1. Introducción  
   - Descripción general del sistema  
   - Componentes principales: InfluxDB, Telegraf, Grafana  

2. Instalación y Configuración de InfluxDB  
   - Requisitos  
   - Pasos de instalación  
   - Configuración inicial  
   - Configuración avanzada (retención de datos, tokens, etc.)  

3. Instalación y Configuración de Telegraf  
   - Requisitos  
   - Pasos de instalación  
   - Configuración de entradas (`inputs`)  
      - Monitorización básica (CPU, memoria, disco)  
      - Monitorización de servicios web y contenedores Docker con JSON  
   - Configuración de salidas (`outputs`)  
   - Ejecución y verificación de Telegraf  
   - Configuración de Telegraf como servicio  

4. Instalación y Configuración de Grafana  
   - Requisitos  
   - Pasos de instalación  
   - Configuración inicial  
   - Configuración de notificaciones por correo  
   - Importación de dashboards predefinidos  
      - Revisión del bucket y fuente de datos  

5. Creación y Configuración de Dashboards  
   - Definición del Dashboard de Servidores  
      - Descripción del propósito  
      - Métricas mostradas  
      - Configuración de consultas en Grafana  
   - Definición del Dashboard de Servicios  
      - Descripción del propósito  
      - Métricas mostradas  
      - Configuración de consultas en Grafana  

6. Añadir Nuevos Servidores o Servicios  
   - Añadir un nuevo servidor  
   - Añadir un nuevo servicio o contenedor Docker  
      - Monitorización de servicios web (URLs)  
      - Monitorización de contenedores Docker  

7. Configuración de Alertas en Grafana  
   - Introducción a las alertas  
   - Configuración inicial  
      - Crear una carpeta para las alertas  
      - Configurar un canal de notificación  
   - Personalización de las alertas  
      - Duplicar y personalizar una alerta  
      - Configurar el comportamiento de evaluación  
      - Añadir canales de notificación  
   - Mini Guía por Tipo de Alerta  
      - Alertas de CPU  
      - Alertas de memoria  
      - Alertas de disco  
      - Alertas de servicios  
         - Configuración de filtros por URL, nombre, palabras clave  
         - Ajustes para alertar por `status_code != 200`  
      - Alertas de contenedores Docker  
         - Configuración de filtros por nombre, palabras clave  
         - Ajustes para alertar por `status_code != 200`  
   - Verificación y pruebas de las alertas  
   - Recomendaciones adicionales  



---
# 1. Introducción

## Descripción General del Sistema

Este sistema de monitorización combina tres herramientas clave: **InfluxDB**, **Telegraf** y **Grafana**, para ofrecer una solución eficiente y flexible para la recopilación, almacenamiento y visualización de métricas en servidores y servicios.

- **InfluxDB**: Una base de datos optimizada para manejar datos de series temporales, ideal para almacenar métricas con gran frecuencia de actualización.
- **Telegraf**: Un agente ligero que recopila datos de servidores y servicios (como URLs o contenedores Docker) y los envía a InfluxDB.
- **Grafana**: Una plataforma de visualización que transforma las métricas almacenadas en dashboards interactivos, fáciles de entender y personalizar.

El objetivo principal es centralizar la monitorización, facilitar la detección de problemas y ofrecer herramientas para tomar decisiones rápidas basadas en datos en tiempo real.

---
---

# 2.Guía de Instalación y Configuración de InfluxDB v2

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




## 2. Configuración Inicial
### A. Servidor con Entorno Gráfico 

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

#### 3. Configuración de API y Token de Acceso

Para permitir la conexión desde Telegraf u otras aplicaciones externas, necesitas un token de acceso.

1. Dirígete a **Data > Tokens** en la interfaz de InfluxDB.
2. **Crear un nuevo token** para tu organización. Guarda este token en un lugar seguro, ya que será necesario para las conexiones externas.

---

#### 4. Configuración de Retención de Datos

1. Navega a **Data > Buckets** en la interfaz de InfluxDB.
2. Selecciona el bucket que creaste durante la configuración inicial (ej. `MiBucket`).
3. Ajusta la **Retención de Datos** según sea necesario, por ejemplo, 30 días o 90 días, dependiendo de tus requisitos.

---

#### 5. Comprobación de la IP del Servidor y Preparación para la Conexión Externa de Telegraf

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


## 3. Configurar InfluxDB como un Servicio

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




























# 3.Guía de Instalación y Configuración de Telegraf en Servidores

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

Los parámetros de entrada (`inputs`) son responsables de recoger las métricas que queremos monitorizar. En este documento, explicaremos cómo configurar tanto los plugins predefinidos como los personalizados (como `exec` para servicios web y contenedores Docker).

---

## 1. Localizar la sección de entrada (`[[inputs]]`)

Usa el siguiente atajo en `nano` para localizar rápidamente la sección `[[inputs]]` en el archivo `telegraf.conf`:

```bash
Ctrl + W y escribe [[inputs
```

---




## 2. Configuracion plugins

Actualmente, se han definido tres dashboards principales para monitorización. Cada uno utiliza diferentes plugins de entrada (`inputs`) de Telegraf:

- **Dashboard de Servidores**:  
  Monitorea el sistema general (CPU, memoria, disco) utilizando los plugins predefinidos: `cpu`, `mem`, y `disk`.  (Si hemos puesto el comando que mencionabamos antes, estos plugins se generan solos) Puedes verificar que están habilitados y configurados correctamente revisando las siguientes secciones:


  **Plugins requeridos**:  
    ```ini
    [[inputs.cpu]]
      percpu = true
      totalcpu = true
      collect_cpu_time = false
      report_active = false
    
    [[inputs.mem]]
      fieldpass = ["used_percent"]
    
    [[inputs.disk]]
      ignore_fs = ["tmpfs", "devtmpfs", "overlay"]
    ```

- **Dashboard de Servicios**:  
  Permite monitorizar el estado de servicios web y contenedores Docker mediante scripts de Python (`monitor_servicio.py` y `monitor_docker.py`).  
  **Plugins requeridos**:  
  ```ini
  [[inputs.exec]]  # Configurado para servicios
  [[inputs.exec]]  # Configurado para contenedores Docker mediante script
  ```

- **Dashboard Técnico de Docker**:  
  Proporciona información técnica y detallada sobre el consumo de recursos de los contenedores Docker (CPU, memoria, red y disco). No requiere scripts de Python.  
  **Plugin requerido**:  
  ```ini
  [[inputs.docker]]
  ```

---

## 2. Configuración del Plugin `[[inputs.docker]]`

Para el **Dashboard Técnico de Docker**, es necesario habilitar el plugin `docker` en el archivo `telegraf.conf`. Este plugin recopila métricas directamente del socket de Docker sin necesidad de scripts adicionales.

### Configuración:

```ini
[[inputs.docker]]
  endpoint = "unix:///var/run/docker.sock"  # Ruta al socket de Docker
  gather_services = false
  container_state_include = ["running", "paused", "exited"]  # Incluye estados de contenedores específicos
  interval = "5s"  # Intervalo de recolección de datos
  timeout = "5s"  # Tiempo máximo para obtener los datos
  container_name_include = []  # Opcional: especifica contenedores a incluir
  container_name_exclude = []  # Opcional: especifica contenedores a excluir
```

### Notas:
- Asegúrate de que el usuario que ejecuta Telegraf tiene permisos para acceder al socket de Docker (`/var/run/docker.sock`). Puedes configurarlo así:  
  ```bash
  sudo usermod -aG docker telegraf
  ```

---

## 3. Relación entre Dashboards y Plugins

| Dashboard               | Plugins Utilizados                                          | Detalles                                                    |
|--------------------------|------------------------------------------------------------|------------------------------------------------------------|
| **Servidores**           | `cpu`, `mem`, `disk`                                       | No requiere configuración adicional.                       |
| **Servicios**            | `exec` (servicios y contenedores mediante scripts)         | Usa los scripts `monitor_servicio.py` y `monitor_docker.py`.|
| **Técnico de Docker**    | `docker`                                                   | Recopila métricas de contenedores directamente de Docker.   |

---

## 4. Configuración General de los Plugins `exec`

### Configuración del plugin `exec` para el Dashboard de Servicios:

```ini
[[inputs.exec]]
  commands = ["python3 /ruta/completa/a/scripts/monitor_servicio.py"]  # Script para servicios web
  interval = "30s"  # Intervalo de ejecución
  timeout = "10s"  # Tiempo máximo permitido
  data_format = "influx"  # Formato de los datos
  name_override = "servicio_gen"  # Nombre de la medición
  [inputs.exec.tags]
    url = "servicio_general"

[[inputs.exec]]
  commands = ["python3 /ruta/completa/a/scripts/monitor_docker.py"]  # Script para contenedores Docker
  interval = "30s"
  timeout = "10s"
  data_format = "influx"
  name_override = "docker_gen"
  [inputs.exec.tags]
    url = "docker_general"
```

### Configuración de Archivos JSON y Scripts
- **JSON utilizados**:
  - `servicios.json` y `dockers.json` (deben estar en la ruta configurada en los scripts).  
- **Ruta completa de los scripts**:  
  Asegúrate de incluir la ruta absoluta en los comandos de los plugins `exec`.

### Notas sobre la configuración:

- **Ruta completa a los scripts**
  - Ejemplo de rutas absolutas:
    ```bash
    /home/usuario/tfg/scripts/servicios.py
    /home/usuario/tfg/scripts/dockers.py
    ```

- **Ubicación de los JSON**
  - `servicios.json`: `/home/usuario/tfg/scripts/servicios.json`
  - `dockers.json`: `/home/usuario/tfg/scripts/dockers.json`

- **Intervalo de ejecución**
  - El intervalo (`interval = "30s"`) puede ajustarse según tus necesidades. Intervalos más cortos permiten detectar problemas rápidamente, pero incrementan la carga del sistema.

---

















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










# 4.Guía de Instalación y Configuración de Grafana

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

- **Revisión del Bucket:**
  - El bucket predeterminado configurado en las consultas del dashboard es "DatosPrueba". Si tu bucket tiene un nombre diferente, debes modificarlo en las consultas de cada panel del dashboard para reflejar el nombre de tu bucket.

- **Dónde Encontrar Dashboards JSON**:
  - Puedes encontrar el dashboard en github/dashboards
  
---




# 6. Añadir un Nuevo Servidor o Servicio al Sistema de Monitorización

## 1. Añadir un Nuevo Servidor
Añadir un nuevo servidor al sistema de monitorización ahora es un proceso sencillo. Solo necesitas configurar **Telegraf** en el servidor y asegurarte de que envíe las métricas al bucket de **InfluxDB**. Los dashboards de Grafana ya están preparados para reconocer y mostrar los datos de cualquier servidor configurado en la base de datos.

Pasos:
1. Instala **Telegraf** en el nuevo servidor siguiendo la guía de instalación.
2. Configura `telegraf.conf` con las métricas básicas (CPU, memoria, disco).
3. Verifica que los datos se están enviando correctamente al bucket de **InfluxDB**.

---

## 2. Añadir un Nuevo Servicio o Contenedor Docker

Con el sistema actualizado, ya no es necesario crear scripts individuales o modificar configuraciones complejas. Ahora, simplemente edita los archivos JSON en la carpeta `scripts` para añadir nuevos servicios o contenedores Docker.

### 2.1 Monitorización de Servicios Web (URLs)

1. **Editar el archivo `servicios.json`**:
   - Abre el archivo en la carpeta `scripts`.
   - Añade una nueva entrada con los siguientes campos:
     ```json
     {
       "url": "http://example.com",
       "nombre": "mi_servicio",
       "keywords": "frontend,api,web"
     }
     ```

2. **Campos requeridos**:
   - **`url`**: La dirección del servicio web a monitorizar.
   - **`nombre`**: Un identificador único y descriptivo para el servicio.
   - **`keywords`**: Palabras clave asociadas para facilitar los filtros en Grafana.

3. **Guardar los cambios**:
   - Guarda el archivo. Telegraf procesará automáticamente el nuevo servicio.

---

### 2.2 Monitorización de Contenedores Docker

1. **Editar el archivo `dockers.json`**:
   - Abre el archivo en la carpeta `scripts`.
   - Añade una nueva entrada con los siguientes campos:
     ```json
     {
       "nombre": "mi_contenedor",
       "alias": "mi_contenedor_alias",
       "keywords": "backend,database,docker"
     }
     ```

2. **Campos requeridos**:
   - **`nombre`**: El nombre del contenedor Docker que deseas monitorizar.
   - **`alias`**: Un identificador único y descriptivo para el contenedor.
   - **`keywords`**: Palabras clave asociadas para facilitar los filtros en Grafana.

3. **Guardar los cambios**:
   - Guarda el archivo. Telegraf procesará automáticamente el nuevo contenedor.

---

### Beneficios del Nuevo Enfoque

- **Simplificación**: Ya no es necesario crear scripts personalizados para cada servicio o contenedor.
- **Flexibilidad**: Los servicios y contenedores se configuran en un solo lugar (los archivos JSON).
- **Automatización**: Telegraf detectará y procesará automáticamente las nuevas entradas sin necesidad de reiniciar.

---
  
  
  
  
 # 7. Configuración de Alertas en Grafana

En este apartado podrás configurar y gestionar alertas en Grafana, personalizando alarmas para que se adapten a tus necesidades específicas. Podrás configurar alertas que te avisen a tu correo cuando un umbral definido sea superado, ya sea para CPU, memoria, disco, servicios o Docker.

---

## Crear y Configurar una Alerta

### Crear una Nueva Alerta

Para comenzar a configurar una alerta desde cero:

1. Ve a **Alerting** > **Alert rules**.
2. Haz clic en **New alert rule** (arriba a la derecha).

### 1. Asignar un Nombre Descriptivo

Asigna un nombre claro y específico a tu alerta en el campo **Alert rule name** (por ejemplo, `CPU > 80% - Servidor Principal`).

### 2. Definir la Consulta y la Condición de la Alerta

1. En el apartado **Query**, introduce la consulta correspondiente al tipo de alerta que deseas configurar.
   - Consulta la **Mini Guía por Tipo de Alerta** (al final de este documento) para obtener ejemplos específicos de consultas y personalizarlos según tu necesidad.
2. Configura el umbral y las condiciones de activación en la sección **Define alert condition**.

### 3. Configurar el Comportamiento de Evaluación (Evaluation Behavior)

En este paso necesitas seleccionar o crear un folder y un **evaluation group**, además de definir el tiempo de evaluación y el período pendiente.

1. **Seleccionar o Crear un Folder**:
   - Elige un folder existente donde almacenarás las alertas, o crea uno nuevo.
   - Para crear un folder:
     - Haz clic en **Create new folder**.
     - Asigna un nombre descriptivo (por ejemplo, `Alertas`).
     - Define un intervalo de evaluación (por ejemplo, `1m`), que será el tiempo en el que las alertas en este folder serán evaluadas.
     - Guarda los cambios.

2. **Seleccionar o Crear un Evaluation Group**:
   - El **evaluation group** corresponde al grupo de alertas que se evaluarán juntas según el intervalo de evaluación del folder seleccionado.
   - Puedes tener, por ejemplo, un grupo que evalúe cada 2 minutos alertas menos críticas, o uno que evalúe cada 10 segundos alertas que necesitan verificarse rápidamente.

3. **Configurar el Pending Period**:
   - Define cuánto tiempo debe cumplirse la condición antes de activar la alerta. 
   - Por ejemplo:
     - Si no te importa que la CPU esté al 100% durante unos segundos, puedes configurar el **Pending Period** en `2m` para activar la alerta solo si la condición persiste más de 2 minutos.


### 4. Configurar el Canal de Notificación

1. En la sección **Contact points**, selecciona un canal existente o configura uno nuevo.
   - Si no tienes ningún canal configurado:
     - Ve a **Alerting** > **Contact points**.
     - Haz clic en **Create contact point**.
     - Configura:
       - **Nombre**: Usa un nombre descriptivo (por ejemplo, `Correo_TuNombre`).
       - **Tipo de notificación**: Elige el canal deseado (correo electrónico, Slack, etc.).
       - **Dirección**: Añade los destinatarios de las alertas.
     - Guarda la configuración.
2. Asocia el canal de notificación configurado con tu alerta.

### 5. Personalizar el Mensaje de Alerta

1. En la sección de notificaciones, puedes añadir un mensaje informativo para identificar rápidamente el contexto de la alerta.
   - Ejemplos:
     - `Host afectado: ${host}`
     - `Uso de CPU: ${value}%`
     - `Umbral superado: ${threshold}`
2. Guarda los cambios.

### 6. Guardar la Alerta

Una vez completados los pasos anteriores, guarda la alerta para activarla.


  
 # Mini Guía por Tipo de Alerta

## CPU

- **A. Consulta (Query)**:
  ```flux
  from(bucket: "DatosPrueba")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
    |> filter(fn: (r) => r["host"] == "luisgarcia-VirtualBox") // Filtra por el host seleccionado
    |> filter(fn: (r) => r["cpu"] == "cpu-total")
    |> filter(fn: (r) => r["_field"] == "usage_idle")
    |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
    |> map(fn: (r) => ({ r with _value: 100.0 - r._value }))
    |> yield(name: "mean")
  ```
  Modifica:
  - **Bucket**: Cambia `"DatosPrueba"` por el nombre de tu bucket.
  - **Host**: Sustituye `"luisgarcia-VirtualBox"` por el nombre del servidor o máquina que deseas monitorizar.

- **B. Reducción (Reduce)**:
  Configura:
  - **Input**: Selecciona `A` como entrada.
  - **Función**: Selecciona `Last`.
  - **Mode**: Selecciona `Strict`.

- **C. Umbral (Threshold)**:
  Configura:
  - **Input**: Selecciona `B` como entrada.
  - **Is Above**: Especifica el valor del umbral deseado (e.g., `80` para alertar cuando el uso de CPU supere el 80%).

---

## Memoria

- **A. Consulta (Query)**:
  ```flux
  from(bucket: "DatosPrueba")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
    |> filter(fn: (r) => r["host"] == "luisgarcia-VirtualBox") // Filtra por el host seleccionado
    |> filter(fn: (r) => r["_measurement"] == "mem")
    |> filter(fn: (r) => r["_field"] == "free" or r["_field"] == "used")
    |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> map(fn: (r) => ({
          _time: r._time,
          _value: float(v: r["used"]) / (float(v: r["free"]) + float(v: r["used"])) * 100.0, // Asegura que todos los valores sean float
          host: r.host
        }))
    |> yield(name: "mean")
  ```
  Modifica:
  - **Bucket**: Cambia `"DatosPrueba"` por el nombre de tu bucket.
  - **Host**: Sustituye `"luisgarcia-VirtualBox"` por el nombre del servidor o máquina.

- **B. Reducción (Reduce)**:
  Configura:
  - **Input**: Selecciona `A` como entrada.
  - **Función**: Selecciona `Last`.
  - **Mode**: Selecciona `Strict`.

- **C. Umbral (Threshold)**:
  Configura:
  - **Input**: Selecciona `B` como entrada.
  - **Is Above**: Especifica el valor del umbral deseado (e.g., `85` para alertar cuando el uso de memoria supere el 85%).

---

## Disco

- **A. Consulta (Query)**:
  ```flux
  from(bucket: "DatosPrueba")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
    |> filter(fn: (r) => r["host"] == "luisgarcia-VirtualBox") // Filtra por el host seleccionado
    |> filter(fn: (r) => r["_measurement"] == "disk")
    |> filter(fn: (r) => r["_field"] == "used_percent") // Nos centramos solo en el porcentaje de disco usado
    |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
    |> yield(name: "mean")
  ```
  Modifica:
  - **Bucket**: Cambia `"DatosPrueba"` por el nombre de tu bucket.
  - **Host**: Sustituye `"luisgarcia-VirtualBox"` por el nombre del servidor o máquina.

- **B. Reducción (Reduce)**:
  Configura:
  - **Input**: Selecciona `A` como entrada.
  - **Función**: Selecciona `Last`.
  - **Mode**: Selecciona `Strict`.

- **C. Umbral (Threshold)**:
  Configura:
  - **Input**: Selecciona `B` como entrada.
  - **Is Above**: Especifica el valor del umbral deseado (e.g., `90` para alertar cuando el uso del disco supere el 90%).

---

## Servicios

- **A. Consulta (Query)**:
  ```flux
  from(bucket: "DatosPrueba")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) // Rango de tiempo dinámico del panel
    |> filter(fn: (r) => r["_measurement"] == "servicio_gen") // Filtra los datos de 'servicio_gen'
    |> filter(fn: (r) => r["_field"] == "status_code") // Filtro para los códigos de estado
    //  |> filter(fn: (r) => r["url"] == "http://example.com" or r["url"] == "http://another-example.com" or r["url"] == "http://localhost:27017/") // Filtra por una o varias URLs

    //|> filter(fn: (r) => r["nombre"] == "prueba/403") // Opcional: Filtra por el nombre del servicio
    //|> filter(fn: (r) => r["servidor"] == "servidor_1") // Opcional: Filtra por servidor
    //|> filter(fn: (r) => r["proyecto"] == "proyecto_B") // Opcional: Filtra por proyecto
    //|> filter(fn: (r) => r["keywords"] == "api") // Opcional: Filtra por keywords
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value") // Reestructura los datos para 'status_code'
    |> keep(columns: ["_time", "url", "status_code"])
  ```
  Modifica:
  - **Bucket**: Cambia `"DatosPrueba"` por el nombre de tu bucket.
  - **Filtros opcionales**: Usa filtros según tus necesidades (`url`, `nombre`, `servidor`).

- **B. Reducción (Reduce)**:
  Configura:
  - **Input**: Selecciona `A` como entrada.
  - **Función**: Selecciona `Last`.
  - **Mode**: Selecciona `Strict`.

- **C. Umbral (Threshold)**:
  Configura:
  - **Input**: Selecciona `B` como entrada.
  - **Is Above**: Especifica el valor del umbral deseado (e.g., `300` para alertar cuando el codigo no sea correcto).

---

## Docker

- **A. Consulta (Query)**:
  ```flux
  from(bucket: "DatosPrueba")
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) // Rango de tiempo dinámico del panel
    |> filter(fn: (r) => r["_measurement"] == "docker_gen") // Filtra los datos de contenedores
    |> filter(fn: (r) => r["_field"] == "status_code") // Filtro para los códigos de estado
    //|> filter(fn: (r) => r["nombre"] == "alpine") // Opcional: Filtra por nombre del contenedor
    //|> filter(fn: (r) => r["keywords"] == "database") // Opcional: Filtra por keywords del contenedor
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value") // Reestructura los datos
    |> keep(columns: ["_time", "nombre", "status_code"])
  ```
  Modifica:
  - **Bucket**: Cambia `"DatosPrueba"` por el nombre de tu bucket.
  - **Filtros opcionales**: Filtra por `nombre` o `keywords` según tus necesidades.

- **B. Reducción (Reduce)**:
  Configura:
  - **Input**: Selecciona `A` como entrada.
  - **Función**: Selecciona `Last`.
  - **Mode**: Selecciona `Strict`.

- **C. Umbral (Threshold)**:
  Configura:
  - **Input**: Selecciona `B` como entrada.
  - **Is Above**: Especifica el valor del umbral deseado (e.g., `300` para alertar cuando el codigo no sea correcto).
 
  
## Conclusión

Con esta configuración, cada usuario podrá gestionar y personalizar sus alertas en Grafana de forma sencilla. Recuerda duplicar las alertas existentes, ajustar las variables necesarias y definir los canales de notificación apropiados. Si tienes dudas, revisa las consultas proporcionadas para cada tipo de alerta y adapta los valores según tus necesidades.


