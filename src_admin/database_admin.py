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



#Usar clases
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



def select_clothes():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, precio, id from ropas order by precio desc;")
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
        cursor.execute("select nombre, precio, id from servicios order by precio desc;")
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
        cursor.execute("select nombre, precio, id from prioridades order by precio desc;")
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



def insert_clothes(clothe):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into ropas values(null,%s,%s);"
        data = (clothe.name, clothe.price)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Ropa ingresada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar la Ropa {error}")

        return "Error al ingresar la Ropa"



def insert_service(service):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into servicios values(null,%s,%s);"
        data = (service.name, service.price)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Servicio ingresado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el Servicio {error}")

        return "Error al ingresar el Servicio"



def insert_priority(priority):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into prioridades values(null,%s,%s);"
        data = (priority.name, priority.price)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Prioridad ingresada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar la Prioridad {error}")

        return "Error al ingresar la Prioridad"



def delete_clothes(id):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "delete from ropas where ropas.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Ropa Eliminada")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al Eliminar la ropa {error}")

        return "Error al Eliminar la ropa"



def delete_service(id):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "delete from servicios where servicios.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Servicio Eliminado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al Eliminar el servicio {error}")

        return "Error al Eliminar el servicio"



def delete_priority(id):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "delete from prioridades where prioridades.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Prioridad Eliminado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al Eliminar el prioridad {error}")

        return "Error al Eliminar el prioridad"



def select_order():

    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, usuario, ropa, servicio, prioridad, comentario, precio, estado from pedidos order by prioridad desc;")
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