from clases_admin import *
from tkinter import messagebox
from tkinter import *
from smtplib import *
from database_admin import *
from decouple import config



def is_a_number(number):

    output = True
    valid_number = "0123456789"

    for i in number:
        if i not in valid_number:
            output = False
    
    return output



def is_a_valid_char(word):

    output = True
    valid_char = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZÀÈÌÒÙàèìòù "

    for i in word:
        if i not in valid_char:
            output = False
    
    return output



def exist_admin(user_data_search,parameter):
    users_data = select_admin()

    for user in users_data:
        if user[parameter] == user_data_search:
            return user
    return None

#    users_data = select_admin()
# 
#    if users_data == "Error al mostrar los datos del admin":
#        return False,users_data
#    else:
#       for user in users_data:
#            if user[parameter] == user_data_search:
#                return True,user
#        return True,None



def verify_admin(name,password):

    if name == "" or password == "":
        return False,"Complete los campos antes de iniciar sesion"
    
    elif not is_a_valid_char(name) or len(name) > 30 :
        return False,"Ingrese un nombre de usuario valido"
    
    elif len(password) > 20:
        return False,"Ingrese una contraseña valida"
    
    else:
        return True,None



def login_admin(user_name,user_password):

    verif_state,verif_res  = verify_admin(user_name,user_password)

    if not verif_state:
        return False, verif_res
    
    else:
        check_conection = conect_DB()

        if check_conection == "Error al conectarse a la base de datos":
            return False,check_conection
        
        else:
            res_search = exist_admin(user_name,1)
        
            if res_search is None:
                return "El administrador no existe"
            
            else:
                if res_search[2] != user_password:
                    return False,"Contraseña incorrecta"
                
                else:
                    if res_search[3] == "conectado":
                        return False,"El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                    else:
                        user_state_switch(res_search[1],True)
                        return True,Admin(res_search[1],res_search[2])               



def de_login(user_name):

    res_search = exist_admin(user_name,1)

    if res_search is None:
        return False,"El usuario que incio sesion dejo de estar registrado en la base de datos"
    else:
        if res_search[2] == "desconectado" or res_search[2] is None:
            return False,"La sesion no se puede cerrar porque el usuario no esta conectado"
        else:
            user_state_switch(user_name,False)
            return True,"La sesion fue cerrada con exito"



def get_admins(user):
    all_admins = select_admin()
    admins_data = []

    if all_admins == "Error al mostrar los datos del admin":
        return False,all_admins
    
    else:
        for admin in all_admins:
            if admin[1] != user.name:
                admin = (admin[0],admin[1],admin[2])
                admins_data.append(admin)
        return True,admins_data



def verif_admin_data(name,password,password_rep,ide=None):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        error_msg = "Ingrese un nombre de usuario valido"
        return False,error_msg
    
    elif password == "" or len(password) > 20:
        error_msg = "No se ha ingresado la contraseña valida"
        return False,error_msg
    
    elif password != password_rep:
        error_msg = "Las contraseñas no coinciden"
        return False,error_msg

    res_search = exist_admin(name,1)
    
    if res_search is not None:
        return False,"Ese nombre de usuario ya existe escoja otro"
    
    if ide is not None:
        return exist_admin(ide,0)
    
    user = Admin(name,password)
    return True,user 



def register_admin_db(name,password,rep):

    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_admin_data(name, password, rep)

        if not verif_state:
            return (1,"Error al registrar la cuenta", verif_res)
        
        else:
            insert_db_res = insert_admin(verif_res)

            if insert_db_res is not None:
                return (0,"Error",insert_db_res)
                    
            else:
                return (2,"Administrador registrado","El Administrador a sido creado y registrado con exito")



def name_for_id(name):
    ides = get_admin_id()

    for data in ides:
        if data[1] == name:
            return data[0]



def modify_admin(name,password,rep,ide):
    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_admin_data(name, password, rep, ide)

        if verif_state:
            return (1,"Error al modificar al usuario", "No se puede modificar un usuario que no existe")
        else:
            admin = Admin(name,password)
            modify_admin_res = update_admin(admin,ide)

            if modify_admin_res is not None:
                return (0,"Error",modify_admin_res)
                    
            else:
                return (2,"Administrador modificado","Los datos del administrador fueron modificados con exito")



def delete_admin_user(id_admin):

    option = messagebox.askyesno("Ultima confirmacion",f"Desea eliminar al administrador?")
    if not option:
        return True,"Se aborto la operacion con exito"
    else:
        delete_res = delete_admin(id_admin)
        if delete_res is not None:
            return False,delete_res
        else:
            return True,"Su pedido fue cancelado con exito"



def exist_user(user_data_search,parameter):
    users_data = select_user()

    if users_data == "Error al mostrar los datos del usuario":
        return False,users_data
    else:
        for user in users_data:
            if user[parameter] == user_data_search:
                return True,user
        return True,None



def get_users():
    all_users = select_user()
    users_data = []

    if all_users == "Error al mostrar los datos del usuario":
        return False,all_users
    
    else:
        for usuario in all_users:
            usuario = (usuario[0],usuario[1],usuario[2])
            users_data.append(usuario)
        return True,users_data



def verif_user_data(name,email):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        error_msg = "Ingrese un nombre de usuario valido"
        return False,error_msg
    
    elif "@gmail.com" not in email or len(email) <= 10 or email == "" or len(email) > 40:
        error_msg = "La estructura del email no es correcta"
        return False,error_msg

    status_search,res_search = exist_user(name,1)

    if not status_search:
        return status_search,res_search
    
    elif res_search is None:
        return False,"Ese nombre de usuario ya existe escoja otro"
    
    return True,None



def modify_user(name,email,ide):
    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_user_data(name, email)

        if verif_state:
            return (1,"Error al modificar al usuario", "No se puede modificar un usuario que no existe")
        else:
            usuario = Usuario(name,email)
            modify_user_res = update_user(usuario,ide)

            if modify_user_res is not None:
                return (0,"Error",modify_user_res)
                    
            else:
                return (2,"Usuario modificado","Los datos del Usuario fueron modificados con exito")



def get_params(option):

    if option == 0:
        all_params = select_clothes()
    elif option == 1:
        all_params = select_service()
    else:
        all_params = select_priority()
    
    params_data = []

    if all_params == "Error al mostrar los datos del usuario":
        return False,all_params
    
    else:
        for param in all_params:
            param = (param[0],param[1],param[2])
            params_data.append(param)
        return True,params_data



def exist_param(price_data_search,parameter,option):

    if option == 0:
        price_data = select_clothes()
    elif option == 1:
        price_data = select_service()
    else:
        price_data = select_priority()

    if price_data == "Error al mostrar los datos del usuario":
        return False,price_data
    else:
        for price in price_data:
            if price_data[parameter] == price_data_search:
                return True,price_data
        return True,None



def verif_param_data(name,price,option):
    
    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        error_msg = "Ingrese un nombre de parametro valido"
        return False,error_msg
    
    elif is_a_number(price) or len(price) > 40:
        error_msg = "El precio no es valido"
        return False,error_msg

    status_search,res_search = exist_param(name,0,option)

    if not status_search:
        return status_search,res_search
    
    elif res_search is None:
        return False,"Ese parametro no existe"
    
    return True,None



def modify_params(name, price, ide, option):
    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_param_data(name, price, option)

        if verif_state:
            return (1,"Error al modificar el parametro", "No se puede modificar un parametro que no existe")
        else:
            param_select = Parametro(name,price)
            
            if option == 0:
                modify_param_res = update_clothes(param_select,ide)
            elif option == 1:
                modify_param_res = update_service(param_select,ide)
            else:
                modify_param_res = update_priority(param_select,ide)

            if modify_param_res is not None:
                return (0,"Error",modify_param_res)
                    
            else:
                return (2,"Parametro modificado","Los datos del Parametro fueron modificados con exito")



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