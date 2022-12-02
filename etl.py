# Importar librerías necesarias
import pandas as pd
import re
import random
from datetime import datetime
import crearpdf

def extract():
    '''
    Función que, dados los ficheros de datos de una pizzeria, los convierte en dataframes para poder trabajar con ellos
    '''
    pizza_types= pd.read_csv('pizza_types.csv',sep=",",encoding="LATIN_1") # Para ver los ingredientes de una pizza
    pedidos = pd.read_csv('order_details.csv',sep=";",encoding="LATIN_1") # Para calcular los pedidos
    pizzas = pd.read_csv('pizzas.csv',sep=",",encoding="LATIN_1") # Para ver el nombre de la pizza
    orders = pd.read_csv('orders.csv',sep=";",encoding="LATIN_1") # Para ver las fechas de los pedidos
    return pizza_types, pedidos, pizzas, orders


def limpiar_fechas(orders):
    '''
    Función que limpia las fechas y las horas para 
    ponerlas todas en el mismo formato utilizando la 
    librería datetime
    '''
    # Rellenamos los valores nulos
    orders = orders.fillna(method = 'pad')

    # Posibles formas de escribir la fecha
    patterns = ["%B %-d %Y","%Y-%m-%d","%A,%d %B, %Y","%b %d %Y",
                "%f","%d-%m%y","%m-%d%y","%d-%m%y %X","%d-%m%y %X",
                "%d %b %Y","%d-%m-%Y","%Y%m%d","%Y/%m/%d","%Y/%d/%m",
                "%Y-%m-%dT%H:%M","%a %d-%b-%Y","%d-%m-%y %X"]
    
    # Recorre todo el dataframe cambiando
    # el tipo de las fechas
    for i in range(len(orders)):
        fila = orders.iloc[i]

        # Busca con qué patrón coincide
        for pattern in patterns:
            try:
                fecha = datetime.strptime(fila['date'], pattern)
                fecha = fecha.strftime("%d-%m-%Y")
                # Si el patrón es correcto, lo cambia en el dataframe
                orders['date'][i] = fecha
                break
            except:
                try:
                    # Si la fecha está en formato UNIX
                    # hay que hacerlo con otra función

                    # Quitamos el número decimal
                    dato = fila['date'].split('.')
                    numero = dato[0]
                
                    
                    fecha = datetime.fromtimestamp(int(numero))
                    fecha = fecha.strftime("%d-%m-%Y")
                    orders['date'][i] = fecha
                    break
                except: 
                    pass
    
    # Ahora limpiamos la columna de horas
    orders = limpiar_horas(orders)

    # Guardamos el resultado en un nuevo csv para visualizar
    # los cambios
    orders.to_csv("Fechas_limpias.csv")
    return orders


def limpiar_horas(orders):
    '''
    Función que cambia el formato de las horas para que todas
    sigan el mismo patrón
    '''
    # Posibles patrones de las horas
    patterns_horas = ["%X %p","%X","%IH %MM %SS","%H:%M %p","%HH %MM %SS"]

    # Recorre todo el dataframe buscando el patrón
    for i in range(len(orders)):
        fila = orders.iloc[i]
        # Busca qué patrón coincide
        for pattern in patterns_horas:
            try:
                antiguo = fila['time']
                hora = datetime.strptime(fila['time'], pattern)
                hora = hora.strftime("%X")

                # Lo actualiza en el dataframe
                orders['time'][i] = hora
                orders['time'][i].replace(antiguo, hora)
                break

            except:
                pass
    # Devuelve el dataframe con las horas limpias
    return orders


def limpiar(pedidos):
    '''
    Función que arregla los datos del dataFrame order_details
    '''

    # Añadimos cantidad de pizzas pedidas
    pedidos[['quantity']]= pedidos[['quantity']].fillna(1)


    # Rellenamos los NaN con el valor de la fila anterior
    pedidos = pedidos.fillna(method='pad')

    for i in range(len(pedidos)):

        #order_details_id = pedidos.at[i,'order_details_id']
        #order_id = pedidos.at[i,'order_id']
        fila = pedidos.iloc[i]
        quantity = str(fila["quantity"])
        pizza_id = str(fila["pizza_id"])
        quantity2 = quantity.replace('one','1')
        quantity2 = quantity2.replace('two','2')
        quantity2 = quantity2.replace('One','1')
        quantity2 = quantity2.replace('Two','2')
        quantity2 = quantity2.replace('-1','1')

        pizza_id2 = pizza_id.replace(' ','_')
        pizza_id3 = pizza_id2.replace('-','_')
        pizza_id4 = pizza_id3.replace('3','e')
        pizza_id5 = pizza_id4.replace('@','a')
        pizza_id6 = pizza_id5.replace('0','o')
        

        pedidos.at[i, 'pizza_id'] = pizza_id6
        pedidos.at[i,'quantity'] = quantity2

    pedidos.to_csv("Datos limpios.csv")
    return pedidos


def transform(pizza_types, pedidos, pizzas, orders):
    '''
    Función que llama a funciones auxiliares para, en primer lugar, 
    contar el número de pizzas en una semana y, en segundo, dada esa 
    lista de pizzas, calcula la cantidad de raciones que la pizzeria necesitarrá 
    en una semana
    '''
    pedidos = limpiar(pedidos)
    orders = limpiar_fechas(orders)
    df_pedidos = pedidos.drop(['order_details_id'], axis=1)
    df_pedidos = df_pedidos.drop(['order_id'],axis = 1)
    df_pedidos = df_pedidos.groupby('pizza_id').sum().reset_index()
    pr = contar_pizzas_en_una_semana(pedidos, pizzas)
    final = calcular_ingredientes(pr, pizza_types)
    return final


def load(final): 
    '''
    Función que carga el dataframe final como csv
    '''
    crearpdf.create_pdf(final)


def ingredientes_de_una_pizza(nombre_tipo, pizza_types):
    '''
    Función que, dado un tipo de pizza te devuelve los ingredientes 
    que se necesitan para hacerla en forma de lista
    '''
    # La lista de ingredientes comienza vacía
    ingredientes = []
    
    # Recorre todo el dataFrame por filas (cada fila es un tipo de pizza) buscando el tipo de pizza solicitado
    for i in range(len(pizza_types.axes[0])):
        fila = pizza_types.iloc[i]
        
        # Si encuentra el nombre de la pizza que estaba buscando, va a la columna de ingredientes
        # y los separa por comas (para obtener una lista en la que los ingredientes están diferenciados)
        if re.search(nombre_tipo,str(fila),re.IGNORECASE) != None:
            ingredientes = fila['ingredients']
            ingredientes_lista = ingredientes.split(",")

    return ingredientes_lista


def cambiar_formato_nombre_pizza(nombre_tipo, pizzas):
    '''
    Función que dado el nombre de una pizza en el que se encuentra incluido su tamaño,
    separa y devuelve por un lado el nombre y por otro el número de raciones a las que 
    equivale su tamaño: pequeña ~ 1 ración; mediana ~ 2 raciones; y grande ~ 3 raciones
    '''

    # Recorre todo el dataframe de pizzas buscando el nombre de pizza completo
    # Como en esa fila del csv también aparece el nombre sin tamaño y el tamaño,
    # guardamos esos datos. Por último, calculamos el número de raciones según el tamaño
    for i in range(len(pizzas.axes[0])):
        fila = pizzas.iloc[i]
        if re.search(nombre_tipo,str(fila),re.IGNORECASE) != None:
            nombre= fila['pizza_type_id']
            tamaño = fila['size']
            if tamaño == "S":
                cantidad = 1
            elif tamaño == "M":
                cantidad = 2
            elif tamaño == "L":
                cantidad = 3
            else:
                cantidad = 4
        else:
            nombre = pizzas['pizza_type_id'].iloc[random.randint(0,30)]
            cantidad = 1
    return nombre, cantidad


def contar_pizzas_por_semana(order_details):
    '''
    Función que calcula el número de pizzas pedidas en una semana de media.
    Para ello, recorre todo el dataFrame con los datos de todos los pedidos
    y, al número total de pizzas en un año, le suma 1 por cada pizza pedida.
    Para ello, también hace uso del valor de la columna quantity que dice cuantas
    pizzas de ese tipo se han pedido en esa orden
    '''
    numero_pizzas_año = 0
    for i in range(len(order_details)):
        try:
            fila = order_details.iloc[i]
            numero_pizzas_año += 1*int(fila['quantity'])
        except:
            numero_pizzas_año += 1
    numero_pizzas = numero_pizzas_año//52
    return numero_pizzas


def contar_pizzas_en_una_semana(order_details,pizzas):
    '''
    Función que devuelve un dataframe en el que se incluyen los nombres de las pizzas
    y el número de pizzas de ese tipo que se piden por semana estándar (número calculado con la
    función contar_pizzas_por_semana)
    '''

    # Crea un dataframe vacío al que ir añadiendo los valores
    order_pizzas = pd.DataFrame(columns = ['pizza','numero'])

    # Recorre el dataframe con los detalles de los pedidos durante una semana estándar
    for i in range(0,contar_pizzas_por_semana(pedidos)):
        # Saca el nombre de la pizza_tamaño para esa fila
        pizza_con_tam = order_details.loc[i,'pizza_id']

        # Saca el dato de cuántas porciones de esa pizza se han pedido
        quantity = order_details.loc[i,'quantity']

        # Cambia el formato de la pizza_tamaño para tener por un lado el nombre
        # de la pizza y por otro su equivalencia en raciones
        pizza, tamaño = cambiar_formato_nombre_pizza(pizza_con_tam,pizzas)
        
        # Si el dataframe está vacío, añade esa pizza con sus raciones correspondientes
        if len(order_pizzas) == 0:
            order_pizzas.loc[0] = (pizza,tamaño*int(quantity))

        else:
            try:
                # Si ya hay pizzas añadidas, busca si ya se ha añadido esa pizza
                # En caso afirmativo, solamente suma las nuevas raciones a las que había
                # y en caso contrario, añade una nueva fila con la nueva pizza
                añadido = False
                for j in range(len(order_pizzas)):
                    # Recorre el dataframe nuevo por filas
                    fila2 = order_pizzas.iloc[j]

                    # Condición para ver si la pizza está ya en el dataFrame
                    if re.search(pizza,str(fila2)):
                        anterior = fila2['numero']
                        nuevo = anterior + quantity*tamaño
                        order_pizzas.loc[j,'numero'] = nuevo
                        añadido = True
                        break
                # Si añadido sigue siendo False, significa que no ha encontrado la pizza
                # en el dataframe y la añade al final
                if añadido == False:
                    order_pizzas.loc[len(order_pizzas)] = (pizza,tamaño*int(quantity))
            except:
                order_pizzas.loc[len(order_pizzas)] = (pizza,tamaño*random.randint(0,3))
    return order_pizzas


def calcular_ingredientes(order_pizzas, pizza_types):
    '''
    Función que recibe el dataframe con el número de pizzas de cada tipo pedidas en una semana
    y el dataframe que contiene los ingredientes necesarios para hacer cada pizza. Devuelve
    un nuevo dataframe en el que se encuentran todos los ingredientes y al lado el número 
    de raciones de ese ingrediente que va a necesitar la pizzeria
    '''
    # Crea un dataframe vacío en el que se van a ir añadiendo los ingredientes
    ingredientes = pd.DataFrame(columns = ['Ingredient','Number_of_rations_needed'])
    
    # Recorre por filas el dataframe con las pizzas que se han pedido
    for i in range(len(order_pizzas)):
        
        # Busca los ingredientes que necesita cada pizza
        ingredientes_de_esa_pizza = ingredientes_de_una_pizza(order_pizzas.loc[i,'pizza'],pizza_types)

        # Por cada uno de los ingredientes, mira si ya está en la "lista de la compra"
        # En caso de que no esté, lo añade y, si está, le suma tantas raciones como se vayan a pedir

        for ingrediente in ingredientes_de_esa_pizza:
            
            # Si el dataframe está vacío, hay que añadir el primer ingrediente
            if len(ingredientes) == 0:
                ingredientes.loc[0] = (ingrediente,order_pizzas.loc[i,'numero'])
            else:
                # Si no está vacío, lo recorre en busca del ingrediente
                añadido = False
                for j in range(len(ingredientes)):
                    fila2 = ingredientes.iloc[j]
                    if re.search(ingrediente,str(fila2)):
                        # Si lo encuentra, cambia el valor que había por la suma del antiguo + el nuevo
                        anterior = fila2['Number_of_rations_needed']
                        nuevo = anterior + order_pizzas.loc[i,'numero']
                        ingredientes.loc[j,'Number_of_rations_needed'] = nuevo
                        añadido = True
                        break
                if añadido == False:
                    # Si no lo ha añadido, lo añade al final del dataFrame
                    ingredientes.loc[len(ingredientes)] = (ingrediente,order_pizzas.loc[i,'numero'])

    return ingredientes

        
if __name__=="__main__":
    '''
    El main llama a las tres funciones necesarias para hacer la ETL
    '''
    pizza_types, pedidos, pizzas, orders = extract()
    final = transform(pizza_types, pedidos, pizzas, orders)
    load(final)