

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
# LIMPIAMOS COLUMNAS (Ordenamos, estandarizamos nombres, eliminamos)
print(f"Columnas antes de limpieza {df.columns}, que son un total de {df.shape[1]} columnas")
# ejecuto metodo ordenar columnas y compruebo que se han ordenado correctamente
df = transform.limpieza_columnas(df)
print(f"DATAFRAME ORDENADO {df.columns} que son un total de {df.shape[1]} columnas")

# %%
df = transform.correccion_tipografica(df)
# comprobamos que después de la corrección los tipos de datos se me han corregido
display(df.head(2))
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
print("Distancia < 0  ==> ", df[df['DistanceFromHome']<0]['DistanceFromHome'].count())

#%%
df = transform.eliminar_employees_duplicados (df)

df[df.duplicated(subset='EmployeeNumber',keep = False)].sort_values(by='EmployeeNumber', ascending=True)

#%%

# IMPUTACION SIMPLE, ASIGNACION DIRECTA, A COLUMNA DATAFRAME

df = transform.imputacion_simple_nulos(df,'EmployeeNumber')
print(df['EmployeeNumber'].isnull().sum())
print(df[df['EmployeeNumber'] == 'Unknown']['EmployeeNumber'].count())



# %%
# CREACION SCHEMA

bbdd.creacion_bbdd(query.query_creacion_bbdd, 'AlumnaAdalab')

# %%

# CREACION TABLAS

bbdd.creacion_tablas(query.query_creacion_tabla_employee, 'AlumnaAdalab', 'Proyecto')
bbdd.creacion_tablas(query.query_creacion_tabla_work, 'AlumnaAdalab', 'Proyecto')
bbdd.creacion_tablas(query.query_creacion_tabla_work_conditions, 'AlumnaAdalab', 'Proyecto')
bbdd.creacion_tablas(query.query_creacion_tabla_work_employee, 'AlumnaAdalab', 'Proyecto')

# %%

df.columns

#%%
# INSERCION DATOS

valores_tabla_employee = list(set(zip(
    df['EmployeeNumber'].values,
    [int(x) for x in df['Age'].values],  
    [int(x) for x in df['Education'].values],                      # Convierte cada valor de 'Age' a int
    [int(x) for x in df['NumCompaniesWorked'].values],     # Convierte cada valor de 'NumCompaniesWorked' a int
    [int(x) for x in df['DistanceFromHome'].values] )))

# %%

bbdd.insercion_datos(query.query_insercion_employees, 'AlumnaAdalab', 'Proyecto', valores_tabla_employee)
# %%

valores_tabla_work = list(set(zip(
    [int(x) for x in df['JobLevel'].values],
    df['JobRole'].values,
    df['Department'].values)))



# %%
bbdd.insercion_datos(query.query_insercion_work, 'AlumnaAdalab', 'Proyecto', valores_tabla_work)

# %%

