
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

# ABRIMOS CSV

df = pd.read_csv('files/HR RAW DATA_CLEAN.csv', index_col = 0)

print(df.shape)

df.head(2)



# %%
# CREACION SCHEMA

bbdd.creacion_bbdd(query.query_creacion_bbdd, 'AlumnaAdalab')

# %%

# CREACION TABLAS

# TABLA WORK
bbdd.creacion_tablas(query.query_creacion_tabla_work, 'AlumnaAdalab', 'Proyecto')

#%%
# TABLA SATISFACTION SURVEYS
bbdd.creacion_tablas(query.query_creacion_tabla_satisfaction_surveys, 'AlumnaAdalab', 'Proyecto')

#%%
# TABLA EMPLOYEES
bbdd.creacion_tablas(query.query_creacion_tabla_employees, 'AlumnaAdalab', 'Proyecto')

#%%

# TABLA WORK_CONDITION
bbdd.creacion_tablas(query.query_creacion_tabla_work_info, 'AlumnaAdalab', 'Proyecto')


# %%
# PRIMERO INSERTAMOS DATOS EN LAS TABLAS WORK Y SATISFACTION, PORQUE SU PRIMARY KEY VA A SER FOREIGN KEY EN TABLA EMPLOYEES

# Lo primero que hacemos es recoger los datos en una lista de tuplas, para lo cual recopilamos las diferentes combinaciones 
# que hay en nuestro dataframe para las columnas de interes. Para evitar registros duplicados despues de aplicar el metodo zip, 
# convertimos el output en un set (para evitar que haya subsets duplicados) y el set lo convertimos a lista para poder hacer 
# las inserciones en SQL (en formato lista de tuplas). 

valores_tabla_work = list(set(zip([int(x) for x in df['JobLevel'].values],df['JobRole'].values, df['Department'].values)))

print(valores_tabla_work)

valores_tabla_satisfaction = list(set(zip(
    [int(x) for x in df['JobInvolvement'].values],
    [float(x) for x in df['PerformanceRating'].values],
    [int(x) for x in df['EnvironmentSatisfaction'].values],
    [int(x) for x in df['RelationshipSatisfaction'].values],
    [float(x) for x in df['WorkLifeBalance'].values],
    [int(x) for x in df['JobSatisfaction'].values])))
    
print(valores_tabla_satisfaction)

# %%

# INSERTAMOS LOS DATOS EN LA TABLA WORK
bbdd.insercion_datos(query.query_insercion_work, 'AlumnaAdalab', 'Proyecto', valores_tabla_work)

#%%
# INSERTAMOS LOS DATOS EN LA TABLA SATISFACTION SURVEYS

bbdd.insercion_datos(query.query_insercion_satisfaction, 'AlumnaAdalab', 'Proyecto', valores_tabla_satisfaction)

# %%

columnas = ['idWork', 'JobLevel', 'JobRole', 'Department']

df_completo = bbdd.union_tabla_work('AlumnaAdalab', 'Proyecto', df)

print(df_completo.shape)

# %%

columnas2 = ['idSatisfaction', 'JobInvolvement', 'PerformanceRating', 'EnvironmentSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance', 'JobSatisfaction']
df_completo = bbdd.union_tabla_satisfaction('AlumnaAdalab', 'Proyecto', df_completo)
print(df_completo.shape)



#%%
print(df_completo)

#%%
valores_tabla_employee = list((zip(
    df_completo['EmployeeNumber'].values,
    [int(x) for x in df_completo['Age'].values],
    df_completo['Gender'].values,   
    [int(x) for x in df_completo['Education'].values], 
    df_completo['EducationField'].values, 
    [int(x) for x in df_completo['NumCompaniesWorked'].values],
    [float(x) for x in df_completo['MonthlyIncome'].values],
    [int(x) for x in df_completo['StockOptionLevel'].values],
    [int(x) for x in df_completo['YearsAtCompany'].values],
    [int(x) for x in df_completo['YearsSinceLastPromotion'].values], 
    [int(x) for x in df_completo['YearsWithCurrManager'].values],
    [int(x) for x in df_completo['TrainingTimesLastYear'].values], 
    [int(x) for x in df_completo['DistanceFromHome'].values],
    df_completo['Attrition'].values, 
    [int(x) for x in df_completo['idWork'].values],
    [int(x) for x in df_completo['idSatisfaction']]
)))

print(valores_tabla_employee)

#%% INSERCION DATOS EMPLOYEE

bbdd.insercion_datos(query.query_insercion_employees, 'AlumnaAdalab', 'Proyecto', valores_tabla_employee)

#%% INSERCION DATOS JOB INFO

valores_tabla_work_info = list(set(zip(
    df_completo['RemoteWork'].values,
    df_completo['OverTime'].values, 
    df_completo['BusinessTravel'].values,
    [int(x) for x in df_completo['idWork'].values]
)))

print(valores_tabla_work_info)

# %%
bbdd.insercion_datos(query.query_insercion_work_info, 'AlumnaAdalab', 'Proyecto', valores_tabla_work_info)

# %%
