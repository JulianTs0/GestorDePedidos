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



def exist_admin(user_data_search,parameter):
    users_data = select_admin()

    for user in users_data:
        if user[parameter] == user_data_search:
            return user
    return None



def verify_admin(name,password):

    if name == "" or password == "":
        return "Complete los campos antes de iniciar sesion"
    
    elif not is_a_valid_char(name) or len(name) > 30 :
        return "Ingrese un nombre de usuario valido"
    
    elif len(password) > 20:
        return "Ingrese una contraseña valida"
    
    else:
        return None



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
        
            if res_search is None:
                return "El administrador no existe"
            
            else:
                if res_search[2] != user_password:
                    return "Contraseña incorrecta"
                
                else:
                    if res_search[3] == "conectado":
                        return "El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                    else:
                        user_state_switch(res_search[1],True)
                        return Admin(res_search[1],res_search[2])               



def de_login(user_name,force=False):

    if not force:

        res_search = exist_admin(user_name,1)

        if res_search is None:
            return "El usuario que incio sesion dejo de estar registrado en la base de datos"
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
def verif_new_admin_data(name,password,password_rep,ide=None):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de usuario valido"
    
    elif password == "" or len(password) > 20:
        return "No se ha ingresado la contraseña valida"
    
    elif password != password_rep:
        return "Las contraseñas no coinciden"

    res_search = exist_admin(name,1)
    
    if res_search is not None:
        return "Ese nombre de usuario ya existe escoja otro"
    
    if ide is not None:
        return exist_admin(ide,0)
    
    user = Admin(name,password)
    return user 



def register_admin_db(name,password,rep):

    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"

    else:
        verif_res = verif_new_admin_data(name, password, rep)

        if isinstance(verif_res,str):
            return f"1|Error al registrar la cuenta|{verif_res}"
        
        else:
            insert_db_res = insert_admin(verif_res)

            if insert_db_res is not None:
                return f"0|Error|{insert_db_res}"
                
            else:
                return "2|Administrador registrado|El Administrador a sido creado y registrado con exito"



def modify_admin(name,password,rep,ide):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_new_admin_data(name, password, rep, ide)

        if not isinstance(verif_res,str):
            return "1|Error al modificar al usuario|No se puede modificar un usuario que no existe"

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



def exist_user(user_data_search,parameter):
    users_data = select_user()

    for user in users_data:
        if user[parameter] == user_data_search:
            return user
    return None



def get_users():
    all_users = select_user()
    users_data = []

    if isinstance(all_users,str):
        return all_users
    
    else:
        for usuario in all_users:
            usuario = (usuario[0],usuario[1],usuario[2])
            users_data.append(usuario)
        return users_data



# Esta funcion no tiene en cuenta que el email nuevo ya exista
def verif_user_data(name,email):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de usuario valido"
    
    elif "@gmail.com" not in email or len(email) <= 10 or email == "" or len(email) > 40:
        return "La estructura del email no es correcta"

    res_search = exist_user(name,0)

    if res_search is not None:
        return "Ese nombre de usuario ya existe escoja otro"
    
    user = Usuario(name,email)
    return user



def modify_user(name,email,ide):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_user_data(name, email)

        if isinstance(verif_res,str):
            return f"1|Error al modificar al usuario|{verif_res}"

        else:
            modify_user_res = update_user(verif_res,ide)

            if modify_user_res is not None:
                return f"0|Error|{modify_user_res}"
                    
            else:
                return "2|Usuario modificado|Los datos del Usuario fueron modificados con exito"



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



def exist_param(price_data_search,parameter,option):

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



def verif_param_data(name,price,option):
    
    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de parametro valido"
    
    if not is_a_number(price) or len(str(price)) > 20:
        return "El precio no es valido"

    res_search = exist_param(name,0,option)

    if res_search is not None:
        return "Ese nombre de parametro ya existe"
    
    return None



def modify_params(name, price, ide, option):
    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_param_data(name, price, option)

        if verif_res is not None:
            return f"1|Error al modificar el parametro|{verif_res}"
        else:
            param_select = Parametro(name,price)
            
            if option == 0:
                modify_param_res = update_clothes(param_select,ide)
            elif option == 1:
                modify_param_res = update_service(param_select,ide)
            else:
                modify_param_res = update_priority(param_select,ide)

            if modify_param_res is not None:
                return f"0|Error|{modify_param_res}"
                    
            else:
                return "2|Parametro modificado|Los datos del Parametro fueron modificados con exito"



def get_orders():
    all_orders = select_order()
    order_data = []

    if all_orders == "Error al mostrar los datos del usuario":
        return False,all_orders
    
    else:
        for order in all_orders:
            order = (order[0],order[1],order[2],order[3],order[4],order[5],order[6],order[7])
            order_data.append(order)
        return True,order_data



def exist_order(order_data_search,parameter):
    order_data = select_order()

    if order_data == "Error al mostrar los datos del pedido":
        return False,order_data
    else:
        for order in order_data:
            if order[parameter] == order_data_search:
                return True,order
        return True,None



def verif_order_data(status,ide):
    
    if len(status) < 2:
        error_msg = "Selecione un estado"
        return False,error_msg

    status_search,res_search = exist_order(ide,0)

    if not status_search:
        return status_search,res_search
    
    elif res_search is None:
        return False,"Ese pedido no existe"
    
    return True,None



def modify_orders(status,ide):
    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_order_data(status,ide)

        if not verif_state:
            return (1,"Error al modificar al pedido", verif_res)
        else:
            modify_order_res = update_order(status,ide)

            if modify_order_res is not None:
                return (0,"Error",modify_order_res)
                    
            else:
                return (2,"Usuario modificado","Los datos del Usuario fueron modificados con exito")    