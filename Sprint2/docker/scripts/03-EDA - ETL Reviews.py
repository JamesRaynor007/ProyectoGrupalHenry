import pandas as pd
import os
import glob

# Obtener directorio base
current_dir = "/data"

# Cargar los restaurantes
csv_file_path = "/data/Datos_Limpios/metadata/restaurantes.csv"

if os.path.isfile(csv_file_path):
    restaurantes = pd.read_csv(csv_file_path)
    print("Archivo cargado correctamente.")
    if "gmap_id" not in restaurantes.columns or "Estado" not in restaurantes.columns:
        raise KeyError("El archivo de restaurantes no contiene las columnas esperadas: 'gmap_id' y 'Estado'.")
else:
    raise FileNotFoundError(f"El archivo {csv_file_path} no existe.")

# Seleccionamos solo las columnas necesarias
restaurantes = restaurantes[["gmap_id", "Estado"]]

# Lista completa de los estados de EE.UU.
estados = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "District_of_Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New_Hampshire",
    "New_Jersey", "New_Mexico", "New_York", "North_Carolina", "North_Dakota", 
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode_Island", "South_Carolina", 
    "South_Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", 
    "Washington", "West_Virginia", "Wisconsin", "Wyoming"
]

# Directorio de salida
ruta_datos_limpios = os.path.join(current_dir, "Datos Limpios")
ruta_reviews = os.path.join(ruta_datos_limpios, "reviews")

# Crear carpetas si no existen
os.makedirs(ruta_reviews, exist_ok=True)

def procesar_estado(estado, index):
    """
    Función para cargar, limpiar y guardar las reseñas de un estado específico.
    """
    json_dir = os.path.join(current_dir, 'google', 'reviews', f'review-{estado}')
    
    if not os.path.exists(json_dir):
        print(f"El directorio {json_dir} no existe. Saltando {estado}.")
        return

    dataframes = []
    json_files = glob.glob(os.path.join(json_dir, '*.json'))

    if not json_files:
        print(f"No se encontraron archivos JSON en {json_dir}. Saltando {estado}.")
        return

    for json_file in json_files:
        try:
            df = pd.read_json(json_file, lines=True)
            dataframes.append(df)
        except ValueError as e:
            print(f"Error al leer el archivo {json_file}: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al leer {json_file}: {e}")

    if not dataframes:
        print(f"No se pudieron cargar DataFrames de los archivos JSON de {estado}.")
        return

    df_estado = pd.concat(dataframes, ignore_index=True)

    if "gmap_id" not in df_estado.columns:
        print(f"El DataFrame de {estado} no contiene la columna 'gmap_id'. Saltando.")
        return

    # Merge con restaurantes
    df_estado_filtrado = df_estado.merge(restaurantes, on="gmap_id", how="left")

    if "time" not in df_estado_filtrado.columns:
        print(f"El DataFrame de {estado} no contiene la columna 'time'. Saltando.")
        return

    # Convertir a datetime
    df_estado_filtrado['time'] = pd.to_datetime(df_estado_filtrado['time'], unit='ms', errors='coerce')

    # Selección de columnas
    columnas_necesarias = ["user_id", "name", "time", "rating", "text", "gmap_id", "Estado"]
    df_estado_filtrado = df_estado_filtrado[columnas_necesarias]

    # Eliminar duplicados
    df_estado_filtrado.drop_duplicates(subset=["time", "text", "user_id"], inplace=True)

    # Guardar CSV limpio
    nombre_archivo = f"{str(index + 1).zfill(2)}-{estado.lower().replace(' ', '_')}.csv"
    df_estado_filtrado.to_csv(os.path.join(ruta_reviews, nombre_archivo), index=False, escapechar='\\', quoting=1)
    print(f"Datos de {estado} procesados y guardados en {nombre_archivo}.")

# Procesar todos los estados
for i, estado in enumerate(estados):
    procesar_estado(estado, i)