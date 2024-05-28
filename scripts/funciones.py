# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plotear la informacion de un dataframe de forma específica
def plot_df_info(df):
    # Dimensiones del plot
    fig, ax = plt.subplots(figsize=(14, 7))

    # Obtener la lista de columnas del dataframe
    columns = df.columns

    # Iterar sobre cada columna y crear un gráfico de columnas
    for i, col in enumerate(columns):
        # Dividir los datos en dos categorías: verde y rojo
        green_data = ~df[col].isna()
        red_data = df[col].isna()

        # Crear barras para cada categoría
        ax.bar(col, green_data.sum(), color='green', label='No NaN' if i == 0 else "")
        ax.bar(col, red_data.sum(), bottom=green_data.sum(), color='red', label='NaN' if i == 0 else "")

        # Obtener tipos de datos únicos presentes en la columna
        data_types = df[col].apply(lambda x: type(x).__name__).unique()
        # Convertir los tipos de datos a una cadena única
        data_types_str = '\n'.join(data_types)

        # Agregar label con tipos de datos sobre la columna
        ax.text(i, green_data.sum() + red_data.sum(), f'{data_types_str}', ha='center', va='bottom', fontsize=8)

    # Configurar etiquetas y leyendas
    ax.set_xlabel('Columnas')
    ax.set_ylabel('Cantidad de registros')
    ax.set_title('Gráfico de columnas', pad=20)  # Aumentar el espacio entre el título y el gráfico

    # Agregar leyenda en la parte superior derecha
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1), title='Significado de colores',
              labels=['No NaN (Verde)', 'NaN (Rojo)'])

    plt.show()

# Realizar una desanidación o explode: 

def explode(df, nombre_de_columna_a_expandir): 
    # Inicializar una lista para almacenar los registros expandidos
    expanded_data = []

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        items_list = row[f'{nombre_de_columna_a_expandir}']
    
        # Verificar si la lista de items está vacía
        if items_list:
            user_id = row['user_id']

            # Iterar sobre cada diccionario en la lista de items
            for item_dict in items_list:
            
                # Crear un nuevo registro con el mismo user_id y los valores del diccionario
                new_record = {'user_id': user_id}
                new_record.update(item_dict)  # Agregar valores del diccionario al nuevo registro
                expanded_data.append(new_record)

    return expanded_data


