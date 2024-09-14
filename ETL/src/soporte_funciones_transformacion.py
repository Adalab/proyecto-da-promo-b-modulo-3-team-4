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
def ordenar_columnas(dataframe):
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
    
    dataframe = dataframe[columnas_ordenadas]
    return dataframe
# %%

def eliminar_columnas(df):
    # Eliminar todas las columnas anteriores:
    cols=["Over18", "DateBirth", "MaritalStatus","NUMBERCHILDREN", "Department", "RoleDepartament", "HourlyRate",
            "DailyRate", "MonthlyRate", "SameAsMonthlyIncome", "Salary", "StandardHours", "employeecount"]
    
    df.drop(labels=cols, axis=1, inplace=True)

    return df
    
#%%

# RENOMBRAR COLUMNAS 

def renombrar_columnas(df):
    dicc_col = {"TOTALWORKINGYEARS": "TotalWorkingYears",
                "WORKLIFEBALANCE":"WorkLifeBalance",
                "NUMCOMPANIESWORKED": "NumCompaniesWorked",
                "YEARSWITHCURRMANAGER":"YearsWithCurrManager",
                'employeenumber':'EmployeeNumber'
                }
    df.rename(columns=dicc_col, inplace=True)
    
    return df

# %%

# CORRECCION ERRORES REGISTROS

def correccion_tipografica(df):
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
    
    comma_list = ["EmployeeNumber", "MonthlyIncome", "PerformanceRating", "TotalWorkingYears", "WorkLifeBalance", "YearsInCurrentRole"]

    df["Age"]= df["Age"].replace(number_mapping)
    # CONVERSION Age a int despues de la corrección
    df['Age'] = df['Age'].astype(int)
    df['JobRole']=df['JobRole'].apply(lambda x : x.lower().title().strip())

    for col in comma_list:
        df[col] = df[col].str.replace(",",".")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# %%
# ESTANDARIZACION COLUMNAS GENDER Y REMOTE WORK
def estandarizacion(df):
    gender_mapping = {0:"Male",1:"Female"}
    remote_mapping = {'1': 'Yes', '0':'No', 'True': 'Yes', 'False': 'No', 'Yes': 'Yes', 'No': 'No'}

    df["Gender"] = df["Gender"].replace(gender_mapping)
    df["RemoteWork"] = df["RemoteWork"].map(remote_mapping)
    
    return df
# %%

def eliminar_duplicados(df):
    df.drop_duplicates(inplace=True)
    return df
# %%

def conversion_distancia_positivo(df):
    # Convertimos Distancias negativas a positivas. 

    df['DistanceFromHome'] = df['DistanceFromHome'].abs()

    return df


#%% 
# INCONGRUENCIAS EN EMPLOYEENUMBER

def eliminar_employees_duplicados (df):
    dup_con_nulos = df[df.duplicated(subset='EmployeeNumber',keep = False)].sort_values(by='EmployeeNumber', ascending=True)
    dup_sin_nulos = dup_con_nulos[dup_con_nulos['EmployeeNumber'].isnull() == False]
    lista_Employees_dup = list(dup_sin_nulos['EmployeeNumber'].unique())
    for employeenumber in lista_Employees_dup:
        dups = df[df['EmployeeNumber'] == employeenumber]
        distancia_1 = dups.iloc[0]['DistanceFromHome']
        distancia_2 = dups.iloc[1]['DistanceFromHome']
        
        if dups.iloc[0]['RemoteWork'] != dups.iloc[1]['RemoteWork']:
            df.drop(df[(df['RemoteWork'] == 'Yes') & (df['EmployeeNumber'] == employeenumber)].index, inplace=True)
        
        if distancia_1 < distancia_2:
            df.drop(df[(df['DistanceFromHome'] == distancia_2)&(df['EmployeeNumber'] == employeenumber)].index, inplace=True)
            
        elif distancia_2 < distancia_1:
            df.drop(df[(df['DistanceFromHome'] == distancia_1)&(df['EmployeeNumber'] == employeenumber)].index, inplace=True)
        
    return df
# %%
