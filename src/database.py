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

    except:

        print(f"Error DB connect {mysql.connector.Error}")
        return "Error al conectarse a la base de datos"



def insert_user(user):

    state_register_user = "desconectado"
    conect = conect_DB()

    if isinstance(conect,str):
        print(f"Error al ingresar el ususario {conect}")
        return "Error al ingresar el ususario"

    else:

        cursor = conect.cursor()
        sql = "insert into usuarios values(null,%s,%s,%s,%s);"
        data = (user.name, user.password, user.email, state_register_user)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Usuario ingresado")
        conect.close()



def select_user():

    conect = conect_DB()

    if isinstance(conect,str):
        print(f"Error al mostrar los datos del ususario {conect}") 
        return "Error al mostrar los datos del ususario"

    else:

        cursor = conect.cursor()
        cursor.execute("select nombre, contra, email, estado from usuarios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data 



def insert_order(order,user):

    state_order_user = "Espera"
    conect = conect_DB()

    if isinstance(conect,str):
        print(f"Error al ingresar el Pedido {conect}")
        return "Error al ingresar el Pedido"

    else:

        cursor = conect.cursor()
        sql = "insert into pedidos values(null,%s,%s,%s,%s,%s,%s,%s);"
        data = (user.name,order.ropa,order.servicio,order.prioridad,order.comentario,order.precio,state_order_user)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido Creado")
        conect.close() 



def select_order():

    conect = conect_DB()

    if isinstance(conect,str):
        print(f"Error al mostrar los peiddos del ususario {conect}")
        return "Error al mostrar los pedidos del ususario" 

    else:

        cursor = conect.cursor()
        cursor.execute("select id, usuario, ropa, servicio, prioridad, precio, estado from pedidos;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data



def delete_order_db(id):

    conect = conect_DB()

    if isinstance(conect,str):

        print(f"Error al Eliminar el pedido {conect}")
        return "Error al Eliminar el pedido"
    else:

        cursor = conect.cursor()
        sql = "delete from pedidos where pedidos.id = %s;"
        data = (id,)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido Eliminado")
        conect.close() 



def user_state_switch(user_name,state):

    conect = conect_DB()

    if isinstance(conect,str):

        print(f"Error al cambiar el estado del usuario {conect}")
        return "Error al Eliminar el pedido"
    else:

        state = "desconectado"
        if state:
            state = "conectado"
        cursor = conect.cursor()
        sql = "update usuarios set usuarios.estado = %s WHERE usuarios.nombre = %s;"
        data = (state,user_name)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,f"Usuario {state}")
        conect.close() 



def get_service_stock_data(stock_table):

    conect = conect_DB()
    if isinstance(conect,str):
        print(f"Error al mostrar los datos del ususario {conect}")
        return "Error al mostrar el stock"
    
    else:

        cursor = conect.cursor()
        cursor.execute(f"select nombre, precio from {stock_table};")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        
        return data