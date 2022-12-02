# Reporte_MavenPizzas_pdf
El repositorio contiene los siguientes ficheros:

- etl.py (programa a ejecutar)
- analisis_de_los_datos.py (programa a ejecutar)
- Analisis_datos.xml
- requirements.txt
- crearpdf.py (librería)

- Informe_powerby.pbix
- Informe_prowerby.png
- Ingredientes_bottom.jpg
- Ingredientes_top.jpg
- logo.jpg
- Pizzas_bottom.jpg
- Pizzas_top.jpg

- Informe.pdf
- Datos limpios.csv
- Fechas_limpias.csv
- data_dictionary.csv
- order_details.csv
- orders.csv
- pizza_types.csv
- pizzas.csv

### etl.py
"etl.py": Programa que, dado un conjunto de datos de una pizzería como ficheros csv, calcula los ingredientes que debe comprar esa pizzería en una semana, suponiendo que el número de ventas de la pizzería en una semana sea regular (utiliza la media de todos los pedidos). Además, supone que la cantidad de ingredientes de una pizza es 1 ración para la pizza pequeña, 2 para la mediana, 3 para la grande y 4 para tamaños superiores. Guarda la lista de los ingredientes a comprar con el número de raciones necesarias en un csv llamado "informe.pdf". Realiza esta funcionalidad como una etl: primero extrae los datos, después los tranforma , y por último obtiene un resultado en forma de pdf (informe.pdf). 
Los csv que recibe esta etl están corruptos, y, antes de realizar la predicción de compra para la semana siguiente, limpia los csv. El fichero 'orders.csv', del que se han modificado fechas y horas, al limpiarlo, se obtiene "Fechas_limpias.csv". Por otra parte, en el fichero de order_daetails.csv, al limpiarlo, se obtiene "Datos limpios.csv". En la limpieza de este último fichero, se ha partido de la suposición de que las pizzas que se piden se distribuyen de forma homogénea.

### analisis_de_los_datos.py
"analisis_de_los_datos.py": programa que guarda en un fichero .xml (Analisis_datos.xml) un análisis de los datos proporcionados por la pizzería. Imprime número de NaN y nulls totales y por columna así como el tipo de datos de cada columna.

### Analisis_datos.xml
Fichero de texto de salida al ejecutar analisis_de_los_datos.py


### crearpdf.py
Programa que crea un pdf a partir de los datos obtenidos en la etl utilizando la librería FPDF. También utiliza seaborn y matplotlib.plt para crear las imagenes que se incluirán en el informe. Estas imágenes son: - Ingredientes_bottom.jpg: top 5 ingredientes menos usados
- Ingredientes_top.jpg: top 5 ingredientes más usados
- Pizzas_bottom.jpg: top 5 pizzas menos vendidas
- Pizzas_top.jpg: top 5 pizzas más vendidas
También utiliza el logo de maven_pizzas (guardado como logo.jpg) y un dashboard creado utilizando powerby (informe_powerby.pbix) del que se ha incluido una imagen (informe_powerby.png)

### requirements.txt
Librerías utilizadas

### Informe.pdf
Xml obtenido como salida al realizar la etl

### Fechas_limpias.csv
Resultado de limpiar el fichero 'orders.csv'

### Datos limpios.csv
Resultado de limpiar el fichero 'order_details.csv'

### Resto de ficheros csv
Ficheros csv sobre los que se han extraido los datos para hacer el análisis