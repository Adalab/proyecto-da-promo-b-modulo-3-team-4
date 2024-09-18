#%% 

import mysql.connector
import pandas as pd

# Config pandas para ver todas las columnas 
pd.set_option("display.max_columns", None)

#%%

def creacion_bbdd (query, contraseña):
    cnx = mysql.connector.connect(
        user = 'root',
        password = contraseña,
        host = "127.0.0.1"
    )
    
    mycursor = cnx.cursor()
    
    try:
        mycursor.execute(query)
        print(mycursor)
        cnx.close()
    except mysql.connector.Error as err:
        print(err)
        print(f"Error Code {err.errno}")
        print(f"SQLSTATE {err.sqlstate}")
        print(f"MESSAGE {err.msg}")
        cnx.close()
            
# %%

def creacion_tablas (query, contraseña, bbdd):
    cnx = mysql.connector.connect(
        user = 'root',
        password = contraseña,
        host = "127.0.0.1",
        database = bbdd
        )
    
    mycursor = cnx.cursor()
    
    try:
        mycursor.execute(query)
        print(mycursor)
        
    except mysql.connector.Error as err:
        print(err)
        print(f"Error Code {err.errno}")
        print(f"SQLSTATE {err.sqlstate}")
        print(f"MESSAGE {err.msg}")
    
    cnx.close()
        
# %%

def insercion_datos (query, contraseña, bbdd, valores):
    cnx = mysql.connector.connect(
        user = 'root',
        password = contraseña,
        host = "127.0.0.1",
        database = bbdd
        )
    
    mycursor = cnx.cursor()
    
    try:
        mycursor.executemany(query,valores)
        cnx.commit()
        print(mycursor.rowcount, "registros insertados")
        
    except mysql.connector.Error as err:
        print(err)
        print(f"Error Code {err.errno}")
        print(f"SQLSTATE {err.sqlstate}")
        print(f"MESSAGE {err.msg}")
    
    cnx.close()


#%%

def union_tabla_work(contraseña, bbdd, dataframe, columnas):
    cnx = mysql.connector.connect(
        user = "root", 
        password = contraseña, 
        host ="127.0.0.1", 
        database = bbdd)

    mycursor = cnx.cursor()

    query = ("SELECT * FROM work")

    mycursor.execute(query)

    datos = mycursor.fetchall()
    
    cnx.close()
    
    dataframe_para_unir = pd.DataFrame(datos, columns = columnas)
     
    df_empleados_completo = pd.merge(dataframe,dataframe_para_unir, on = columnas.remove('idWork'))
    
    return df_empleados_completo
    
def union_tabla_satisfaction(contraseña, bbdd, dataframe, columnas):
    
    cnx = mysql.connector.connect(
        user = "root", 
        password = contraseña, 
        host ="127.0.0.1", 
        database = bbdd)

    mycursor = cnx.cursor()

    query = ("SELECT * FROM satisfaction_surveys")

    mycursor.execute(query)

    datos = mycursor.fetchall()
    
    cnx.close()
    
    dataframe_para_unir = pd.DataFrame(datos, columns = columnas)
     
    df_empleados_completo = pd.merge(dataframe,dataframe_para_unir, on = columnas.remove('idSatisfaction'))
    
    return df_empleados_completo