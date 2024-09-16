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


#%%
def limpieza_columnas(dataframe):
    
    columnas_ordenadas = [
    'employeenumber', 
    'Age', 'Over18', 'DateBirth', 'Gender', 'MaritalStatus', 'Education', 'EducationField', 'NUMBERCHILDREN', 'NUMCOMPANIESWORKED',
    'JobLevel', 'JobRole', 'Department', 'RoleDepartament',
    'JobInvolvement', 'PerformanceRating',
    'Attrition','JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction', 'WORKLIFEBALANCE', 
    'HourlyRate', 'DailyRate', 'MonthlyRate', 'MonthlyIncome', 'SameAsMonthlyIncome', 'Salary', 'StockOptionLevel', 
    'PercentSalaryHike', 
    'YearsAtCompany', 'TOTALWORKINGYEARS','YearsInCurrentRole', 'YearsSinceLastPromotion', 'YEARSWITHCURRMANAGER', 
    'TrainingTimesLastYear', 'BusinessTravel', 'DistanceFromHome', 'StandardHours', 'OverTime', 'RemoteWork',
    'employeecount'
    ]
    
    cols=["Over18", "DateBirth", "MaritalStatus", "NUMBERCHILDREN", "RoleDepartament", "HourlyRate",
            "DailyRate", "MonthlyRate", "SameAsMonthlyIncome", "Salary","TOTALWORKINGYEARS","YearsInCurrentRole",
            "StandardHours", "employeecount"]
    
    dataframe = dataframe[columnas_ordenadas]
    
    dataframe.drop(labels=cols, axis=1, inplace=True)
    
    dicc_col = {"TOTALWORKINGYEARS": "TotalWorkingYears",
                "WORKLIFEBALANCE":"WorkLifeBalance",
                "NUMCOMPANIESWORKED": "NumCompaniesWorked",
                "YEARSWITHCURRMANAGER":"YearsWithCurrManager",
                'employeenumber':'EmployeeNumber'
                }
    
    dataframe = dataframe.rename(columns=dicc_col)
    
    return dataframe


# %%

# CORRECCION ERRORES REGISTROS

def correccion_tipografica(dataframe):
    number_mapping = {
        'forty-seven': 47,
        'fifty-eight':58,
        'thirty-six':36,
        'fifty-five':55,
        'fifty-two':52,
        'thirty-one': 31,
        'thirty':30,
        'twenty-six': 26,
        'thirty-seven':37,
        'thirty-two':32,
        'twenty-four':24
    }    
    
    comma_list = ["EmployeeNumber", "MonthlyIncome", "PerformanceRating", "WorkLifeBalance"]

    dataframe["Age"]= dataframe["Age"].replace(number_mapping)
    # CONVERSION Age a int despues de la corrección
    dataframe['Age'] = dataframe['Age'].astype('int64')
    dataframe['JobRole'] = dataframe['JobRole'].apply(lambda x : x.lower().title().strip())

    for col in comma_list:
        dataframe[col] = dataframe[col].str.replace(",",".")
        dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce")

    return dataframe

# %%
# ESTANDARIZACION COLUMNAS GENDER Y REMOTE WORK
def estandarizacion(dataframe):
    gender_mapping = {0:"Male",1:"Female"}
    remote_mapping = {'1': 'Yes', '0':'No', 'True': 'Yes', 'False': 'No', 'Yes': 'Yes', 'No': 'No'}

    dataframe["Gender"] = dataframe["Gender"].replace(gender_mapping)
    dataframe["RemoteWork"] = dataframe["RemoteWork"].map(remote_mapping)
    
    return dataframe
# %%

def eliminar_duplicados(dataframe):
    dataframe.drop_duplicates(inplace=True)
    return dataframe
# %%

def conversion_distancia_positivo(dataframe):
    # Convertimos Distancias negativas a positivas. 

    dataframe['DistanceFromHome'] = dataframe['DistanceFromHome'].abs()

    return dataframe


#%% 
# INCONGRUENCIAS EN EMPLOYEENUMBER

def eliminar_employees_duplicados (dataframe):
    dup_con_nulos = dataframe[dataframe.duplicated(subset='EmployeeNumber',keep = False)].sort_values(by='EmployeeNumber', ascending=True)
    dup_sin_nulos = dup_con_nulos[dup_con_nulos['EmployeeNumber'].isnull() == False]
    lista_Employees_dup = list(dup_sin_nulos['EmployeeNumber'].unique())
    for employeenumber in lista_Employees_dup:
        dups = dataframe[dataframe['EmployeeNumber'] == employeenumber]
        distancia_1 = dups.iloc[0]['DistanceFromHome']
        distancia_2 = dups.iloc[1]['DistanceFromHome']
        
        if dups.iloc[0]['RemoteWork'] != dups.iloc[1]['RemoteWork']:
            dataframe.drop(dataframe[(dataframe['RemoteWork'] == 'Yes') & (dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
        
        if distancia_1 < distancia_2:
            dataframe.drop(dataframe[(dataframe['DistanceFromHome'] == distancia_2)&(dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
            
        elif distancia_2 < distancia_1:
            dataframe.drop(dataframe[(dataframe['DistanceFromHome'] == distancia_1)&(dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
        
    return dataframe
# %%
# Imputamos a los nulos de EmployeeNumber el valor 'Unknown'

def imputacion_simple_nulos(dataframe, columna):
    
    print(f"Valores nulos antes de imputacion en EmployeeNumber ==> {dataframe[columna].isnull().sum()}")

    # Cambiamos esos nulos por Unknown
    dataframe[columna] = dataframe[columna].fillna('Unknown')

    return dataframe
