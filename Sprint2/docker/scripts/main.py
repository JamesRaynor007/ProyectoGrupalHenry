import subprocess
import time

def ejecutar_script(script):
    """Ejecuta un script Python dentro del contenedor y muestra su salida."""
    print(f"\n🚀 Ejecutando {script}...\n")
    proceso = subprocess.run(["python", f"/app/scripts/{script}"], capture_output=True, text=True)
    
    # Imprimir la salida del script
    if proceso.returncode == 0:
        print(f"✅ {script} ejecutado correctamente\n")
    else:
        print(f"❌ Error en {script}\n")
        print(proceso.stdout)
        print(proceso.stderr)
        exit(1)  # Detener la ejecución si hay un error

# **1️⃣ Descarga de archivos desde Google Drive**
ejecutar_script("01-carga cruda.py")

# **2️⃣ Procesamiento ETL - Metadata**
ejecutar_script("02-EDA - ETL Metadata.py")

# **3️⃣ Procesamiento ETL - Reviews**
ejecutar_script("03-EDA - ETL Reviews.py")

# **4️⃣ Conexión a MySQL**
time.sleep(10)  # Esperar 10 segundos para asegurar que MySQL esté activo
ejecutar_script("Conexion MySQL.py")

# **5️⃣ Cargar datos limpios en MySQL**
ejecutar_script("04-Carga Limpia.py")

# **6️⃣ Crear claves foráneas en MySQL**
ejecutar_script("05-Claves Foraneas.py")

# **7️⃣ Carga incremental de datos en MySQL**
ejecutar_script("Carga Incremental.py")

print("\n🎉 Todo el proceso se ejecutó correctamente 🎉")
