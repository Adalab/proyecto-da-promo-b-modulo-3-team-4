

#%%

# Importamos librerías para el tratamiento de datos
import pandas as pd
import numpy as np
# Config pandas para ver todas las columnas 
pd.set_option("display.max_columns", None)

# Importamos librerías para visualización
import matplotlib.pyplot as plt
import seaborn as sns

# Importamos librerías para análisis estadístico
import scipy.stats as stats
from scipy.stats import shapiro, kstest, ttest_ind, mannwhitneyu, expon, chisquare

import sys
import os

# Agrega el directorio 'src' al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src import soporte_funciones_transformacion as transform

#%%

# Abrimos Dataframe
df = pd.read_csv("files/HR RAW DATA.csv", index_col=0)
df.head(2)

# %%
# ORDENAMOS COLUMNAS 
print(f"Columnas antes de ordenar {df.columns}")
# ejecuto metodo ordenar columnas y compruebo que se han ordenado correctamente
df = transform.ordenar_columnas(df)
print(f"Columnas ordenadas {df.columns}")


# %%
# ELIMINAR COLUMNAS
print(f"Numero columnas antes de eliminar ==> {len(df.columns)}")
df = transform.eliminar_columnas(df)
print(f"Columnas despues de la limpieza {len(df.columns)}")
print(f"Columnas actualizadas ==> {df.columns}")

# %%

# RENOMBRAR COLUMNAS
df = transform.renombrar_columnas(df)
print(f"COLUMNAS ACTUALIZADAS ==> {df.columns}")

# %%
df = transform.correccion_tipografica(df)
# comprobamos que después de la corrección los tipos de datos se me han corregido
df.dtypes

# %%

# ESTANDARIZACION COLUMNAS GENDER Y REMOTE WORK

df = transform.estandarizacion(df)
print(f"CATEGORIAS REMOTE WORK: {df['RemoteWork'].unique()}")
print(f"CATEGORIAS GENDER: {df['Gender'].unique()}")

# %%
print(f"DUPLICADOS ANTES DE DEPURAR: {df.duplicated().sum()}")
df = transform.eliminar_duplicados(df)
print(f"DUPLICADOS DESPUES DE LIMPIEZA: {df.duplicated().sum()}")
# %%

df = transform.conversion_distancia_positivo(df)
#comprobamos
print(df[df['DistanceFromHome']>0].count())

#%%
df = transform.eliminar_employees_duplicados (df)

df[df.duplicated(subset='EmployeeNumber',keep = False)].sort_values(by='EmployeeNumber', ascending=True)



