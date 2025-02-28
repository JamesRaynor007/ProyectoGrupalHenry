# 🚀 Proyecto de ETL con Docker y MySQL

Este repositorio contiene un pipeline ETL (Extract, Transform, Load) implementado con Python y Docker, que extrae datos de Google Maps, los limpia y los almacena en una base de datos MySQL en contenedores Docker.

## 📌 Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/) (opcional para visualizar datos)
- [Power BI](https://powerbi.microsoft.com/) (opcional para dashboards)

## 📁 Estructura del Proyecto

```
📂 Crear Docker/
├── 📂 data/               # Carpeta donde se almacenan los datos procesados
├── 📂 scripts/            # Scripts de procesamiento ETL
├── 📜 docker-compose.yml  # Configuración de Docker Compose
├── 📜 Dockerfile          # Definición de imagen del contenedor Python
├── 📜 requirements.txt    # Dependencias del proyecto
└── 📜 README.md           # Este archivo
```

## 🚀 Instalación y Ejecución

Sigue los siguientes pasos para ejecutar el proyecto:

### 1️⃣ Construir y ejecutar los contenedores

Desde la carpeta raíz del proyecto, ejecuta los siguientes comandos:

```sh
docker-compose build --no-cache
docker-compose up -d
```

Esto iniciará los contenedores de MySQL y Python, ejecutando el pipeline ETL.

### 2️⃣ Verificar los logs

Puedes revisar la ejecución del pipeline con:

```sh
docker logs -f creardocker-python_app-1
```

Si todo se ejecuta correctamente, deberías ver la siguiente salida:&#x20;

## 🔗 Conectar a la Base de Datos desde MySQL Workbench

1. Abre **MySQL Workbench**.
2. Crea una nueva conexión con los siguientes datos:
   - **Host**: `localhost`
   - **Puerto**: `3306`
   - **Usuario**: `root`
   - **Contraseña**: `root`
   - **Base de Datos**: `Analisis_Total`
3. Guarda y conéctate.
4. Para listar las tablas disponibles, ejecuta:
   ```sql
   SHOW TABLES;
   ```
5. Para visualizar los datos:
   ```sql
   SELECT * FROM restaurantes LIMIT 10;
   ```

## 📊 Conectar Power BI a MySQL en Docker

1. Abre **Power BI Desktop**.
2. En **Inicio > Obtener Datos**, selecciona **Base de datos MySQL**.
3. En **Servidor**, ingresa `localhost`, y en **Base de Datos**, escribe `Analisis_Total`.
4. En **Modo de autenticación**, elige **Base de datos** e ingresa:
   - **Usuario**: `root`
   - **Contraseña**: `root`
5. Presiona **Conectar**.
6. Selecciona las tablas deseadas y carga los datos para visualizarlos en Power BI.

## 🛠 Detener y Reiniciar los Contenedores

Para detener los contenedores y liberar recursos:

```sh
docker-compose down --volumes
```

Para reiniciar desde cero:

```sh
docker-compose build --no-cache
docker-compose up -d
```

## 📌 Notas Finales

- Docker **NO** necesita conexión a internet para acceder a los datos en los contenedores, ya que MySQL y Python están en la misma red interna.
- Si hay problemas de conexión a MySQL, asegúrate de que el servicio está corriendo con:
  ```sh
  docker ps
  ```
- Para ingresar manualmente al contenedor de MySQL, usa:
  ```sh
  docker exec -it creardocker-mysql_db-1 mysql -u root -p
  ```

🎉 **¡Felicidades! Has configurado y ejecutado exitosamente el pipeline ETL en Docker.**

