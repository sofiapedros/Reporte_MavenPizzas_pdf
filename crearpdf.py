# Importamos las librerías necesarias
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Creamos la clase PDF
class PDF(FPDF):
    # Cabecera que aparece en todas las páginas
    def header(self):
        # En la esquina superior izquierda aparece el logo de la pizzería
        self.image('logo.jpg',10,8,15)
        # Asignamos el tipo de letra times en negrita de tamaño 20
        self.set_font('times','B',20)
        # Espacio en blanco entre el logo y el título
        self.cell(10,10)
        # Título del reporte en el centro
        self.cell(0,10,'Maven Pizza Report',new_x=XPos.LMARGIN, new_y=YPos.NEXT,border=False,align='C')
    
    # Pie de página
    def footer(self):
        # Espacio en blanco al final de cada página: 15mm
        self.set_y(-15)
        # Tipo de letra del lnúmero de páginas, times tamaño 10 en cursiva
        self.set_font('times','I',10)
        # Número de página
        self.cell(0,10,f'Page {self.page_no()}',align = 'C')

# Creamos un objeto del tipo PDF:
def create_pdf(dataframe):
    # Objeto pdf en python de hojas de tamaño A4
    pdf = PDF('P','mm','A4')

    # Cuando queden 15 mm al final de la página,
    # crea una nueva página automáticamente
    pdf.set_auto_page_break(auto = True, margin = 15)
    
    # Añadimos una página
    pdf.add_page()
    # En esa página ponemos una imagen de las estadísticas
    # de las ventas de la pizzería
    pdf.image('Maven_Pizza.png',x = -0.25, w = pdf.w +1)
    pdf.set_font('times','BU', 16)
    
    # Añadimos otra página
    pdf.add_page()
    # Añadimos una gráfica con las 5 pizzas más vendidas
    pdf.cell(10,10,'Top 5 pizzas more sold',new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=False)
    # Creamos las gráficas que vamos a añadir
    crear_pizzas_año()
    # Añadimos la imagen de las 5 pizzas más vendidas
    pdf.image('Pizzas_top.jpg',x = -0.5, w = pdf.w +1)

    # En la siguiente página, añadimos una gráfica con las 5 menos vendidas
    pdf.add_page()
    pdf.cell(10,10,'Top 5 pizzas less sold',new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=False)
    pdf.image('Pizzas_bottom.jpg',x = -0.5, w = pdf.w +1)
    
    # Añadimos otra página en blanco en la que aparecerá una gráfica con los 5 ingredientes
    # más usados
    pdf.add_page()
    pdf.cell(10,10,'Top 5 ingredients more used',new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=False)
    # Creamos las gráficas
    crear_ingredientes(dataframe)
    pdf.image('Ingredientes_top.jpg',x = -0.5, w = pdf.w +1)

    # En la siguiente página, añadimos la gráfica de las pizzas menos vendidas
    pdf.add_page()
    pdf.cell(10,10,'Top 5 ingredients less used',new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=False)
    pdf.image('Ingredientes_bottom.jpg',x = -0.5, w = pdf.w +1)

    # Añadimos otra página, a partir de la cual aparecerá un informe detallado sobre los ingredientes
    # que se necesitan en una semana
    pdf.add_page()
    pdf.cell(120,25,'Number of ingredients needed for next week',new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=False)

    # Letra times de tamaño 14
    pdf.set_font("times",'',14)
    # Columnas que aprecerán
    pdf.cell(70,10,'INGREDIENT')
    pdf.cell(70,10,"RATIONS NEEDED",new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # Recorremos el dataframe final con los ingredientes añadiendo
    # en la columna correspondiente el nombre del ingrediente y las raciones necesarias
    for i in range(len(dataframe)):
        fila = dataframe.iloc[i]
        ingrediente = str(fila['Ingredient'])
        raciones = str(fila['Number_of_rations_needed'])
        pdf.cell(70,10,ingrediente)
        pdf.cell(70,10,str(raciones),new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Guardamos el pdf
    pdf.output("Informe.pdf")

def crear_pizzas_año():
    '''
    Función que crea dos gráficos: uno con las 5 pizzas más vendidas
    y otra con las 5 menos vendidas
    '''
    # Leemos el csv con los pedidos
    pedidos = pd.read_csv('order_details.csv',sep=",",encoding="LATIN_1") 
    # Quitamos las columnas que no vamos a usar
    pedidos = pedidos.drop(['order_details_id'], axis=1)
    pedidos = pedidos.drop(['order_id'],axis = 1)
    # Agrupamos las pizzas y como cantidad, guardamos 
    # el número de veces que aparece la pizza
    pedidos = pedidos.groupby('pizza_id').sum().reset_index()

    # 5 pizzas menos vendidas (con menos apariciones)
    menores = pedidos.nsmallest(5,'quantity')

    # 5 pizzas más vendidas (con más apariciones)
    mayores = pedidos.nlargest(5,'quantity')

    # Pintar y guardar las pizzas más vendidas
    plt.rcParams.update({'font.size': 24})
    plt.figure(figsize=(24, 25))
    ax = sns.barplot(x='pizza_id', y="quantity", data=mayores,palette='mako')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=40)
    ax.set_title("Pizzas most ordered in a year")
    plt.savefig("Pizzas_top.jpg")

    # Pintar y guardar las pizzas menos vendidas
    plt.figure(figsize=(24, 25))
    ax = sns.barplot(x='pizza_id', y="quantity", data=menores,palette='mako')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=40)
    ax.set_title("Pizzas least ordered in a year")
    plt.savefig("Pizzas_bottom.jpg")

def crear_ingredientes(final):
    '''
    Función que crea dos gráficos: uno con los 5 ingredientes
    más usados y otra con los 5 menos usados
    '''

    # El dataframe ya está preparado, cogemos solamente
    # los 5 que aparecen más vences y los 5 que aparecen 
    # menos veces
    menores = final.nsmallest(5,'Number_of_rations_needed')
    mayores = final.nlargest(5,'Number_of_rations_needed')
    
    # Pintar y guardar la gráfica con los más usados en una semana
    plt.rcParams.update({'font.size': 24})
    plt.figure(figsize=(24, 25))
    ax = sns.barplot(x='Ingredient', y="Number_of_rations_needed", data=mayores,palette='mako')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=40)
    ax.set_title("Ingredients more used in a week")
    plt.savefig("Ingredientes_top.jpg")

    # Pintar y guardar la gráfica de los menos usados en una samena
    plt.figure(figsize=(24, 25))
    ax = sns.barplot(x='Ingredient', y="Number_of_rations_needed", data=menores,palette='mako')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=40)
    ax.set_title("Ingredients less used in a week")
    plt.savefig("Ingredientes_bottom.jpg")