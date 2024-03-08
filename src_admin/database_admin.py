import mysql.connector
from decouple import config

#   La funcion conectBD es la que se encarga de intentar conectarse a la base de datos usando
#   las credenciales que se alojan en el archivo .env siendo USER_DB el usuario PASSWORD_DB la
#   contraseña HOST_DB la direccion del host DATBASE el nombre de la abse de datos a usar y 
#   PORT_DB el puerto de dicha conexion. Si logra realizar una conexion exitosa, la funcion
#   devuelve dicha conexion de tipo mysql.connector si no devuelve un string de error.

def conect_DB():
    try:
        conection = mysql.connector.connect(user=config("USER_DB"),
                                            password=config("PASSWORD_DB"),
                                            host=config("HOST_DB"),
                                            database=config("DATABASE"),
                                            port=config("PORT_DB"))
        
        return conection
    except mysql.connector.Error as error:

        print(f"Error al conectarse a la base de datos {error}")

        return "Error al conectarse a la base de datos"

#   La funcion ingresarUsuarios es la que se encarga de insertar en la BD los datos de un
#   objeto de tipo Usuario llamado usuario, a traves de comandos en lenguaje SQL que se determinan
#   en la variable sql. Si logra insertar los datos exitosamente en la BD retorna None, caso contrario
#   retorna una string de error.

def select_user():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, contra, estado from admins;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del admin {error}")

        return "Error al mostrar los datos del admin"

#
#
#

def user_state_switch(user_name,state):
    if state:
        state = "conectado"
    else:
        state = "desconectado"

    conect = conect_DB()
    cursor = conect.cursor()
    sql = "update admins set admins.estado = %s WHERE admins.nombre = %s;"
    data = (state,user_name)
    cursor.execute(sql,data)
    conect.commit()
    print(cursor.rowcount,f"Amin {state}")
    conect.close()

    return


    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute(f"select nombre, precio from {stock_table};")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del ususario {error}")

        return "Error al mostrar el stock"