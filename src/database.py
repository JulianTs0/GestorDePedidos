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
    state_register_user = "desconectado"
    try:
        conect = conectBD()
        cursor = conect.cursor()
        sql = "insert into usuarios values(null,%s,%s,%s,%s);"
        data = (usuario.name, usuario.password, usuario.email, state_register_user)
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
        cursor.execute("select nombre, contra, email, estado from usuarios;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los datos del ususario {error}")

        return "Error al mostrar los datos del ususario"

#
#
#

def ingresarPedidos(pedido,usuario):
    state_order_user = "Espera"
    try:
        conect = conectBD()
        cursor = conect.cursor()
        sql = "insert into pedidos values(null,%s,%s,%s,%s,%s,%s,%s);"
        data = (usuario.name,pedido.ropa,pedido.servicio,pedido.prioridad,pedido.comentario,pedido.precio,state_order_user)
        cursor.execute(sql,data)
        conect.commit()
        print(cursor.rowcount,"Pedido Creado")
        conect.close()

        return None
    except mysql.connector.Error as error:
        print(f"Error al ingresar el Pedido {error}")

        return "Error al ingresar el Pedido"

#
#
#

def buscarPedido():
    try:
        conect = conectBD()
        cursor = conect.cursor()
        cursor.execute("select id, usuario, ropa, servicio, prioridad, precio, estado from pedidos;")
        data = cursor.fetchall()
        conect.commit()
        conect.close()
        return data

    except mysql.connector.Error as error:
        print(f"Error al mostrar los peiddos del ususario {error}")

        return "Error al mostrar los pedidos del ususario"

#
#
#

def eliminarPedido(id):
    try:
        conect = conectBD()
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

#
#
#
    
def cambiarEstadoUsuario(user_name,state):
    if state:
        state = "conectado"
    else:
        state = "desconectado"

    conect = conectBD()
    cursor = conect.cursor()
    sql = "update usuarios set usuarios.estado = %s WHERE usuarios.nombre = %s;"
    data = (state,user_name)
    cursor.execute(sql,data)
    conect.commit()
    print(cursor.rowcount,f"Usuario {state}")
    conect.close()

    return