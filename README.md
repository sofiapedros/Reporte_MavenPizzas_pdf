# Reporte_MavenPizzas_pdf
"etl.py": Programa que, dado un conjunto de datos de una pizzería como ficheros csv, calcula los ingredientes que debe comprar esa pizzería en una semana, suponiendo que el número de ventas de la pizzería en una semana sea regular (utiliza los datos de la primera semana de enero). Además, supone que la cantidad de ingredientes de una pizza es 1 ración para la pizza pequeña, 2 para la mediana, 3 para la grande y 4 para tamaños superiores. Crea un reporte en formato pdf al final llamado "informe.pdf". Realiza esta funcionalidad como una etl: primero extrae los datos, después los tranforma, y por último obtiene un resultado en forma de un xml.

"analisis_de_los_datos.py": programa que imprime un análisis de los datos proporcionados por la pizzería. Guarda en un xml el número de NaN y nulls totales y por columna así como el tipo de datos de cada columna.

"crear_pdf.py": programa que crea un reporte ejecutivo con los datos obtenidos en el que aparecen datos generales de la pizzería, 5 pizzas más y menos vendidas, ingredientes más y menos usados así como la lista detallada de ingredientes a comprar en una semana.
