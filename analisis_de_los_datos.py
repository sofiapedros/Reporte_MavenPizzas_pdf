import pandas as pd
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    '''
    Función recurisiva para indentar correctamente el código en un xml
    Va añadiendo espacios entre elementos y subelementos
    así como añadiendo espacios en subelementos
    '''

    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

if __name__ == "__main__":
    # Nombre de todos los ficheros a subir
    ficheros = ['data_dictionary.csv','order_details.csv','order_details_limpio.csv','orders.csv','pizza_types.csv','pizzas.csv',]

    # Raíz del documento
    root = ET.Element('Análisis_ficheros', {'Análisis':'NaN, null y tipología'})

    # Vamos a hacer lo mismo para todos los ficheros 
    for fichero in ficheros:
        # Forma de abrilos: depende del separados
        if fichero != 'orders.csv' and fichero != 'order_details.csv':
            df = pd.read_csv(fichero,sep=",",encoding="LATIN_1")
        else:
            df = pd.read_csv(fichero,sep=";",encoding="LATIN_1")
        fichero = ET.SubElement(root, 'fichero', {'nombre':fichero})

        # Escribe NaN y null totales como subelementos del fichero
        NaN_totales = ET.SubElement(fichero,'NaN_totales',{'NaN_totales':str(df.isna().sum().sum())})
        Null_totales = ET.SubElement(fichero,'Null_totales',{'Null_totales':str(df.isnull().sum().sum())})

        # Análisis de los datos por columnas
        columns_names = df.columns.values
        for j in range(len(columns_names)):
            # Crea el subelemento columna
            columna = ET.SubElement(fichero,'columna',{'nombre_columna':columns_names[j]})

            # La columna tiene varios hijos: Nan, null y tipo de dato
            NaN_en_columna =  ET.SubElement(columna,'NaN_columna',{'numero_NaN_columna':str(df[columns_names[j]].isna().sum())})
            Null_en_columna =  ET.SubElement(columna,'Null_columna',{'numero_Null_columna':str(df[columns_names[j]].isnull().sum())})
            tipo_columna =  ET.SubElement(columna,'tipo_dato',{'tipo_dato_columna':str(df[columns_names[j]].dtype)})


    #Crear el árbol bien indentado
    tree = ET.ElementTree(indent(root))

    # Escribir el árbol con la correcta indentación en el fichero
    tree.write('Analisis_datos.xml', xml_declaration=True, encoding='utf-8')

        

        