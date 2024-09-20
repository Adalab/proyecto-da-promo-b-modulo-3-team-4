
#%%

# Importamos librerías para el tratamiento de datos
import pandas as pd
import numpy as np
# Config pandas para ver todas las columnas 
pd.set_option("display.max_columns", None)

# Importamos librerías para visualización
import matplotlib.pyplot as plt
import seaborn as sns

# import libraries for imputation using advanced statistical methods
# -----------------------------------------------------------------------
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer

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
df = pd.read_csv("../data/HR RAW DATA.csv", index_col=0)
df.head(2)

#%% 
print(df.shape)


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

# REALIZAMOS IMPUTACIONES EN FUNCION DE MEDIDAS DE ESTADISTICA DESCRIPTIVA 

df = transform.limpieza_environment_satisfaction(df)

#%%

df = transform.imputacion_work_life_balance(df)


#%% 

df = transform.imputacion_performance_rating(df)

#%%

df = transform.imputacion_monthly_income(df)


#%% 

print(df.shape)
df.columns

# GUARDAMOS EN UN CSV

df.to_csv('../data/HR RAW DATA_CLEAN.csv')

df.head(1)
# %%
