import mysql.connector

# Configuración de conexión a MySQL
config = {
    "host": "localhost",
    "user": "root",  # Modificar según tu configuración
    "password": "tu_contraseña",  # Modificar según tu configuración
    "database": "Analisis_Total"
}

# Sentencias SQL
queries = [
    # Creación de tabla temporal para carga incremental de restaurantes
    """
    CREATE TABLE IF NOT EXISTS restaurantes_carga_incremental(
        gmap_id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(250),
        state VARCHAR(50),
        promedio FLOAT,
        valoraciones INT,
        categoria1 FLOAT,
        categoria2 FLOAT,
        categoria3 FLOAT,
        categoria4 FLOAT,
        categoria5 FLOAT
    );
    """,
    
    # Carga de datos en la tabla temporal de restaurantes
    """
    LOAD DATA INFILE 'csv_dir = "/data/Datos_Limpios/metadata/restaurantes.csv'
    INTO TABLE restaurantes_carga_incremental
    CHARACTER SET utf8mb4 
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    """,

    # Transformación de datos (NULL en lugar de 0)
    """
    UPDATE restaurantes_carga_incremental
    SET 
        categoria1 = NULLIF(categoria1, 0),
        categoria2 = NULLIF(categoria2, 0),
        categoria3 = NULLIF(categoria3, 0),
        categoria4 = NULLIF(categoria4, 0),
        categoria5 = NULLIF(categoria5, 0);
    """,

    # Inserción de nuevos registros en la tabla principal
    """
    INSERT INTO restaurantes
    SELECT * FROM restaurantes_carga_incremental
    WHERE gmap_id NOT IN (SELECT gmap_id FROM restaurantes);
    """,

    # Vaciar tabla temporal
    "TRUNCATE TABLE restaurantes_carga_incremental;",

    # Creación de tabla temporal para ubicación
    """
    CREATE TABLE IF NOT EXISTS ubicacion_carga_incremental(
        gmap_id VARCHAR(100),
        address VARCHAR(550),
        latitud DECIMAL(10,6),
        longitud DECIMAL(10,6)
    );
    """,

    # Carga de datos en tabla temporal de ubicaciones
    """
    LOAD DATA INFILE "csv_dir = "/data/Datos_Limpios/metadata/direcciones.csv"
    INTO TABLE ubicacion_carga_incremental
    CHARACTER SET utf8mb4 
    FIELDS TERMINATED BY ',' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    """,

    # Inserción de nuevos registros en la tabla principal
    """
    INSERT INTO ubicacion
    SELECT * FROM ubicacion_carga_incremental
    WHERE gmap_id NOT IN (SELECT gmap_id FROM ubicacion);
    """,

    # Vaciar tabla temporal
    "TRUNCATE TABLE ubicacion_carga_incremental;",

    # Creación de tabla temporal para MISC
    """
    CREATE TABLE IF NOT EXISTS misc_carga_incremental(
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
        highlights_1 INT
    );
    """,

    # Carga de datos en tabla temporal de MISC
    """
    LOAD DATA INFILE 'csv_dir = "/data/Datos_Limpios/metadata/metadata/MISC.csv'
    INTO TABLE misc_carga_incremental
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;
    """,

    # Transformación de datos (NULL en lugar de 0)
    """
    UPDATE misc_carga_incremental
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
    """,

    # Inserción de nuevos registros en la tabla principal
    """
    INSERT INTO misc
    SELECT * FROM misc_carga_incremental
    WHERE gmap_id NOT IN (SELECT gmap_id FROM misc);
    """,

    # Vaciar tabla temporal
    "TRUNCATE TABLE misc_carga_incremental;"
]

try:
    # Conectar a MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a MySQL")

    # Ejecutar cada consulta en orden
    for query in queries:
        try:
            cursor.execute(query)
            print(f"✅ Ejecución correcta: {query.split(';')[0][:50]}...")  # Mostrar parte de la consulta
        except mysql.connector.Error as e:
            print(f"⚠️ Error en consulta: {e}")

    # Confirmar cambios
    conn.commit()
    print("💾 Todos los cambios han sido guardados en MySQL")

except mysql.connector.Error as e:
    print(f"⚠️ Error en la conexión a MySQL: {e}")

finally:
    # Cerrar conexión
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
    print("🔌 Conexión cerrada")
