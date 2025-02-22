from __future__ import print_function
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import datetime

# Configura tus credenciales
SERVICE_ACCOUNT_FILE = 'proyecto-resto-score-f02454a3aee3.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# IDs de las carpetas de Google Drive
DRIVE_FOLDER_ID_YELP = '1TI-SsMnZsNP6t930olEEWbBQdo_yuIZF'
DRIVE_FOLDER_ID_GOOGLE_METADATA = '1olnuKLjT8W2QnCUUwh8uDuTTKVZyxQ0Z'
DRIVE_FOLDER_ID_GOOGLE_REVIEWS = '19QNXr_BcqekFNFNYlKd0kcTXJ0Zg7lI6'
DRIVE_FOLDER_ID_MACROECONOMIA = '1sFdg3PtGYqIaV2wpS3XSzD6CVP41etT6'  # ID de la nueva carpeta

def obtener_fecha_hora_actual():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def descargar_archivos_de_google_drive(directorio_destino, folder_id):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('drive', 'v3', credentials=creds)

    # Obtener archivos y carpetas en una carpeta específica
    query = f"'{folder_id}' in parents"
    
    # Inicializa el token de la siguiente página
    page_token = None
    
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    while True:
        results = service.files().list(q=query, pageSize=10, fields="nextPageToken, files(id, name, mimeType, modifiedTime)", pageToken=page_token).execute()
        items = results.get('files', [])
        page_token = results.get('nextPageToken')

        if not items:
            print(f'[{obtener_fecha_hora_actual()}] No se encontraron archivos en la carpeta {folder_id}.')
            break
        
        for item in items:
            item_path = os.path.join(directorio_destino, item['name'])
            modified_time = item['modifiedTime']

            # Convertir la hora de modificación de Google Drive a un objeto datetime
            modified_time = datetime.datetime.fromisoformat(modified_time[:-1])  # Eliminar la 'Z' del final

            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Si el item es una carpeta, llamamos recursivamente
                print(f'[{obtener_fecha_hora_actual()}] Accediendo a la carpeta: {item["name"]}')
                descargar_archivos_de_google_drive(item_path, item['id'])
            else:
                # Verificar si el archivo ya existe y su fecha de modificación
                if os.path.exists(item_path):
                    local_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                    if local_modified_time >= modified_time:
                        print(f'[{obtener_fecha_hora_actual()}] El archivo {item["name"]} está actualizado. Saltando descarga.')
                        continue  # Saltar este archivo si ya está actualizado

                print(f'[{obtener_fecha_hora_actual()}] Descargando: {item["name"]}')
                request = service.files().get_media(fileId=item['id'])
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)

                done = False
                while not done:
                    try:
                        status, done = downloader.next_chunk()
                        print(f'[{obtener_fecha_hora_actual()}] Descargado {int(status.progress() * 100)}%.')
                    except Exception as e:
                        print(f'[{obtener_fecha_hora_actual()}] Error al descargar {item["name"]}: {str(e)}')
                        break
                
                fh.seek(0)

                # Guardar el archivo en el directorio de destino
                with open(item_path, 'wb') as f:
                    f.write(fh.read())

        # Si no hay más tokens de página, sal del bucle
        if not page_token:
            break


if __name__ == '__main__':
    carpeta_base = r'D:\2023\aleca\OneDrive\Escritorio\Ale\2023\Exiting - Success\Proyectos\Data Science\Data Science\01-Parte 2 - Henry Labs\05-Proyecto Final\SPRINT 2\LOCAL'
    
    # Descargar archivos desde la carpeta Yelp
    directorio_destino_yelp = os.path.join(carpeta_base, 'yelp')
    descargar_archivos_de_google_drive(directorio_destino_yelp, DRIVE_FOLDER_ID_YELP)
    
    # Descargar archivos desde la carpeta Google Metadata
    directorio_destino_metadata = os.path.join(carpeta_base, 'google/metadata')
    descargar_archivos_de_google_drive(directorio_destino_metadata, DRIVE_FOLDER_ID_GOOGLE_METADATA)

    # Descargar archivos desde la carpeta Google Reviews
    directorio_destino_reviews = os.path.join(carpeta_base, 'google/reviews')
    descargar_archivos_de_google_drive(directorio_destino_reviews, DRIVE_FOLDER_ID_GOOGLE_REVIEWS)

    # Descargar archivos desde la carpeta Macroeconomía
    directorio_destino_macroeconomia = os.path.join(carpeta_base, 'Macroeecnomía')
    descargar_archivos_de_google_drive(directorio_destino_macroeconomia, DRIVE_FOLDER_ID_MACROECONOMIA)
