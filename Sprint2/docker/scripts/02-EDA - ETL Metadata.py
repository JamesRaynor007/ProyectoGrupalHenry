import os
import glob
import pandas as pd
import numpy as np
import time

def cargar_metadata(json_dir):
    """Carga archivos JSON desde un directorio y los combina en un DataFrame."""
    dataframes = []
    json_files = glob.glob(os.path.join(json_dir, '*.json'))
    for json_file in json_files:
        try:
            if os.path.getsize(json_file) > 0:
                df = pd.read_json(json_file, lines=True)
                dataframes.append(df)
            else:
                print(f"⚠️ Archivo vacío: {json_file}")
        except ValueError as e:
            print(f"⚠️ Error al leer {json_file}: {e}")
    
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        raise ValueError("❌ No se pudieron cargar datos desde los JSONs.")

def limpiar_metadata(metadata):
    """Limpia y transforma la metadata cruda."""
    metadata["state"] = metadata["address"].str.extract(r'\b([A-Z]{2})\b')
    valid_states = set(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 
                        'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
                        'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 
                        'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 
                        'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 
                        'WY'])
    metadata = metadata[metadata['state'].isin(valid_states)]
    return metadata

def filtrar_categorias(metadata):
    """Filtra los datos para incluir solo categorías relevantes a restaurantes."""
    metadata["category"] = metadata["category"].apply(lambda x: x if isinstance(x, list) else [])
    df_categories = metadata.explode("category")
    restaurant_keywords = {'restaurant', 'café', 'diner', 'bistro', 'food truck', 'takeout', 'catering', 'pizzeria', 'bar', 'grill', 'buffet', 'seafood', 'steakhouse', 'vegan', 'bakery'}
    return df_categories[df_categories['category'].str.lower().isin(restaurant_keywords)]

def guardar_csv(df, path, nombre):
    """Guarda un DataFrame en un archivo CSV."""
    os.makedirs(path, exist_ok=True)  # Asegura que el directorio exista antes de guardar
    df.to_csv(os.path.join(path, nombre), index=False)
    print(f"✅ Archivo guardado: {os.path.join(path, nombre)}")

def main():
    """Función principal para ejecutar el script completo."""
    inicio = time.time()
    current_dir = "/data"
    json_dir = os.path.join(current_dir, 'google', 'metadata')
    output_dir = os.path.join(current_dir, "Datos_Limpios", "metadata")  # Definir output_dir correctamente

    try:
        print("📂 Cargando metadata...")
        metadata = cargar_metadata(json_dir)

        print("🧹 Limpiando datos...")
        metadata = limpiar_metadata(metadata)

        print("🔎 Filtrando categorías...")
        metadata_filtrado = filtrar_categorias(metadata)  # Asignar metadata_filtrado antes de modificarlo
        
        print("🔄 Renombrando columna 'state' a 'Estado'...")
        metadata_filtrado.rename(columns={"state": "Estado"}, inplace=True)

        print("💾 Guardando resultados...")
        guardar_csv(metadata_filtrado, output_dir, "restaurantes.csv")

        fin = time.time()
        print(f"✅ ¡Proceso completado en {(fin - inicio) / 60:.2f} minutos!")

    except Exception as e:
        print(f"❌ Error en la ejecución: {e}")

if __name__ == "__main__":
    main()
