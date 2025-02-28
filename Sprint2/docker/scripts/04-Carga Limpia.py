import mysql.connector
import os

# Configuración de la conexión a MySQL
config = {
    "host": "localhost",
    "user": "root",  # Cambia por tu usuario de MySQL
    "password": "tu_contraseña",  # Cambia por tu contraseña de MySQL
    "database": "Analisis_Total"
}

# Ruta donde están los archivos CSV
csv_dir = "/data/Datos_Limpios/metadata"

# Conectar a MySQL
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a MySQL")

    # Crear base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS Analisis_Total;")
    cursor.execute("USE Analisis_Total;")
    print("📂 Base de datos 'Analisis_Total' seleccionada")

    # Crear tablas
    queries = [
        """
        CREATE TABLE IF NOT EXISTS restaurantes (
            gmap_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(250),
            state VARCHAR(50),
            promedio FLOAT,
            valoraciones INT,
            categoria1 INT,
            categoria2 INT,
            categoria3 INT,
            categoria4 INT,
            categoria5 INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ubicacion (
            gmap_id VARCHAR(100),
            address VARCHAR(550),
            latitud DECIMAL(10,6),
            longitud DECIMAL(10,6),
            FOREIGN KEY (gmap_id) REFERENCES restaurantes(gmap_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            nombre_categoria VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS opciones_de_servicio (
            id_opcion INT PRIMARY KEY,
            descripcion_opcion VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS accesibilidad (
            id_accesibilidad INT PRIMARY KEY,
            descripcion_accesibilidad VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS popular (
            id_popular INT PRIMARY KEY,
            descripcion_popular VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS publico (
            id_publico INT PRIMARY KEY,
            descripcion_publico VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS medios_de_pago (
            id_medios_de_pago INT PRIMARY KEY,
            descripcion_medios_de_pago VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS destacados (
            id_destacado INT PRIMARY KEY,
            descripcion_destacado VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS MISC (
            gmap_id VARCHAR(255) PRIMARY KEY,
            service_option_1 INT,
            service_option_2 INT,
            accessibility_1 INT,
            accessibility_2 INT,
            popular_for_1 INT,
            popular_for_2 INT,
            popular_for_3 INT,
            crowd_1 INT,
            crowd_2 INT,
            payments_1 INT,
            payments_2 INT,
            payments_3 INT,
            highlights_1 INT,
            FOREIGN KEY (gmap_id) REFERENCES restaurantes(gmap_id)
        );
        """
    ]

    # Ejecutar las consultas de creación de tablas
    for query in queries:
        cursor.execute(query)
    print("🛠️ Tablas creadas correctamente")

    # Archivos y tablas a cargar
    files_and_tables = [
        ("restaurantes.csv", "restaurantes"),
        ("direcciones.csv", "ubicacion"),
        ("categorias.csv", "categorias"),
        ("MISC.csv", "MISC"),
        ("MISC/opciones de servicio.csv", "opciones_de_servicio"),
        ("MISC/accesibilidad.csv", "accesibilidad"),
        ("MISC/popular por.csv", "popular"),
        ("MISC/publico.csv", "publico"),
        ("MISC/medio de pago.csv", "medios_de_pago"),
        ("MISC/destacados.csv", "destacados")
    ]

    # Cargar datos en MySQL desde los archivos CSV
    for file_name, table_name in files_and_tables:
        file_path = os.path.join(csv_dir, file_name)
        file_path = file_path.replace("\\", "/")
        if os.path.exists(file_path):
            load_query = """
                LOAD DATA INFILE '{}'  
                INTO TABLE {}
                CHARACTER SET utf8mb4
                FIELDS TERMINATED BY ','
                OPTIONALLY ENCLOSED BY '"'
                LINES TERMINATED BY '\\n'
                IGNORE 1 LINES;
                """.format(file_path, table_name)
            try:
                cursor.execute(load_query)
                print(f"📄 Datos cargados en '{table_name}' desde {file_name}")
            except mysql.connector.Error as e:
                print(f"❌ Error cargando {file_name}: {e}")
        else:
            print(f"⚠️ Archivo no encontrado: {file_path}")

    # Actualizar columnas para reemplazar 0 con NULL en restaurantes y MISC
    update_queries = [
        """
        UPDATE restaurantes
        SET 
            categoria1 = NULLIF(categoria1, 0),
            categoria2 = NULLIF(categoria2, 0),
            categoria3 = NULLIF(categoria3, 0),
            categoria4 = NULLIF(categoria4, 0),
            categoria5 = NULLIF(categoria5, 0);
        """,
        """
        UPDATE MISC
        SET 
            service_option_1 = NULLIF(service_option_1, 0),
            service_option_2 = NULLIF(service_option_2, 0),
            accessibility_1 = NULLIF(accessibility_1, 0),
            accessibility_2 = NULLIF(accessibility_2, 0),
            popular_for_1 = NULLIF(popular_for_1, 0),
            popular_for_2 = NULLIF(popular_for_2, 0),
            popular_for_3 = NULLIF(popular_for_3, 0),
            crowd_1 = NULLIF(crowd_1, 0),
            crowd_2 = NULLIF(crowd_2, 0),
            payments_1 = NULLIF(payments_1, 0),
            payments_2 = NULLIF(payments_2, 0),
            payments_3 = NULLIF(payments_3, 0),
            highlights_1 = NULLIF(highlights_1, 0);
        """
    ]

    for query in update_queries:
        cursor.execute(query)
    print("✅ Valores actualizados en 'restaurantes' y 'MISC'")

    # Confirmar los cambios
    conn.commit()
    print("💾 Cambios guardados en la base de datos")

except mysql.connector.Error as e:
    print(f"⚠️ Error en la conexión a MySQL: {e}")

finally:
    # Cerrar la conexión
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
    print("🔌 Conexión cerrada")
