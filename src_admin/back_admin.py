from clases_admin import *
from tkinter import messagebox
from tkinter import *
from smtplib import *
from database_admin import *
from decouple import config



def is_a_number(number):

    valid_number = "0123456789"

    for i in number:
        if i not in valid_number:
            return False
    
    return True



def is_a_valid_char(word):

    valid_char = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZÀÈÌÒÙàèìòù "

    for i in word:
        if i not in valid_char:
            return False
    
    return True



# Retornar tambien el msg de error
def exist_admin(user_data_search,parameter):
    users_data = select_admin()

    if isinstance(users_data,str):
        return "Error al conectarse a la base de datos"
    else:
        for user in users_data:
            if user[parameter] == user_data_search:
                return user
        return "El administrador no existe"



# Retornar tambien el msg de error
# Usar las clases
def verify_admin(name,password):

    if name == "" or password == "":
        return "Complete los campos antes de iniciar sesion"
    
    elif not is_a_valid_char(name) or len(name) > 30 :
        return "Ingrese un nombre de usuario valido"
    
    elif len(password) > 20:
        return "Ingrese una contraseña valida"
    
    else:
        return None



# Usar el check_conection
def login_admin(user_name,user_password):

    verif_res  = verify_admin(user_name,user_password)

    if verif_res is not None:
        return verif_res
    
    else:
        check_conection = conect_DB()

        if isinstance(check_conection,str):
            return check_conection
        
        else:
            res_search = exist_admin(user_name,1)
        
            if isinstance(res_search,str):
                return res_search
            
            else:
                if res_search[2] != user_password:
                    return "Contraseña incorrecta"
                
                else:
                    if res_search[3] == "conectado":
                        return "El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                    else:
                        user_state_switch(res_search[1],True)
                        return Admin(res_search[1],res_search[2])               



#Crear una nueva funcion para eliminar el parametro force
def de_login(user_name,force=False):

    if not force:

        res_search = exist_admin(user_name,1)

        if isinstance(res_search,str):
            return res_search
        else:
            if res_search[2] == "desconectado" or res_search[2] is None:
                return "La sesion no se puede cerrar porque el usuario no esta conectado"
            else:
                user_state_switch(user_name,False)
                return None
    else:
        user_state_switch(user_name,False)



def get_admins(user):
    all_admins = select_admin()
    admins_data = []

    if isinstance(all_admins,str):
        return all_admins

    else:
        for admin in all_admins:
            if admin[1] != user.name:
                admin = (admin[0],admin[1],admin[2])
                admins_data.append(admin)
        return admins_data



# Reducir las exigencias para crear un nuevo administrador, esta funcion esta
# haciendo dos cosas distintas
# Retornar tambien el msg de error
# Usar las clases
def verif_admin_data(name,password,ide=None):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de usuario valido"
    
    elif password == "" or len(password) > 20:
        return "No se ha ingresado la contraseña valida"

    res_search = exist_admin(name,1)
    
    if not isinstance(res_search,str):
        return "Ese nombre de usuario ya existe escoja otro"
    
    if ide is not None:
        return exist_admin(ide,0)
    
    user = Admin(name,password)
    return user 



# Usar el check_conection
def register_admin_db(name,password):

    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"

    else:
        verif_res = verif_admin_data(name, password)

        if isinstance(verif_res,str):
            return f"1|Error al registrar la cuenta|{verif_res}"
        
        else:
            insert_db_res = insert_admin(verif_res)

            if insert_db_res is not None:
                return f"0|Error|{insert_db_res}"
                
            else:
                return "2|Administrador registrado|El Administrador a sido creado y registrado con exito"



# Usar el check_conection
# Esta funcion no esta pudiendo modifcar un usuario con su id, revisar el caso
def modify_admin(name,password,ide):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_admin_data(name, password, ide)

        if not isinstance(verif_res,str):
            return "1|Error al modificar al usuario|Seleccione devuelta al usuario para modificarlo"

        else:
            admin = Admin(name,password)
            modify_admin_res = update_admin(admin,ide)

            if modify_admin_res is not None:
                return f"0|Error|{modify_admin_res}"

            else:
                return f"2|Administrador modificado|Los datos del administrador fueron modificados con exito"



def delete_admin_user(id_admin):

    option = messagebox.askyesno("Ultima confirmacion",f"Desea eliminar al administrador?")

    if not option:
        return "1|Accion exitosa|Se aborto la operacion con exito"

    else:
        delete_res = delete_admin(id_admin)
        if delete_res is not None:
            return f"0|Error|{delete_res}"
        
        else:
            return "1|Accion exitosa|Su accion fue cancelada con exito"



# Retornar tambien el msg de error
def exist_user(user_data_search,parameter):
    users_data = select_user()

    for user in users_data:
        if user[parameter] == user_data_search:
            return user
    return None



def orders_amount(user_name):
    all_orders = select_order()
    amount = 0

    if isinstance(all_orders,str):
        return -1
    
    else:
        for order in all_orders:
            if order[1] == user_name:
                amount += 1
        return amount



def get_users():
    all_users = select_user()
    users_data = []

    if isinstance(all_users,str):
        return all_users
    
    else:
        for usuario in all_users:
            usuario = (usuario[0],usuario[1],usuario[2],orders_amount(usuario[0]))
            users_data.append(usuario)
        return users_data



# Usar match case
def get_params(option):

    params_data = []

    if option == 0:
        all_params = select_clothes()
    elif option == 1:
        all_params = select_service()
    elif option == 2:
        all_params = select_priority()
    else:
        return "Error de estructura interna"

    if isinstance(all_params,str):
        return all_params
    
    else:
        for param in all_params:
            param = (param[0],param[1],param[2])
            params_data.append(param)
        return params_data



# Usar match case
def register_param_db(name,price,option):

    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"

    else:
        verif_res = verif_param_data(name, price,option)

        if isinstance(verif_res,str):
            return f"1|Error al ingresar un nuevo parametro |{verif_res}"
        
        else:

            if option == 0:
                insert_db_res = insert_clothes(verif_res)
            elif option == 1:
                insert_db_res = insert_service(verif_res)
            elif option == 2:
                insert_db_res = insert_priority(verif_res)
            else:
                insert_db_res = "Error de estructura interna"

            if insert_db_res is not None:
                return f"0|Error|{insert_db_res}"
                
            else:
                return "2|Parametro creado|El Parametro a sido creado y registrado con exito"



# Usar match case
def delete_param(id_param,option_param):

    option = messagebox.askyesno("Ultima confirmacion",f"Desea eliminar el parametro?")

    if not option:
        return "1|Accion exitosa|Se aborto la operacion con exito"

    else:
        if option_param == 0:
            delete_res = delete_clothes(id_param)
        elif option_param == 1:
            delete_res = delete_service(id_param)
        elif option_param == 2:
            delete_res = delete_priority(id_param)
        else:
            delete_res = "Error de estructura interna"
        
        if delete_res is not None:
            return f"0|Error|{delete_res}"
        
        else:
            return "1|Accion exitosa|Su accion fue cancelada con exito"



# Usar match case
# Retornar tambien el msg de error
def exist_param(option,price_data_search,parameter):

    if option == 0:
        price_data = select_clothes()
    elif option == 1:
        price_data = select_service()
    elif option == 2:
        price_data = select_priority()
    else:
        return None

    for price in price_data:
        if price[parameter] == price_data_search:
            return price
    return None



# Retornar tambien el msg de error
# Usar las clases
def verif_param_data(name,price,option):
    
    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de parametro valido"
    
    if price == "" or not is_a_number(price) or len(price) > 20 or price == "0":
        return "El precio no es valido"

    res_search = exist_param(option,name,0)

    if res_search is not None:
        return "Ese nombre de parametro ya existe"
    
    param = Parametro(name,price)
    return param



# Usar el check_conection
# Usar match case
def modify_params(name, price, ide, option):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_param_data(name, price, option)

        if isinstance(verif_res,str):
            return f"1|Error al modificar el parametro|{verif_res}"
        else:

            if option == 0:
                modify_param_res = update_clothes(verif_res,ide)
            elif option == 1:
                modify_param_res = update_service(verif_res,ide)
            else:
                modify_param_res = update_priority(verif_res,ide)

            if modify_param_res is not None:
                return f"0|Error|{modify_param_res}"
                    
            else:
                return "2|Parametro modificado|Los datos del Parametro fueron modificados con exito"



def get_orders():
    all_orders = select_order()
    priorities = ["Baja","Media","Alta"]
    order_data = []

    if isinstance(all_orders,str):
        return all_orders
    
    else:
        for order in all_orders:
            order_data.append((order[0],order[1],order[2],order[3],priorities[int(order[4])],order[5],order[6],order[7]))
        return order_data



# Retornar tambien el msg de error
def exist_order(order_data_search,parameter):
    order_data = select_order()

    if isinstance(order_data,str):
        return order_data
    else:
        for order in order_data:
            if order[parameter] == order_data_search:
                return order
        return None



# Retornar tambien el msg de error
# Usar las clases
def verif_order_data(status,ide):
    
    if len(status) < 2:
        return "Selecione un estado"

    res_search = exist_order(ide,0)

    if isinstance(res_search,str):
        return res_search
    
    elif res_search is None:
        return "Ese pedido no existe"
    
    return None



# Usar el check_conection
def modify_orders(status,ide):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_order_data(status,ide)

        if verif_res is not None:
            return f"1|Error al modificar al pedido|{verif_res}"

        else:
            modify_order_res = update_order(status,ide)

            if modify_order_res is not None:
                return f"0|Error|{modify_order_res}"
                
            else:
                return f"2|Usuario modificado|Los datos del Usuario fueron modificados con exito"   