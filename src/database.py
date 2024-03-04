import mysql.connector
from decouple import config

#   La funcion conectBD es la que se encarga de intentar conectarse a la base de datos usando
#   las credenciales que se alojan en el archivo .env siendo USER_DB el usuario PASSWORD_DB la
#   contraseña HOST_DB la direccion del host DATBASE el nombre de la abse de datos a usar y 
#   PORT_DB el puerto de dicha conexion. Si logra realizar una conexion exitosa, la funcion
#   devuelve dicha conexion de tipo mysql.connector si no devuelve un string de error.

def conectBD():
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

def ingresarUsuarios(usuario):
    try:
        conect = conectBD()
        cursor = conect.cursor()
        sql = "insert into usuarios values(null,%s,%s,%s);"
        data = (usuario.name, usuario.password, usuario.email)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Usuario ingresado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el ususario {error}")

        return "Error al ingresar el ususario"

#
#
#

def buscarUsuario():
    try:
        conect = conectBD()
        cursor = conect.cursor()
        cursor.execute("select nombre, contra, email from usuarios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del ususario {error}")

        return "Error al mostrar los datos del ususario"