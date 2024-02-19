"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    # Lista de archivos
    filenames = glob.glob(input_directory + '/*.*')

    # Leemos cada archivo
    dataframes = [
        pd.read_csv(filename, sep=';', names=['word']) for filename in filenames
    ]

    # Convertimos a un mismo df
    dataframe = pd.concat(dataframes).reset_index(drop=True)

    # Devolvemos el df
    return dataframe

def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()

    # Convierte a minúsculas
    dataframe['word'] = dataframe['word'].str.lower()
    # Elimianos los signo
    dataframe['word'] = dataframe['word'].str.replace(',', '').str.replace('.', '')
    # Devolvemos el df
    return dataframe


def count_words(dataframe):
    """Word count"""
    dataframe = dataframe.copy()

    # Convertimos a lista de palabras
    dataframe['word'] = dataframe['word'].str.split()

    # Convertimos la lista en una columna
    dataframe = dataframe.explode('word').reset_index(drop=True)

    # Agregamos la columna con la frecuencia de palabras
    dataframe['count'] = 1

    frequence = dataframe.groupby(['word'], as_index=False).agg(
        {
            'count':sum
        }
    )

    # Devolvemos el df
    return frequence


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, index=False, header=False, sep="\t")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
