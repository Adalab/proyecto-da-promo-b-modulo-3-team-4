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

def ordenar_columnas (dataframe):
    # Ordenamos las columnas para que siempre tengan el mismo orden, de cara a la insercion de datos. 
    # Es el orden que elegimos para poder realizar una mejor exploración de los datos. 
    
    # Escribimos una lista con las columnas en el orden deseado. 
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
    
    # Sustituimos el dataframe por el mismo dataframe pero con las columnas según el orden escrito en la lista colulmnas ordenadas 

    dataframe = dataframe[columnas_ordenadas] 
    
    print(f"Las columnas ordenadas son: {dataframe.columns}")
    
    return dataframe
    
def eliminar_columnas(dataframe):

    # Seleccionamos las columnas que hemos decidido eliminar por considerarlas menos relevantes en la EDA de los datos. 
    # Algunas son irrelevantes porque tienen informacion redundante, otras por la excesiva cantidad de nulos o registros identicos. 
    
    # Agrupamos las columnas que queremos eliminar en una variable de tipo lista.
    columnas=["Over18", "DateBirth", "MaritalStatus", "NUMBERCHILDREN", "RoleDepartament", "HourlyRate",
            "DailyRate", "MonthlyRate", "SameAsMonthlyIncome", "Salary","TOTALWORKINGYEARS","YearsInCurrentRole",
            "StandardHours", "employeecount"]
    
    print(f"Antes de la limpieza el numero de columnas que tenemos es {dataframe.shape[1]}")
    # Eliminamos las columnas con el metodo drop de pandas. 
    dataframe.drop(labels=columnas, axis=1, inplace=True)
    
    print(f"Despues de la limpieza el numero de columnas que tenemos es {dataframe.shape[1]}")
    
    return dataframe
    

def renombrar_columnas (dataframe): 
    
    # Lo primero que hacemos es un diccionario, cuyo par clave valor es respectivamente Nombre Original:Nombre Modificado. 
    diccionario_columnas = {"TOTALWORKINGYEARS": "TotalWorkingYears",
                "WORKLIFEBALANCE":"WorkLifeBalance",
                "NUMCOMPANIESWORKED": "NumCompaniesWorked",
                "YEARSWITHCURRMANAGER":"YearsWithCurrManager",
                'employeenumber':'EmployeeNumber'
                }
    
    # Con el metodo rename de pandas renombramos las columnas, que sustituye la clave por el valor asignado. 
    dataframe = dataframe.rename(columns=diccionario_columnas)
    
    print(f"Las columnas con el nombre actualizado son: {dataframe.columns}") 
    
    return dataframe


# %%

# CORRECCION ERRORES REGISTROS

def conversion_edad_numero(dataframe):
    # Hacemos par clave valor, donde la clave es el numero escrito con letras en formato string, y el valor es el numero en formato int
    number_mapping = {
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'twenty-one': 21,
        'twenty-two': 22,
        'twenty-three': 23,
        'twenty-four': 24,
        'twenty-five': 25,
        'twenty-six': 26,
        'twenty-seven': 27,
        'twenty-eight': 28,
        'twenty-nine': 29,
        'thirty': 30,
        'thirty-one': 31,
        'thirty-two': 32,
        'thirty-three': 33,
        'thirty-four': 34,
        'thirty-five': 35,
        'thirty-six': 36,
        'thirty-seven': 37,
        'thirty-eight': 38,
        'thirty-nine': 39,
        'forty': 40,
        'forty-one': 41,
        'forty-two': 42,
        'forty-three': 43,
        'forty-four': 44,
        'forty-five': 45,
        'forty-six': 46,
        'forty-seven': 47,
        'forty-eight': 48,
        'forty-nine': 49,
        'fifty': 50,
        'fifty-one': 51,
        'fifty-two': 52,
        'fifty-three': 53,
        'fifty-four': 54,
        'fifty-five': 55,
        'fifty-six': 56,
        'fifty-seven': 57,
        'fifty-eight': 58,
        'fifty-nine': 59,
        'sixty': 60,
        'sixty-one': 61,
        'sixty-two': 62,
        'sixty-three': 63,
        'sixty-four': 64,
        'sixty-five': 65
    }
    
    
    for age in dataframe['Age'].values:
        try: # Si el registro coincide con alguna clave de nuestro diccionario number_mapping se ejecutará el try
            # Primero ponemos todas las letras en minuscula y quitamos espacios antes y despues
            dataframe['Age'] = dataframe['Age'].apply(lambda x : x.lower().strip())
            # Despues reemplazamos el valor escrito por valor numerico, mediante el diccionario previamente creado
            dataframe["Age"] = dataframe["Age"].replace(number_mapping)
            # Tras la conversion convertimos el dato Age a tipo int64
            dataframe['Age'] = dataframe['Age'].astype('int64')
            
        except: # Si entra en el except o bien el registro ya es un numero, o bien está mal escrito o es nulo
            try:
                dataframe['Age'] = dataframe['Age'].astype('int64') 
                # si es un numero indicamos que lo convierta a formato int64
            except:
                print(f"Lo sentimos, no es posible convertir la edad, el registro insertado no es válido.")
                # si no es ninguna clave de nuestro diccionario ni un número indicamos que el registro no es válido. 
        
    return dataframe

    
def correccion_tipografica_JobRole(dataframe):
    # Como JobRole tiene registros no homogéneos en cuanto a mayúsculas y minúsculas usamos 
    # metodos de strings, para lo cual aplicamos una lambda function, para que en cada registro se 
    # aplique un lower (todo a minúscula), un title (primera letra de cada palabra en mayúscula) y 
    # strip (quitar espacios antes y después)
    dataframe['JobRole'] = dataframe['JobRole'].apply(lambda x : x.lower().title().strip())
    
    print(f"Las categorias actualizadas de JobRole son {dataframe['JobRole'].unique()}")
    
    return dataframe

def comas_a_puntos (dataframe): 
    # Hacemos una lista con las columnas que queremos modificar, para iterar sobre ellos.
    
    comma_list = ["EmployeeNumber", "MonthlyIncome", "PerformanceRating", "WorkLifeBalance"]
    
    # Iteramos sobre las diferentes columnas seleccionadas del dataframe
    for col in comma_list:
        
        dataframe[col] = dataframe[col].str.replace(",",".")
        dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce")
    
    print(f"Los tipos de datos numéricos que tenemos ahora en el dataframe, después de la conversion son {dataframe.select_dtypes(include=int).columns}")

    return dataframe

def conversion_distancia_positiva (dataframe):

    dataframe['DistanceFromHome'] = dataframe['DistanceFromHome'].abs()
    # usando el metodo abs de pandas, los registros negativos se transforman en su valor absoluto. 

    print(f"Podemos comprobar que después de la limpieza en nuestro dataframe hay {dataframe[dataframe['DistanceFromHome'] < 0].count()}")
    
    return dataframe


# %%
# ESTANDARIZACION COLUMNAS GENDER Y REMOTE WORK
def estandarizacion_gender(dataframe):
    gender_mapping = {0:"Male",1:"Female"}
    # Hacemos un diccionario para poder cambiar 0 por Male y 1 por Female en todos los registros, usando el metodo map de pandas
    dataframe["Gender"] = dataframe["Gender"].map(gender_mapping)
    print("Categorias actualizadas Gender:", dataframe['Gender'].unique()) 
    return dataframe

def estandarizacion_remote_work(dataframe):
    remote_mapping = {'1': 'Yes', '0':'No', 'True': 'Yes', 'False': 'No', 'Yes': 'Yes', 'No': 'No'}
    # Hacemos un diccionario para que los únicos registros que tengamos en remote_work sean yes o no
    # Esto lo conseguimos aplicando el metodo map de pandas, que sustituye las claves de nuestro diccionario por los valores
    # Si alguna clave no la encontrata cambiaria el registro por NaN
    dataframe["RemoteWork"] = dataframe["RemoteWork"].map(remote_mapping)
    print("Categorias actualizadas RemoteWork:", dataframe['RemoteWork'].unique())
    return dataframe

#%% 
# INCONGRUENCIAS EN EMPLOYEENUMBER

def eliminar_employees_duplicados (dataframe):
    
    print(f"REGISTROS DUPLICADOS ANTES DE LIMPIEZA {dataframe.duplicated().sum()}")
    # Primero eliminamos los duplicados antes de modificar RemoteWork y Distance
    dataframe.drop_duplicates(inplace=True)
  
    # filtramos del dataframe los registros que tienen EmployeeNumber repetido
    dup_con_nulos = dataframe[dataframe.duplicated(subset='EmployeeNumber',keep = False)].sort_values(by='EmployeeNumber', ascending=True)
    

    print("Numero filas duplicadas en employee number con NaN:", dup_con_nulos.shape[0])
    # Como tenemos NaN dentro de los registros repetidos, filtramos para tener el dataframe con registros repetidos sin incluir los nulos. 
    dup_sin_nulos = dup_con_nulos[dup_con_nulos['EmployeeNumber'].isnull() == False]
    print("Numero de filas duplicadas en employee number sin NaN:", dup_sin_nulos.shape[0])
    
    
    # Generamos una lista sobre la que poder iterar, que incluye todos los EmployeeNumber No nulos que tenemos repetidos
    lista_Employees_dup = list(dup_sin_nulos['EmployeeNumber'].unique())
    
    for employeenumber in lista_Employees_dup:
        # Voy elemento a elemento por esa lista y genero un dataframe dups, que incluye registros con EmployeeNumber duplicados. 
        dups = dataframe[dataframe['EmployeeNumber'] == employeenumber]
        print(dups['EmployeeNumber'].value_counts())
        print("Como para todos los EmployeeNumber no hay más de dos registros duplicados hago las comprobaciones a pares")

        
        distancia_1 = dups.iloc[0]['DistanceFromHome'] # Accedo a la Distancia del registro de la primera fila del par con el mismo EmployeeNumber
        distancia_2 = dups.iloc[1]['DistanceFromHome'] # Haemos lo mismo para el registro de la segunda fila del par con el mismo EmployeeNumber
        
        if dups.iloc[0]['RemoteWork'] != dups.iloc[1]['RemoteWork']: 
            # Si entre ambos registros hay discrepancias en RemoteWork, asumimos que el correcto es No. 
            # Eliminamos el registro que tiene el employeenumber que estamos iterando y ademas (AND) RemoteWork es Yes
            dataframe.drop(dataframe[(dataframe['RemoteWork'] == 'Yes') & (dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
        
        # Como hemos guardado las distancias en dos variables podemos comprobar cual es menor, que es con la que nos quedaremos. 
        if distancia_1 < distancia_2:
            # Si distancia 1 es menor a distancia 2 eliminamos el registro que tiene el employee number que estamos iterando y la distancia es == a distancia_2
            dataframe.drop(dataframe[(dataframe['DistanceFromHome'] == distancia_2)&(dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
            
        elif distancia_2 < distancia_1:
            # Esto es igual pero al reves, si la distancia 2 es menor, eliminamos el registro con la distancia 1. 
            dataframe.drop(dataframe[(dataframe['DistanceFromHome'] == distancia_1)&(dataframe['EmployeeNumber'] == employeenumber)].index, inplace=True)
    
    print(f"REGISTROS DUPLICADOS DESPUES DE LA LIMPIEZA {dataframe.duplicated().sum()}")
    # dataframe.drop_duplicates(inplace=True)
    
    print("EmployeeNumber Duplicados (veremos que solo son aquellos registros nulos NaN, que despues vamos a imputar):")
    print(dataframe[dataframe.duplicated(subset='EmployeeNumber')]['EmployeeNumber'].unique())

    return dataframe
# %%

def imputacion_simple_employee_number(dataframe):
    print(f"Antes de la imputacion el numero de nulos que tenemos en EmployeeNumber es : {dataframe['EmployeeNumber'].isnull().sum()}")
    
    # Cambiamos los registros que tienen valores nulos a registros en los que ponga 'Unknown' con el metodo fillna de pandas
    dataframe['EmployeeNumber'] = dataframe['EmployeeNumber'].fillna('Unknown')
    print(f"Despues de la imputacion el numero de nulos que tenemos es: {dataframe['EmployeeNumber'].isnull().sum()}")

    return dataframe

def imputacion_simple_department(dataframe):
    print(f"Antes de la imputacion el numero de nulos que tenemos en Department es : {dataframe['Department'].isnull().sum()}")
    
    # Cambiamos los registros que tienen valores nulos a registros en los que ponga 'Unknown' con el metodo fillna de pandas
    dataframe['Department'] = dataframe['Department'].fillna('Unknown')
    print(f"Despues de la imputacion el numero de nulos que tenemos es: {dataframe['Department'].isnull().sum()}")
    
    # Para terminar de limpiar department, ahora que hemos quitado los nulos, aplicamos strip, antes no podiamos por 
    # ser de tipo float (Tenia muchos NaN) y strip es un metodo de strings
    
    dataframe['Department'] = dataframe['Department'].apply(lambda x : x.strip())
    print(f"Categorias actualizadas Department: {dataframe['Department'].unique()}")
    
    return dataframe

def imputacion_simple_business_travel(dataframe): 
    print(f"Antes de la imputacion el numero de nulos que tenemos en BusinessTravel es : {dataframe['BusinessTravel'].isnull().sum()}")

    # Convertimos los nulos de 'BusinessTravel' a 'Non-Travel' 
    dataframe['BusinessTravel'] = dataframe['BusinessTravel'].fillna('Non-Travel')

    print(f"Despues de la imputacion el numero de nulos que tenemos es: {dataframe['BusinessTravel'].isnull().sum()}")
    
    return dataframe

def imputacion_simple_overtime(dataframe):
    print(f"Antes de la imputacion el numero de nulos que tenemos en OverTime es : {dataframe['OverTime'].isnull().sum()}")
    # Convertimos los nulos de 'OverTime' a 'No'
    dataframe['OverTime'] = dataframe['OverTime'].fillna('No')
    print(f"Despues de la imputacion el numero de nulos que tenemos es: {dataframe['OverTime'].isnull().sum()}")

    
    return dataframe

# %%

def limpieza_environment_satisfaction (dataframe):
    
    # Convertimos a nulos los datos mayores que 4 puesto que sabemos que son valores erróneos y distorsionan los gráficos y los
    # estadísticos

    dataframe['EnvironmentSatisfaction'] = dataframe['EnvironmentSatisfaction'].apply(lambda x: np.nan if x > 4 else x)
    
    # Calculamos la moda

    moda = dataframe['EnvironmentSatisfaction'].mode()[0]
    
    # Imputamos la moda a los nulos que se correspondian con esa recogida incorrecta de datos
    
    dataframe['EnvironmentSatisfaction'] = dataframe['EnvironmentSatisfaction'].fillna(moda)
    
    print(f"Comprobamos que las categorias que tenemos en EnvironmentSatisfaction despues de la limpieza son \n{dataframe['EnvironmentSatisfaction'].unique()}")
    
    return dataframe

#%%

def imputacion_work_life_balance (dataframe):

    # Calculamos la moda

    moda = dataframe['WorkLifeBalance'].mode()[0]
    
    # Imputamos la moda a los nulos que se correspondian con esa recogida incorrecta de datos
    
    dataframe['WorkLifeBalance'] = dataframe['WorkLifeBalance'].fillna(moda)
    
    print(f"Comprobamos que las ya no tenemos nulos en WorkLifeBalance")
    
    print(f"NULOS ==> {dataframe['WorkLifeBalance'].isnull().sum()}")
    
    return dataframe

#%%

def imputacion_performance_rating(dataframe): 
    
    # Calculamos con la mediana para imputar los nulos

    mediana= dataframe['PerformanceRating'].median()

    # Realizamos la imputacion
    dataframe['PerformanceRating'] = dataframe['PerformanceRating'].fillna(mediana)

    print(f"Comprobamos que las ya no tenemos nulos en PerformanceRating")
    
    print(f"NULOS ==> {dataframe['PerformanceRating'].isnull().sum()}")
    
    return dataframe