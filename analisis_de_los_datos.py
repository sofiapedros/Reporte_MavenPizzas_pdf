import pandas as pd
import xml.etree.ElementTree as ET

def indent(elem, level=0):
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
    ficheros = ['data_dictionary.csv','order_details.csv','orders.csv','pizza_types.csv','pizzas.csv']
    root = ET.Element('Análisis_ficheros', {'Análisis':'NaN, null y tipología'})
    for fichero in ficheros:
        
        df = pd.read_csv(fichero,sep=",",encoding="LATIN_1")
        fichero = ET.SubElement(root, 'fichero', {'nombre':fichero})

        NaN_totales = ET.SubElement(fichero,'NaN_totales',{'NaN_totales':str(df.isna().sum().sum())})
        Null_totales = ET.SubElement(fichero,'Null_totales',{'Null_totales':str(df.isnull().sum().sum())})

        columns_names = df.columns.values
        for j in range(len(columns_names)):
            columna = ET.SubElement(fichero,'columna',{'nombre_columna':columns_names[j]})
            NaN_en_columna =  ET.SubElement(columna,'NaN_columna',{'numero_NaN_columna':str(df[columns_names[j]].isna().sum())})
            Null_en_columna =  ET.SubElement(columna,'Null_columna',{'numero_Null_columna':str(df[columns_names[j]].isnull().sum())})
            tipo_columna =  ET.SubElement(columna,'tipo_dato',{'tipo_dato_columna':str(df[columns_names[j]].dtype)})


    #write to file
    tree = ET.ElementTree(indent(root))
    tree.write('Analisis_datos.xml', xml_declaration=True, encoding='utf-8')

        