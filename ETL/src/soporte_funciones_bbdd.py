#%% 

import mysql.connector

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