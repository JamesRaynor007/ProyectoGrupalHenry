Bueno, la idea va a ser realizar el análisis de los datos que vienen en los datasets de YELP y de Google. 

Vamos a tratar de pasarla en limpio los datos que van a ser necesarios para realizar el algoritmo de Machine Learning y proveer origen a los distintos dashboard que vamos a implementar. 

El primer concepto inicia con el análisis de los datos de YELP para identificar a aquellos que serán utilizados para alimentar el dashboard. 

Tiempos, intentarán encontrar relaciones para la posibilidad de desplegar tablas en las cual es encontremos claves primarias y foráneas para relacionarlas y tener mayor cantidad de información disponible. Esto podría beneficiar la utilización de indicadores más precisos. 

Una vez realizado este procedimiento, se creará el Código script que va a utilizar los datos crudos previamente cargados para generar los nuevos datos limpios que van a ser almacenados en google cloud storage. 

En segunda instancia, vamos a utilizar los datos de Google Maps. Estos datos contienen la meta data y los reviews de los diferentes Estados. 

Por un lado, vamos a utilizar solamente los datos de cuatro Estados para alimentar nuestro algoritmo de Machine Learning. 

Estos cuatro Estados van a ser los más representativos de la población de Estados Unidos. 
Siendo nuestro primer filtro respecto a reviews. 

Al realizar este filtro y en conjunto con los datos de Metadata vamos a estar generando los nuevos data sets a ser almacenados como datos limpios. 

Por otro lado, vamos a estar utilizando los reviews de todos los Estados para generar los data sets necesarios que puedan alimentar los dashboard respecto a indicadores que necesitan tener la totalidad de las reviews de todos los Estados para determinar los promedios de la industria. 
