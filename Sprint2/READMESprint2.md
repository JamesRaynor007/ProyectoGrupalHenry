# 1. Introducción

## Objetivo del Sprint  
En esta fase del proyecto, el equipo ha trabajado en la preparación y estructuración de los datos para garantizar un análisis eficiente y una visualización efectiva. Esto incluyó la identificación de patrones y anomalías en los datos, la construcción de una infraestructura de almacenamiento óptima y el desarrollo de una prueba de concepto para las visualizaciones y productos de Machine Learning.  

El análisis exploratorio de datos (EDA) permitió evaluar la calidad de la información y detectar tendencias, distribuciones y posibles correlaciones. Además, se estableció un pipeline ETL robusto para la extracción, transformación y carga de datos en una estructura de tipo Data Warehouse, asegurando que la información esté disponible de manera organizada y escalable.  

Como parte de este sprint, también se desarrolló un modelo entidad-relación (EER) en formato copo de nieve, optimizando la estructuración de los datos en MySQL y BigQuery. Finalmente, se avanzó en el diseño de una prueba de concepto del dashboard en Power BI, que permitirá visualizar insights clave para la toma de decisiones estratégicas.  

Como parte de este análisis, se presentarán dos opciones para la implementación futura: con el procesamiento y almacenamiento de datos en la nube o con todo el proceso ETL y demás componentes a una infraestructura local.

## Alcance  
Durante este sprint, el equipo ha desarrollado las siguientes tareas clave:  

- **Análisis Exploratorio de Datos (EDA):** Identificación de valores atípicos, distribución de variables y correlaciones.  
- **Implementación del ETL:** Desarrollo de pipelines para procesar y cargar datos en un Data Warehouse con Google Cloud Storage y Cloud Run.  
- **Diseño del Modelo Entidad-Relación (EER):** Creación de un modelo en formato copo de nieve en MySQL. 
- **Automatización con Docker:** Contenerización del proceso ETL para facilitar la implementación y escalabilidad.  
- **Desarrollo de un pipeline conceptual:** Documentación del flujo de trabajo y estructura del sistema.  
- **Diseño preliminar del dashboard en Power BI:** Conexión con el DW y primeras visualizaciones con datos de muestra.  
- **Modelo de recomendación en Python:** Implementación inicial para analizar preferencias de los usuarios y sugerir opciones relevantes.  

## Herramientas Utilizadas  
Para llevar a cabo estas tareas, se utilizaron las siguientes tecnologías y plataformas:  

- **Lenguajes de programación:** Python, SQL.  
- **Almacenamiento y procesamiento de datos:** BigQuery, MySQL, Google Cloud Storage.  
- **Automatización y despliegue:** Docker, Cloud Run.  
- **Visualización de datos:** Power BI.  
- **Análisis de datos y Machine Learning:** Python (para el algoritmo de recomendación).  


## 2. Arquitectura del ETL

### 2.1 Extracción de Datos (Extract)
#### Fuentes de Datos
Los datos utilizados en este proyecto provienen de distintas fuentes:

- **Google Maps y Yelp:** Reseñas de negocios obtenidas de estas plataformas.
- **Archivos en Google Drive:** Los datos iniciales fueron proporcionados en carpetas de Google Drive en formatos JSON, Parquet y PKL.
- **Google Cloud Storage:** Posteriormente, los datos fueron migrados a Google Cloud Storage para su almacenamiento centralizado antes de la ejecución del ETL.

#### Proceso de Extracción
La extracción de datos en este proyecto se realizó de la siguiente manera:

1. Recepción de archivos en Google Drive en los formatos JSON, Parquet y PKL.
2. Carga manual a Google Cloud Storage, donde se almacenaron para su posterior procesamiento.
3. Descarga desde Google Cloud Storage a un entorno local, donde se ejecutó el proceso ETL en Visual Studio Code utilizando Python.

---

### 2.2 Transformación de Datos (Transform)
En esta etapa se realizaron diversas transformaciones para limpiar y estructurar los datos antes de su almacenamiento final.

#### Procesos de Transformación

1. **Eliminación de duplicados**
   - Se identificaron y eliminaron registros duplicados utilizando los campos:
     - `time` (marca de tiempo de la reseña)
     - `text` (contenido del comentario)
     - `user_id` (identificador del usuario)
   
   ```python
   alabama_filtrado.drop_duplicates(subset=["time", "text", "user_id"], inplace=True)
   alaska_filtrado.drop_duplicates(subset=["time", "text", "user_id"], inplace=True)
   arizona_filtrado.drop_duplicates(subset=["time", "text", "user_id"], inplace=True)
   ```

2. **Manejo de valores nulos**
   - Se identificaron valores nulos en los datos, aunque actualmente no hay estrategias explícitas de imputación o eliminación en el código disponible.
   - Se recomienda evaluar el impacto de los valores nulos antes de su eliminación o reemplazo.

3. **Conversión de formatos**
   - La columna `time`, almacenada en milisegundos, se convirtió a formato `datetime` para facilitar su análisis:
   
   ```python
   alabama_filtrado['time'] = pd.to_datetime(alabama_filtrado['time'], unit='ms')
   alaska_filtrado['time'] = pd.to_datetime(alaska_filtrado['time'], unit='ms')
   arizona_filtrado['time'] = pd.to_datetime(arizona_filtrado['time'], unit='ms')
   ```

4. **Selección y reordenación de columnas**
   - Se seleccionaron solo las columnas relevantes para optimizar la estructura de los datos:
     - `user_id`: Identificador del usuario
     - `name`: Nombre del restaurante
     - `time`: Fecha y hora de la reseña
     - `rating`: Calificación otorgada por el usuario
     - `text`: Contenido de la reseña
     - `gmap_id`: Identificador único del restaurante en Google Maps
     - `Estado`: Ubicación del restaurante
   
   ```python
   alabama_filtrado = alabama_filtrado[["user_id", "name", "time", "rating", "text", "gmap_id", "Estado"]]
   alaska_filtrado = alaska_filtrado[["user_id", "name", "time", "rating", "text", "gmap_id", "Estado"]]
   arizona_filtrado = arizona_filtrado[["user_id", "name", "time", "rating", "text", "gmap_id", "Estado"]]
   ```

#### Herramientas Utilizadas
- **Python:** Lenguaje de programación principal para la transformación de datos.
- **Pandas:** Biblioteca de manipulación de datos utilizada para la limpieza y estructuración.

---

### 2.3 Carga de Datos (Load)

#### Modelo de Almacenamiento y Justificación
Los datos transformados se almacenaron en:

- **MySQL (en local):** Base de datos relacional utilizada durante la fase inicial del ETL.
- **Google Cloud Storage y BigQuery:** Para almacenamiento y análisis en la nube.

#### Justificación de Elección del Modelo de Almacenamiento

1. **Facilidad de Desarrollo y Pruebas:** La ejecución en local permitió iteraciones rápidas sin costos adicionales de computación en la nube.
2. **Compatibilidad con MySQL:** Se eligió MySQL para la carga inicial por su estabilidad.
3. **Uso de Docker para Portabilidad:** Se está trabajando en la contenedorización del ETL.
4. **Uso de Google Cloud Storage y BigQuery:** Se considera BigQuery como destino final para almacenamiento y análisis escalable.
5. **Migración Progresiva a la Nube:** Se planea trasladar el ETL completamente a la nube una vez validado la eleccion con el cliente.

#### Destino Final de los Datos
- **Tablas en MySQL (local)**
- **Google Cloud Storage (intermedio antes de BigQuery)**
- **BigQuery (almacenamiento final y análisis de datos con la opcion de la nube)**

#### Formatos de Almacenamiento
Actualmente, los datos se almacenan en formato tabular dentro de MySQL. Sin embargo, con la opcion en la nube se considera el uso de **Parquet, JSON** o **tablas particionadas** para optimización del almacenamiento en BigQuery.


---

### 2.4 Carga Incremental
*(Pendiente de definir)*


## 3. Estructura de Datos

### Análisis del EER (Entidad-Relación Extendido)

El modelo EER define la estructura de la base de datos y su nivel de normalización. A continuación, se presentan los principales aspectos analizados:

#### 1. Claves Primarias y Tipos de Datos

- Se han definido los tipos de datos para cada atributo con el fin de optimizar la eficiencia y el almacenamiento.
- `gmap_id` se ha definido como clave primaria en la tabla **restaurantes**, asegurando la unicidad de cada restaurante.
- `gmap_id` también funciona como clave foránea en varias tablas, garantizando la integridad referencial y evitando inconsistencias en los datos.

#### 2. Relaciones y Normalización

- La tabla **misc** centraliza información sobre accesibilidad, medios de pago, popularidad y opciones de servicio, evitando redundancia de datos en otras tablas.
- La tabla **ubicacion** está vinculada con **restaurantes** a través de `gmap_id`, lo que permite manejar la información geográfica sin duplicaciones.
- Se mantiene una relación de muchos a muchos entre **restaurantes** y **categorias**, donde se han definido cinco claves foráneas (`categoria1` a `categoria5`). Sin embargo, esta estructura podría optimizarse con una tabla intermedia que maneje las relaciones de forma más eficiente.

#### 3. Tablas de Dominio o Catálogos

Se han creado tablas normalizadas para almacenar valores referenciales, lo que mejora la escalabilidad y evita la repetición de datos:

- **accesibilidad**
- **medios_de_pago**
- **opciones_de_servicio**
- **destacados**
- **publico**
- **popular**

Estas tablas permiten mantener un diseño normalizado y eficiente en términos de almacenamiento.

![Diagrama EER Copo de Nieve](Sprint2/powerbi/EER_Copo_de_Nieve.png)


---

### Análisis del DER - Modelo en Copo de Nieve

El modelo DER adoptado sigue la forma de **Copo de Nieve**, lo que significa que ha sido altamente normalizado para evitar redundancias. Este modelo presenta las siguientes características:

#### 1. Entidades Principales

- **restaurantes**: Contiene la información principal de cada restaurante, incluyendo `gmap_id`, `name`, `state`, número de valoraciones y su relación con categorías y ubicación.
- **ubicacion**: Almacena la dirección del restaurante con atributos como `address`, `latitud`, `longitud`, y se relaciona con **restaurantes** a través de `gmap_id`.
- **categorias**: Define las distintas categorías de los restaurantes y mantiene una relación con **restaurantes**.
- **misc**: Contiene atributos diversos como accesibilidad, medios de pago y crowd-levels (posible tabla de métricas), relacionándose con varias entidades.

#### 2. Entidades de Apoyo o Referenciales

- **opciones_de_servicio**, **medios_de_pago**, **publico**, **accesibilidad**, **destacados**, **popular**.

Estas tablas contienen valores categóricos normalizados, evitando redundancias en la base de datos y mejorando su organización.

![Diagrama DER - Copo de Nieve PBI](Sprint2/powerbi/DER%20-%20Copo%20de%20Nieve%20PBI.png)



---

### Modelo de Almacenamiento

Para la gestión de los datos, se ha considerado el uso de diferentes tecnologías de almacenamiento. A continuación, se describen las soluciones adoptadas:

#### 1. Data Warehouse

Se ha utilizado **BigQuery** como Data Warehouse para centralizar y analizar los datos transformados, tambien localmente por si esa es la opcion a elegir. BigQuery es una solución escalable y optimizada para consultas analíticas de grandes volúmenes de datos.

#### 2. Data Lake

**Google Cloud Storage** se ha empleado como un Data Lake, almacenando archivos en formatos **JSON**, **Parquet** y **Pickle**. Esta solución permite flexibilidad en el almacenamiento de datos sin necesidad de estructuración previa.

#### 3. Justificación de la Elección

La combinación de **Data Warehouse (BigQuery)** y **Data Lake (Google Cloud Storage)** permite:

- **Escalabilidad y procesamiento eficiente**: BigQuery maneja grandes volúmenes de datos y consultas analíticas de manera eficiente.
- **Flexibilidad en almacenamiento**: Cloud Storage permite almacenar archivos en diferentes formatos sin necesidad de transformaciones previas.
- **Optimización de costos**: Se evita el uso innecesario de recursos en la nube durante la etapa de desarrollo, reduciendo costos asociados al procesamiento y almacenamiento.

---

### Diccionario de Datos - Modelo EER

A continuación, se describe la estructura de cada tabla del modelo **Entidad-Relación Extendido (EER)**, especificando el nombre de la tabla, los atributos, su tipo de dato y una breve descripción de su función.


# Diccionario de Datos

| Nombre de la columna         | Tipo de dato | Descripción |
|-----------------------------|-------------|-------------|
| `business_id`               | STRING      | Identificador único del negocio. |
| `name`                      | STRING      | Nombre del negocio. |
| `address`                   | STRING      | Dirección del negocio. |
| `city`                      | STRING      | Ciudad donde se encuentra el negocio. |
| `state`                     | STRING      | Estado donde se encuentra el negocio. |
| `postal_code`               | STRING      | Código postal del negocio. |
| `latitude`                  | FLOAT       | Latitud de la ubicación del negocio. |
| `longitude`                 | FLOAT       | Longitud de la ubicación del negocio. |
| `stars`                     | FLOAT       | Calificación promedio del negocio. |
| `review_count`              | INT         | Número total de reseñas del negocio. |
| `is_open`                   | INT         | Indica si el negocio está abierto (1) o cerrado (0). |
| `categories`                | STRING      | Lista de categorías a las que pertenece el negocio. |
| `review_id`                 | STRING      | Identificador único de la reseña. |
| `user_id`                   | STRING      | Identificador único del usuario que hizo la reseña. |
| `stars_review`              | INT         | Calificación dada en la reseña. |
| `date`                      | DATE        | Fecha en la que se realizó la reseña. |
| `text`                      | STRING      | Texto de la reseña. |
| `useful`                    | INT         | Número de veces que la reseña fue marcada como útil. |
| `funny`                     | INT         | Número de veces que la reseña fue marcada como divertida. |
| `cool`                      | INT         | Número de veces que la reseña fue marcada como genial. |
| `user_name`                 | STRING      | Nombre del usuario que realizó la reseña. |
| `average_stars_user`        | FLOAT       | Calificación promedio dada por el usuario en todas sus reseñas. |
| `fans`                      | INT         | Número de seguidores del usuario. |
| `elite`                     | STRING      | Indica si el usuario es considerado "élite" en Yelp. |
| `compliments`               | INT         | Cantidad de cumplidos recibidos por el usuario. |
| `useful_user`               | INT         | Número de veces que las reseñas del usuario fueron marcadas como útiles. |
| `funny_user`                | INT         | Número de veces que las reseñas del usuario fueron marcadas como divertidas. |
| `cool_user`                 | INT         | Número de veces que las reseñas del usuario fueron marcadas como geniales. |



# Automatización del Pipeline

## 1. Descripción de la Automatización
Para la automatización del pipeline de procesamiento de datos, se ha implementado un flujo estructurado que permite la ingesta, validación, procesamiento y análisis de datos de manera eficiente.

### Características de la Automatización:
- **Ejecución Programada:** Se definen horarios y condiciones para la ejecución automática del pipeline.
- **Monitoreo y Registro de Ejecuciones:** Se facilita la observación en tiempo real y la auditoría de los procesos de ingesta y transformación.
- **Escalabilidad:** El diseño permite adaptarse al crecimiento del volumen de datos sin comprometer el rendimiento.
- **Integración con Servicios en la Nube:** Compatible con Google Cloud (BigQuery, Cloud Run, Cloud Storage) y otras plataformas.

## 2. Flujo de ejecución
Este pipeline representa el flujo de procesamiento de datos para el análisis de reseñas de negocios en EE.UU., asegurando que los datos sean cargados, procesados y utilizados para actualizar dashboards, algoritmos y generar nuevos insights.

### 2.1. Ingesta de Datos
- **Datos (Inputs):** Se recopilan datos desde diversas fuentes (APIs, bases de datos externas, archivos CSV en Cloud Storage, entre otros).
- **Carga en Cloud Run:** Un servicio en la nube recibe los datos y los preprocesa para su validación.
- **Trigger de verificación de fuentes:** Se ejecuta diariamente para comprobar si hay nuevos datos disponibles.

### 2.2. Validación y Carga Condicional
- **¿Están Cargados?:** Se verifica si los datos ya han sido incorporados previamente en el sistema.
  - Si los datos ya están cargados, no se realiza ninguna acción.
  - Si no están cargados, se procede a cargar solo los nuevos datos en la base de datos.

### 2.3. Procesamiento y Almacenamiento
- **Trigger de procesamiento:** Una vez cargados los nuevos datos, se activa el siguiente paso.
- **Actualización en BigQuery:** Los datos se almacenan y actualizan en la base de datos en la nube para su posterior análisis.

### 2.4. Actualización y Generación de Insights
- **Actualizar Dashboard:** Se reflejan los nuevos datos en las visualizaciones de negocio.
- **Actualizar Algoritmos:** Los modelos de Machine Learning se recalibran con la información más reciente.
- **Generación de nuevos análisis y recomendaciones:**
  - **Nuevo Análisis de Sentimientos:** Se actualiza el procesamiento de texto para evaluar la opinión de los usuarios.
  - **Nuevas Recomendaciones:** Se generan sugerencias basadas en los nuevos datos procesados.

### 2.5. Generación de Resultados
- **Nuevos Outputs:** Se almacenan los resultados del análisis de sentimientos y las recomendaciones finales en un repositorio accesible para su consulta y análisis posterior.

## 3. Resumen del Pipeline Conceptual
1. **Ingesta:** Obtención de datos desde fuentes externas.
2. **Validación:** Comprobación y carga condicional de datos nuevos.
3. **Procesamiento:** Transformación de datos y almacenamiento en BigQuery.
4. **Análisis y Modelado:** Aplicación de Machine Learning y generación de insights.
5. **Resultados:** Actualización de dashboards y almacenamiento de predicciones y análisis.

Este flujo de trabajo garantiza que los datos estén siempre actualizados, mejorando la calidad del análisis y la toma de decisiones en función de las tendencias del mercado.

![Diagrama Pipeline Conceptual]( "Sprint2/powerbi/Pipeline Conceptual.png")



## 4. Workflow del Proyecto  

### Diagrama de flujo del proceso  
El siguiente diagrama muestra cómo interactúan las distintas partes del pipeline, desde la ingesta de datos hasta la actualización del dashboard. Se contemplan dos enfoques para la ejecución del flujo de trabajo:  

1. **Opción en la nube:** Utilizando servicios gestionados para el almacenamiento, procesamiento y análisis de los datos.  
2. **Opción local:** Ejecutando todo el proceso en infraestructura propia sin depender de servicios en la nube.  

En ambos casos, el objetivo es garantizar la disponibilidad y calidad de los datos para la toma de decisiones.  

### Tecnologías y herramientas utilizadas  

#### **Opción en la nube:**  
1. **Cloud Storage:** Almacena temporalmente los datos recopilados desde diferentes fuentes.  
2. **Cloud Run:** Ejecuta los procesos de validación y transformación de los datos antes de enviarlos a la base de datos.  
3. **BigQuery:** Almacena y organiza los datos procesados para su posterior análisis.  
4. **Herramienta de visualización (Dashboard):** Permite la exploración y monitoreo de los datos a partir de la información almacenada en BigQuery.  

#### **Opción local:**  
1. **Almacenamiento en disco o servidor local:** Se utiliza como repositorio de datos en lugar de Cloud Storage.  
2. **Procesamiento en máquinas locales:** Se pueden emplear scripts en Python, SQL o herramientas como Apache Airflow para la transformación y validación de los datos.  
3. **Base de datos local:** PostgreSQL, MySQL o cualquier otro sistema de gestión de bases de datos para almacenar los datos procesados.  
4. **Dashboard en entorno local:** Herramientas como Power BI o Metabase pueden utilizarse para la visualización de los datos.  

Este flujo de trabajo, ya sea en la nube o en local, permite que los datos sean procesados y analizados de manera eficiente, asegurando su disponibilidad para la toma de decisiones.  

![Diagrama Flujo de Trabajo](Sprint2/images/Flujo%20de%20Trabajo%20(1).png)
