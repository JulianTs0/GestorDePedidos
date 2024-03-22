from clases_admin import *
from tkinter import messagebox
from tkinter import *
from smtplib import *
from database_admin import *
from decouple import config

#   La funcion is_a_number determina si en una palabra esta contiene algun numero, si es asi retorna true
#   si no false.

def is_a_valid_char(word):

    output = True
    valid_char = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZÀÈÌÒÙàèìòù "

    for i in word:
        if i not in valid_char:
            output = False
    
    return output

#
#
#

def exist_user(user_data_search,parameter):
    users_data = select_user()

    if users_data == "Error al mostrar los datos del admin":
        return False,users_data
    else:
        for user in users_data:
            if user[parameter] == user_data_search:
                return True,user
        return True,None

#
#
#

def verify_user(name,password):

    if name == "" or password == "":
        return False,"Complete los campos antes de iniciar sesion"
    
    elif not is_a_valid_char(name) or len(name) > 30 :
        return False,"Ingrese un nombre de usuario valido"
    
    elif len(password) > 20:
        return False,"Ingrese una contraseña valida"
    
    else:
        return True,None

#
#
#

def login_user(user_name,user_password):

    verif_state,verif_res  = verify_user(user_name,user_password)

    if not verif_state:
        return False, verif_res
    
    else:
        check_conection = conect_DB()

        if check_conection == "Error al conectarse a la base de datos":
            return False,check_conection
        
        else:
            state_search,res_search = exist_user(user_name,1)
        
            if not state_search:
                return state_search,res_search
        
            else:
                if res_search is None:
                    return False,"El usuario no existe"
            
                else:
                    if res_search[2] != user_password:
                        return False,"Contraseña incorrecta"
                
                    else:
                        if res_search[3] == "conectado":
                            return False,"El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                        else:
                            user_state_switch(res_search[1],True)
                            return True,Admin(res_search[1],res_search[2])               

#
#
# 

def de_login(user_name):

    state_search,res_search = exist_user(user_name,1)

    if not state_search:
        return False,"El usuario que incio sesion dejo de estar registrado en la base de datos"
    else:
        if res_search[2] == "desconectado":
            return False,"La sesion no se puede cerrar porque el usuario no esta conectado"
        else:
            user_state_switch(user_name,False)
            return True,"La sesion fue cerrada con exito"

#
#
# 

def get_admins(user):
    all_admins = select_user()
    admins_data = []

    if all_admins == "Error al mostrar los datos del admin":
        return False,all_admins
    
    else:
        for admin in all_admins:
            if admin[1] != user.name:
                admin = (admin[0],admin[1],admin[2])
                admins_data.append(admin)
        return True,admins_data

#
#
#

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

    status_search,res_search = exist_user(name,1)

    if not status_search:
        return status_search,res_search
    
    elif res_search is not None:
        return False,"Ese nombre de usuario ya existe escoja otro"
    
    if ide is not None:
        return exist_user(ide,0)
    
    user = Admin(name,password)
    return True,user 

#
#
#

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

#
#
#

def name_for_id(name):
    ides = get_admin_id()

    for data in ides:
        if data[1] == name:
            return data[0]

#
#
#

def modify_admin(name,password,rep,ide):
    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_admin_data(name, password, rep, ide)

        if not verif_state:
            return (1,"Error al modificar al usuario", verif_res)
        else:
            admin = Admin(name,password)
            modify_admin_res = update_admin(admin,ide)

            if modify_admin_res is not None:
                return (0,"Error",modify_admin_res)
                    
            else:
                return (2,"Administrador modificado","Los datos del administrador fueron modificados con exito")

#
#
#

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