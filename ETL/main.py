
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

import mysql.connector

# Agrega el directorio 'src' al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src import soporte_funciones_transformacion as transform
from src import queries as query
from src import soporte_funciones_bbdd as bbdd

#%%

# Abrimos Dataframe
df = pd.read_csv("files/HR RAW DATA.csv", index_col=0)
df.head(2)

# %%

# LIMPIAMOS COLUMNAS DATAFRAME

df = transform.ordenar_columnas(df)

# %%
df = transform.eliminar_columnas(df)

#%%

df = transform.renombrar_columnas(df)


#%% 

# CORREGIMOS COLUMNA AGE (PARA QUE SOLO INCLUYA REGISTROS NUMERICOS)

df = transform.conversion_edad_numero(df)

#%%

# UNIFICAMOS REGISTROS JOBROLE

df = transform.correccion_tipografica_JobRole(df)

# %%

# CAMBIAMOS COMAS POR PUNTOS

df = transform.comas_a_puntos(df)

#%%

# CONVERTIMOS DISTANCIAS NEGATIVAS EN POSITIVAS 

df = transform.conversion_distancia_positiva(df)

# ESTANDARIZACION COLUMNAS GENDER Y REMOTE WORK

df = transform.estandarizacion_gender(df)
df = transform.estandarizacion_remote_work(df)


#%%

df = transform.eliminar_employees_duplicados (df)


#%%

# REALIZAMOS IMPUTACIONES SIMPLES

df = transform.imputacion_simple_employee_number(df)
df = transform.imputacion_simple_department(df)
df = transform.imputacion_simple_business_travel(df)
df = transform.imputacion_simple_overtime(df)


#%% 

# GUARDAMOS EN UN CSV

df.to_csv('files/HR RAW DATA_CLEAN.csv')

