import mysql.connector
from decouple import config

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

def ingresarUsuarios(usuario):
    try:
        conect = conectBD()
        cursor = conect.cursor()
        sql = "insert into usuarios values(null,%s,%s,%s);"
        data = (usuario.name ,usuario.password ,usuario.email)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Usuario ingresado")
        conect.close()

        return
    except mysql.connector.Error as error:
        print(f"Error al ingresar el ususario {error}")

        return "Error al ingresar el ususario"

