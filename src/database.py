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

        print(f"Error DB connect {error}")

        return "Error al conectarse a la base de datos"



def insert_user(user):
    state_register_user = "desconectado"
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into usuarios values(null,%s,%s,%s,%s);"
        data = (user.name, user.password, user.email, state_register_user)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Usuario ingresado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el ususario {error}")

        return "Error al ingresar el ususario"



def select_user():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select nombre, contra, email, estado from usuarios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del ususario {error}")

        return "Error al mostrar los datos del ususario"



def insert_order(order,user):
    state_order_user = "Espera"
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "insert into pedidos values(null,%s,%s,%s,%s,%s,%s,%s);"
        data = (user.name,order.ropa,order.servicio,order.prioridad,order.comentario,order.precio,state_order_user)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido Creado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el Pedido {error}")

        return "Error al ingresar el Pedido"



def select_order():
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute("select id, usuario, ropa, servicio, prioridad, precio, estado from pedidos;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los peiddos del ususario {error}")

        return "Error al mostrar los pedidos del ususario"



def delete_order_db(id):
    try:
        conect = conect_DB()
        cursor = conect.cursor()
        sql = "delete from pedidos where pedidos.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido Eliminado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al Eliminar el pedido {error}")

        return "Error al Eliminar el pedido"



def user_state_switch(user_name,state):
    if state:
        state = "conectado"
    else:
        state = "desconectado"

    conect = conect_DB()
    cursor = conect.cursor()
    sql = "update usuarios set usuarios.estado = %s WHERE usuarios.nombre = %s;"
    data = (state,user_name)
    cursor.execute(sql,data)
    conect.commit()
    print(cursor.rowcount,f"Usuario {state}")
    conect.close()

    return



def get_service_stock_data(stock_table):

    try:
        aux = []

        conect = conect_DB()
        cursor = conect.cursor()
        cursor.execute(f"select nombre from {stock_table};")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        
        for i in data:
            aux.append(i[0])
        return aux

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del ususario {error}")

        return "Error al mostrar el stock"