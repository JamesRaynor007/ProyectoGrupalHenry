import mysql.connector

# Configuración de la conexión a MySQL
config = {
    "host": "localhost",
    "user": "root",  # Cambia por tu usuario de MySQL
    "password": "tu_contraseña",  # Cambia por tu contraseña de MySQL
    "database": "Analisis_Total"
}

# Lista de sentencias ALTER TABLE para agregar claves foráneas
alter_queries = [
    "ALTER TABLE MISC ADD CONSTRAINT fk_service_option_1_fk FOREIGN KEY (service_option_1) REFERENCES opciones_de_servicio(id_opcion);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_service_option_2_fk FOREIGN KEY (service_option_2) REFERENCES opciones_de_servicio(id_opcion);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_accessibility_1_fk FOREIGN KEY (accessibility_1) REFERENCES accesibilidad(id_accesibilidad);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_accessibility_2_fk FOREIGN KEY (accessibility_2) REFERENCES accesibilidad(id_accesibilidad);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_popular_for_1_fk FOREIGN KEY (popular_for_1) REFERENCES popular(id_popular);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_popular_for_2_fk FOREIGN KEY (popular_for_2) REFERENCES popular(id_popular);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_popular_for_3_fk FOREIGN KEY (popular_for_3) REFERENCES popular(id_popular);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_crowd_1_fk FOREIGN KEY (crowd_1) REFERENCES publico(id_publico);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_crowd_2_fk FOREIGN KEY (crowd_2) REFERENCES publico(id_publico);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_payments_1_fk FOREIGN KEY (payments_1) REFERENCES medios_de_pago(id_medios_de_pago);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_payments_2_fk FOREIGN KEY (payments_2) REFERENCES medios_de_pago(id_medios_de_pago);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_payments_3_fk FOREIGN KEY (payments_3) REFERENCES medios_de_pago(id_medios_de_pago);",
    "ALTER TABLE MISC ADD CONSTRAINT fk_highlights_1_fk FOREIGN KEY (highlights_1) REFERENCES destacados(id_destacado);"
]

try:
    # Conectar a MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a MySQL")

    # Seleccionar la base de datos
    cursor.execute("USE Analisis_Total;")
    
    # Agregar claves foráneas
    for query in alter_queries:
        try:
            cursor.execute(query)
            print(f"🔗 Clave foránea agregada correctamente: {query.split('FOREIGN KEY')[0].strip()}")
        except mysql.connector.Error as e:
            print(f"⚠️ Error agregando clave foránea: {e}")

    # Confirmar cambios
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
