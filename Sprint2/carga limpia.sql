DROP DATABASE Analisis_Total;

CREATE DATABASE IF NOT EXISTS Analisis_Total;

USE Analisis_Total;

DROP TABLE restaurantes;

CREATE TABLE IF NOT EXISTS restaurantes(
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

LOAD DATA INFILE 'D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/restaurantes.csv'
INTO TABLE restaurantes
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE ubicacion;

CREATE TABLE IF NOT EXISTS ubicacion(
    gmap_id VARCHAR(100),
    address VARCHAR(550),
    latitud DECIMAL(10,6),
    longitud DECIMAL(10,6),
    FOREIGN KEY (gmap_id) REFERENCES restaurantes(gmap_id)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/direcciones.csv"
INTO TABLE ubicacion
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE categorias;

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50)
);

SELECT * FROM categorias;

LOAD DATA INFILE 'D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/categorias.csv'
INTO TABLE categorias
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@dummy,nombre_categoria);

CREATE TABLE IF NOT EXISTS opciones_de_servicio(
    id_opcion INT PRIMARY KEY,
    descripcion_opcion VARCHAR(20)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/opciones de servicio.csv"
INTO TABLE opciones_de_servicio
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE IF NOT EXISTS accesibilidad(
    id_accesibilidad INT PRIMARY KEY,
    descripcion_accesibilidad VARCHAR(50)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/accesibilidad.csv"
INTO TABLE accesibilidad
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE IF NOT EXISTS popular(
    id_popular INT PRIMARY KEY,
    descripcion_popular VARCHAR(50)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/popular por.csv"
INTO TABLE popular
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE IF NOT EXISTS publico(
    id_publico INT PRIMARY KEY,
    descripcion_publico VARCHAR(20)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/publico.csv"
INTO TABLE publico
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;



CREATE TABLE IF NOT EXISTS medios_de_pago(
    id_medios_de_pago INT PRIMARY KEY,
    descripcion_medios_de_pago VARCHAR(30)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/medio de pago.csv"
INTO TABLE medios_de_pago
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE IF NOT EXISTS destacados(
    id_destacado INT PRIMARY KEY,
    descripcion_destacado VARCHAR(30)
);

LOAD DATA INFILE "D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC/destacados.csv"
INTO TABLE destacados
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE MISC;

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



LOAD DATA INFILE 'D:/2023/aleca/OneDrive/Escritorio/Ale/2023/Exiting - Success/Proyectos/Data Science/Data Science/01-Parte 2 - Henry Labs/05-Proyecto Final/SPRINT 2/LOCAL/Datos Limpios/metadata/MISC.csv'
INTO TABLE MISC
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

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
    highlights_1 = NULLIF(highlights_1, 0)
;
    
ALTER TABLE MISC 
ADD CONSTRAINT fk_service_option_1_fk FOREIGN KEY (service_option_1) REFERENCES opciones_de_servicio(id_opcion), 
ADD CONSTRAINT fk_service_option_2_fk FOREIGN KEY (service_option_2) REFERENCES opciones_de_servicio(id_opcion), 
ADD CONSTRAINT fk_accessibility_1_fk FOREIGN KEY (accessibility_1) REFERENCES accesibilidad(id_accesibilidad), 
ADD CONSTRAINT fk_accessibility_2_fk FOREIGN KEY (accessibility_2) REFERENCES accesibilidad(id_accesibilidad), 
ADD CONSTRAINT fk_popular_for_1_fk FOREIGN KEY (popular_for_1) REFERENCES popular(id_popular), 
ADD CONSTRAINT fk_popular_for_2_fk FOREIGN KEY (popular_for_2) REFERENCES popular(id_popular), 
ADD CONSTRAINT fk_popular_for_3_fk FOREIGN KEY (popular_for_3) REFERENCES popular(id_popular), 
ADD CONSTRAINT fk_crowd_1_fk FOREIGN KEY (crowd_1) REFERENCES publico(id_publico), 
ADD CONSTRAINT fk_crowd_2_fk FOREIGN KEY (crowd_2) REFERENCES publico(id_publico), 
ADD CONSTRAINT fk_payments_1_fk FOREIGN KEY (payments_1) REFERENCES medios_de_pago(id_medios_de_pago), 
ADD CONSTRAINT fk_payments_2_fk FOREIGN KEY (payments_2) REFERENCES medios_de_pago(id_medios_de_pago), 
ADD CONSTRAINT fk_payments_3_fk FOREIGN KEY (payments_3) REFERENCES medios_de_pago(id_medios_de_pago), 
ADD CONSTRAINT fk_highlights_1_fk FOREIGN KEY (highlights_1) REFERENCES destacados(id_destacado);



UPDATE restaurantes
SET 
    categoria1 = NULLIF(categoria1, 0),
    categoria2 = NULLIF(categoria2, 0),
    categoria3 = NULLIF(categoria3, 0),
    categoria4 = NULLIF(categoria4, 0),
    categoria5 = NULLIF(categoria5, 0);


ALTER TABLE restaurantes
ADD CONSTRAINT fk_categoria1 FOREIGN KEY (categoria1) REFERENCES categorias(id_categoria),
ADD CONSTRAINT fk_categoria2 FOREIGN KEY (categoria2) REFERENCES categorias(id_categoria),
ADD CONSTRAINT fk_categoria3 FOREIGN KEY (categoria3) REFERENCES categorias(id_categoria),
ADD CONSTRAINT fk_categoria4 FOREIGN KEY (categoria4) REFERENCES categorias(id_categoria),
ADD CONSTRAINT fk_categoria5 FOREIGN KEY (categoria5) REFERENCES categorias(id_categoria);