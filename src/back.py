from clases import *
from tkinter import *
from tkinter import messagebox
from smtplib import *
from database import *
from decouple import config
import random
import os



class Mini(Toplevel):
    def __init__(self, tittle, size, resize, back_color, verif_number, register_struct):

        #setup

        super().__init__()
        self.title(tittle)
        self.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
        self.resizable(resize, resize)
        self.config(bg=back_color)
        self.attributes("-topmost", True)
        self.grab_set() #Hace que lo que este pasando en la pagina principal se congele
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_mini_window(self))

        #strcut

        self.authentication(verif_number,register_struct)

        #loop

        self.mainloop()

    def authentication(self ,verif_number, register_struct):

        #var

        input_code = IntVar()

        #create

        main_label = Label(self, bg="red", text="Ingrese el codigo que le enviamos al email", wraplength=150)
        main_input = Entry(self, textvariable=input_code)
        main_button = Button(self, text="Verificar", bg="blue", fg="white", command=lambda : self.verification(input_code.get(),verif_number,register_struct))
        
        #configure

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        #grid

        main_label.grid(column=0, row=1, sticky="w", padx=10)
        main_input.grid(column=1, row=1, sticky="we")
        main_button.grid(column=2, row=2)

    def verification(self,input_code,verif_number,register_struct):
        
        if input_code == verif_number:
            register_struct.ok = True
            self.close_mini_window(self)
        else:
            messagebox.showerror("Error al verifcar su email","El codigo ingresado es incorrecto")

    def close_mini_window(self,object):
        object.quit()
        object.destroy()



def is_a_valid_char(word):

    valid_char = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZÀÈÌÒÙàèìòù "

    for i in word:
        if i not in valid_char:
            return False
    
    return True



def exist_user(user_data_search,parameter):
    users_data = select_user()

    if isinstance(users_data,str):
        return users_data
    else:
        for user in users_data:
            if user[parameter] == user_data_search:
                return user
        return None



def verif_new_user_data(name,password,password_rep,email):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        return "Ingrese un nombre de usuario valido"
    
    elif "@gmail.com" not in email or len(email) <= 10 or email == "" or len(email) > 40:
        return "La estructura del email no es correcta"
    
    elif password == "" or len(password) > 20:
        return "No se ha ingresado la contraseña valida"
    
    elif password != password_rep:
        return "Las contraseñas no coinciden"

    res_search = exist_user(name,0)
    
    if isinstance(res_search,str):
        return res_search

    elif res_search is not None:
        return "Ese nombre de usuario ya existe escoja otro"
    
    res_search = exist_user(email,2)
    
    if isinstance(res_search,str):
        return res_search
    if res_search is not None:
        return "Ese email ya esta registrado"
    
    user = Usuario(name,password,email)
    return user 



def send_email_autenti(mail):

    try:
        autenti_number = random.randint(10000,999999)
        msg = f"Subject: Mensaje de autentificacion de mail\n\nIngrese el siguiente codigo para terminar de registrar su cuenta en el sistema\nEl codigo es : {autenti_number}"
        remitente = config("USER_GMAIL")
        contra = config("PASSWORD_GMAIL")

        server = SMTP("smtp.gmail.com" ,587)
        server.starttls()
        server.login(remitente, contra)

        server.sendmail(remitente, mail, msg)

        server.quit()

        return autenti_number
    except:
        return "Error al envial el mail, verifique que el remitente o el destinatario"



# Eliminar el print(autenti)
def register_in_db(register_struct,main_window,name,password,rep,email):

    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return f"0|Error|{check_conection}"
    
    else:
        verif_res = verif_new_user_data(name, password, rep, email)

        if isinstance(verif_res,str):
            return f"1|Error al registrar la cuenta|{verif_res}"
        
        else:
            email_res = send_email_autenti(verif_res.email)

            if isinstance(email_res,str):
                return f"1|Error de email|{email_res}"
            
            else:
                print(email_res)
                Mini(f"Verificacion del email", (400,150,100,50), True, "black", email_res, register_struct)
                register_struct.lift()

                if register_struct.ok == False:
                    return "1|Registro cancelado|Vuelva a ingresar los datos para registrar una cuenta"
                
                else:
                    insert_db_res = insert_user(verif_res)

                    if insert_db_res is not None:
                        return f"0|Error|{insert_db_res}"
                    
                    else:
                        main_window.quit()
                        main_window.destroy()
                        return "2|Usuario registrado|El usuario a sido creado y registrado con exito ingrese sesion en la pagina principal"



def verify_user(name,password):

    if name == "" or password == "":
        return "Complete los campos antes de iniciar sesion"
    
    elif not is_a_valid_char(name) or len(name) > 30 :
        return "Ingrese un nombre de usuario valido"
    
    elif len(password) > 20:
        return "Ingrese una contraseña valida"
    
    else:
        return None



def login_user(user_name,user_password):

    verif_res  = verify_user(user_name,user_password)

    if verif_res is not None:
        return verif_res
    
    else:
        check_conection = conect_DB()

        if isinstance(check_conection,str):
            return check_conection
        
        else:
            res_search = exist_user(user_name,0)
        
            if res_search is None:
                return "El usuario no existe"
            
            elif isinstance(res_search,str):
                return res_search

            else:
                if res_search[1] != user_password:
                    return "Contraseña incorrecta"
                
                else:
                    if res_search[3] == "conectado":
                        return "El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                    else:
                        user_state_switch(res_search[0],True)
                        return Usuario(res_search[0],res_search[1],res_search[2])               



def unexpected_delogin():

    check_conection = conect_DB()

    if isinstance(check_conection,str):
        return "Error|Error al conectarse a la base de datos ingrese a la aplicacion mas tarde"

    else:
        if not os.path.exists("local_storage.txt"):
            return ""

        else:
            archivo = open("local_storage.txt","rt")
            user_name = archivo.read()

            if user_name == "":
                return ""

            else:
                user_state_switch(user_name,False)
                archivo = open("local_storage.txt","wt")
                archivo.write("")
                archivo.close()
                return ""



def de_login(user_name):

    check_conection = conect_DB()

    if isinstance(check_conection,str):

        archivo = open("local_storage.txt","wt")
        archivo.write(f"{user_name}")
        archivo.close()
        return "La base de datos se deconecto, se guardo su cierre de sesion"

    else:

        res_search = exist_user(user_name,0)

        if res_search is None:
            return "El usuario que incio sesion dejo de estar registrado en la base de datos"

        elif isinstance(res_search,str):
            return res_search

        else:
            if res_search[3] == "desconectado":
                return "La sesion no se puede cerrar porque el usuario no esta conectado"

            else:
                user_state_switch(user_name,False)
                return None



def verifiy_order(ropa,servicio,prioridad,comentario):

    if ropa == "" or servicio == "" or prioridad == "":
        return "Complete los campos antes de hacer un pedido"
    
    else:
        order = Pedido(ropa,servicio,prioridad,comentario)
        return order



def create_order_db(ropa,servicio,prioridad,conentario,user):

    if conentario[-1] == "\n":
            conentario = conentario[:-1]

    res_order = verifiy_order(ropa,servicio,prioridad,conentario)

    if isinstance(res_order,str):
        return f"1|Error al realizar el pedido|{res_order}"
    
    else:
        if res_order.precio == 0:
            return "0|Error|Se produjo un error al intentar cargar los precios"
        
        else:
            option = messagebox.askyesno("Ultima confirmacion",f"El precio del pedido es de ${res_order.precio} desea continuar?")
            if not option:
                return "2|Pedido cancelado|Se cancelo el pedido"
        
            else:
                insert_res = insert_order(res_order,user)
                if insert_res is not None:
                    return f"0|Error|{insert_res}"

                else:
                    return "2|Pedido creado|Se pudo realizar el pedido exitosamente"



def get_user_orders(user):

    all_orders = select_order()
    priorities = ["Baja","Media","Alta"]
    display_orders = []

    if isinstance(all_orders,str):
        return all_orders

    else:
        for order in all_orders:
            if order[1] == user.name:
                display_orders.append((order[0],order[2],order[3],priorities[int(order[4])],order[5],order[6]))
        return display_orders



def state_order(id_order):
    all_orders = select_order()

    if isinstance(all_orders,str):
        return all_orders

    else:
        for order in all_orders:
            if order[0] == id_order and order[6] == "Espera":
                return None
        return "No se puede cancelar el pedido ya que fue aceptado"



def delete_order(id_order):

    search_res = state_order(id_order)

    if search_res is not None:
        return search_res
    else:
        option = messagebox.askyesno("Ultima confirmacion",f"Desea cancelar su pedido?")
        if not option:
            return "Se aborto la operacion con exito"
        else:
            delete_res = delete_order_db(id_order)
            if delete_res is not None:
                return delete_res
            else:
                return None



def get_fields_name(name):

    conect = conect_DB()

    if isinstance(conect,str):
        return None

    else:
        field_data = get_service_stock_data(name)

        if isinstance(field_data,str):
            return None

        else:

            aux = []
            for i in field_data:
                aux.append(i[0])

            return aux