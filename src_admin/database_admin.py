import mysql.connector
from decouple import config



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



def select_admin():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, nombre, contra, estado from admins order by nombre;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del admin {error}")

        return "Error al mostrar los datos del admin"



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
    print(cursor.rowcount,f"Admin {state}")
    conect.close()

    return



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



def select_user():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, email, id from usuarios order by nombre;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del usuario {error}")

        return "Error al mostrar los datos del usuario"



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



def select_clothes():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, precio, id from ropas;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del parametro {error}")

        return "Error al mostrar los datos del parametro"



def select_service():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, precio, id from servicios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del parametro {error}")

        return "Error al mostrar los datos del parametro"



def select_priority():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, precio, id from prioridades;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del parametro {error}")

        return "Error al mostrar los datos del parametro"



def update_clothes(clothe,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update ropas set ropas.nombre = %s, ropas.precio = %s WHERE ropas.id = %s;"
        data = (clothe.name, clothe.price, ide)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Ropa ingresada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar la Ropa {error}")

        return "Error al ingresar la Ropa"



def update_service(service,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update servicios set servicios.nombre = %s, servicios.precio = %s WHERE servicios.id = %s;"
        data = (service.name, service.price, ide)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Servicio ingresada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar la Servicio {error}")

        return "Error al ingresar la Servicio"



def update_priority(prio,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update prioridades set prioridades.nombre = %s, prioridades.precio = %s WHERE prioridades.id = %s;"
        data = (prio.name, prio.price, ide)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Prioridad ingresada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar la Prioridad {error}")

        return "Error al ingresar la Prioridad"



def select_order():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, usuario, ropa, servicio, prioridad, comentario, precio, estado from pedidos;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del pedido {error}")

        return "Error al mostrar los datos del pedido"



def update_order(status,ide):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "update pedidos set pedidos.estado = %s WHERE pedidos.id = %s;"
        data = (status, ide)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido ingresado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el Pedido {error}")

        return "Error al ingresar el Pedido"