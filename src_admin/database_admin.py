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

def select_admin():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, nombre, contra, estado from admins;")
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

#
#
#

def insert_admin(user):
    state_register_user = "desconectado"
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into admins values(null,%s,%s,%s);"
        data = (user.name, user.password, state_register_user)
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

def get_admin_id():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, nombre from admins;")
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

def update_admin(user,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update admins set admins.nombre = %s, admins.contra = %s WHERE admins.id = %s;"
        data = (user.name, user.password,ide)
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

def delete_admin(id):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "delete from admins where admins.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Administrador Eliminado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al Eliminar el Administrador {error}")

        return "Error al Eliminar el Administrador"

#
#
#

def select_user():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, email, id from usuarios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del usuario {error}")

        return "Error al mostrar los datos del usuario"

#
#
#

def update_user(user,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update usuarios set usuarios.nombre = %s, usuarios.email = %s WHERE usuarios.id = %s;"
        data = (user.name, user.email, ide)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Usuario ingresado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el ususario {error}")

        return "Error al ingresar el ususario"