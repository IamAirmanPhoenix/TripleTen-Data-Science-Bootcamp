import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Listas de nombres nombres de las columnas. 'buttons_label' se usa para definir los radiobuttons 
# y 'list_cols' para procesar la informacion antes de generar los graficos.
# La lista 'list_cols' representa las columns cuyos valores ausentes se rellenaron con 0 y que queremos ignorar.
buttons_labels = ['price', 'model_year', 'model', 'condition', 'cylinders', 'fuel', 'odometer', 'transmission', 'type', 'paint_color', 'is_4wd', 'date_posted', 'days_listed']
list_cols = ['price', 'model_year', 'cylinders', 'odometer']

# Leemos el dataset y lo guardamos en la variable data
data = pd.read_csv('vehicles_us.csv')

# Reemplazamos valores ausentes en las columnas correspondientes
data['paint_color'] = data['paint_color'].fillna('unknown')
data['is_4wd'] = data['is_4wd'].fillna(0.0)
data['model_year'] = data['model_year'].fillna(0)
data['cylinders'] = data['cylinders'].fillna(0)
data['odometer'] = data['odometer'].fillna(0)

# Cambiamos el tipo de dato para las siguientes columnas
data['model_year'] = data['model_year'].astype('int')
data['cylinders'] = data['cylinders'].astype('int')
data['is_4wd'] = data['is_4wd'].astype('int')
data['date_posted'] = pd.to_datetime(data['date_posted'], format='%Y-%m-%d')

def names(name:str) -> str:
    '''
    Esta funcion tiene como proposito cambiar los nombres de las columnas "en bruto" por valores que sean mas interpretables.
    Se usa en el parametro format_func de los radiobuttons.
    '''

    match name:

        case 'price':
            return 'Price'
        
        case 'model_year':
            return 'Model Year'
        
        case 'model':
            return 'Car Model'
        
        case 'condition':
            return 'Condition'
        
        case 'cylinders':
            return 'Cylinders'
        
        case 'fuel':
            return 'Fuel'
        
        case 'odometer':
            return 'Odometer'
        
        case 'transmission':
            return 'Transmission'
        
        case 'type':
            return 'Type'
        
        case 'paint_color':
            return 'Paint Color'
        
        case 'is_4wd':
            return 'Is forwarded?'
        
        case 'date_posted':
            return 'Posted Date'
        
        case 'days_listed':
            return 'Days Listed'
        
# Generamos la informacion para los histogramas interactivos
hist_button = st.button('Histograma')
hist_val = st.radio("Valor a analizar:", buttons_labels, horizontal=True, key='hist_val', format_func=names)

# Generamos la informacion para los diagramas de dispersion interactivos
scatter_button = st.button('Diagramas de dispersion')
scatter_xval = st.radio("Primer valor a comparar:", buttons_labels, horizontal=True, key='scatter_xval', format_func=names)
scatter_yval = st.radio("Segundo valor a comparar:", buttons_labels, horizontal=True, key='scatter_yval', format_func=names)

# Codigo para el evento 'hist_button'
if hist_button:

    st.write(f"Histograma para '{names(hist_val)}'.")

    def column(hist_val:str) -> tuple:
        '''
        Esta funcion toma el valor del radiobutton 'hist_val' y la compara con la lista 'list_cols'. Si el valor se encuentra en la lista,
        filtra el dataframe base para quitar las filas con valores igual y menores a 0 dentro de la columna 'hist_val' y generar un nuevo
        dataframe, ademas de guardar el nombre de la columna. Estos valores los envia como una tupla.
        '''

        if hist_val in list_cols:
            data_val = data[data[hist_val] > 0]
        else:
            data_val = data

        data_name = hist_val

        return data_val, data_name

    
    # Obtenemos y usamos los valores devueltos por la funcion 'column' para generar el histograma
    data_val, data_name = column(hist_val)
    fig = px.histogram(data_val, x=data_name)

    st.plotly_chart(fig, use_container_width=True)


# Codigo para el evento 'scatter_button'
if scatter_button:

    st.write(f"Grafico de dispersion para '{names(scatter_xval)}' y '{names(scatter_yval)}':")

    def xval(scatter_xval:str) -> tuple:
        '''
        Esta funcion toma el valor del radiobutton 'scatter_xval' y la compara con la lista 'list_cols'. Si el valor se encuentra en la lista,
        genera una condicion para filtrar el dataframe base para quitar las filas con valores igual y menores a 0 dentro de la columna 'hist_val',
        ademas de guardar el nombre de la columna. Estos valores los envia como una tupla.
        '''

        if scatter_xval in list_cols:
            xval_data = data[scatter_xval] > 0
        else:
            xval_data = data

        xval_name = scatter_xval

        return xval_data, xval_name
    
            
    def yval(scatter_yval:str) -> tuple:
        '''
        Misma logica que la funcion 'xval' pero usando el valor del radiobutton 'scatter_yval'.
        '''

        if scatter_yval in list_cols:
            yval_data = data[scatter_xval] > 0
        else:
            yval_data = data

        yval_name = scatter_yval

        return yval_data, yval_name


    # Obtenemos la informacion de los radiobuttons para los graficos de dispersion       
    xval_data, xval_name = xval(scatter_xval)
    yval_data, yval_name = yval(scatter_yval)

    # Filtrado del dataset base dependiendo de las condiciones de las columnas seleccionadas
    if xval_name == yval_name:

        if xval_name not in list_cols:
            data_val = data

        else:
            data_val = data[xval_data]
            
    else:

        if (xval_name not in list_cols) & (yval_name in list_cols):
            data_val = data[yval_data]

        elif (xval_name in list_cols) & (yval_name not in list_cols):
            data_val = data[xval_data]

        elif (xval_name in list_cols) & (yval_name in list_cols):
            data_val = data[xval_data & yval_data]

        elif (xval_name not in list_cols) & (yval_name not in list_cols):
            data_val = data

    # Generamos el diagrama de dispersion interactivo
    fig = px.scatter(data_val, x=xval_name, y=yval_name)

    st.plotly_chart(fig, use_container_width=True)