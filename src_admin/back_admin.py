from clases_admin import *
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
            state_search,res_search = exist_user(user_name,0)
        
            if not state_search:
                return state_search,res_search
        
            else:
                if res_search is None:
                    return False,"El usuario no existe"
            
                else:
                    if res_search[1] != user_password:
                        return False,"Contraseña incorrecta"
                
                    else:
                        if res_search[2] == "conectado":
                            return False,"El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                        else:
                            user_state_switch(res_search[0],True)
                            return True,Admin(res_search[0],res_search[1])               

#
#
# 

def de_login(user_name):

    state_search,res_search = exist_user(user_name,0)

    if not state_search:
        return False,"El usuario que incio sesion dejo de estar registrado en la base de datos"
    else:
        if res_search[2] == "desconectado":
            return False,"La sesion no se puede cerrar porque el usuario no esta conectado"
        else:
            user_state_switch(user_name,False)
            return True,"La sesion fue cerrada con exito"
