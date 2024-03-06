from clases import *
from tkinter import *
from tkinter import messagebox
from smtplib import *
from database import *
from decouple import config
import random

#   Mini es una ventana que se usa exclusivamente para poder verificar el codigo de verificacion de email
#   con el ingresado por el usuario en esta misma ventana. A esta ventana ademas de pasarle parametros de
#   inicializacion se le pasa el parametro verif el cual es el numero que fue enviado al email y parent el
#   cual hace referencia a la estrucutra register la cual posee una variable booleana llamada ok, que determina
#   si el proceso de registro definitivo esta terminado, sin ningun inconveniente, y listo para ingresar
#   en la base de datos.

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
    
    #   La funcion aunthrntication es la estructura peronalizada hecha exclusivamente para la ventana Mini
    #   la cual crea todos los widgets que se van a mostrar.

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
    
    #   La funcion verification lo que hace es comparar el numero ingresado en el entry main_input y la
    #   variable verif la cual es el numero de verificacion enviado por emial, si coinciden setea en true
    #   la variable ok y llama a la funcion close, si no simplemente muestra un mensaje de error.

    def verification(self,input_code,verif_number,register_struct):
        
        if input_code == verif_number:
            register_struct.ok = True
            self.close_mini_window(self)
        else:
            messagebox.showerror("Error al verifcar su email","El codigo ingresado es incorrecto")
    
    #   La funcion close cierra y termina definitivamente los procesos de la ventana Mini

    def close_mini_window(self,object):
        object.quit()
        object.destroy()

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

    if users_data == "Error al mostrar los datos del ususario":
        return False,users_data
    else:
        for user in users_data:
            if user[parameter] == user_data_search:
                return True,user
        return True,None

#   La funcion register_user basicamente es la que se encarga de las validaciones iniciales de los valores
#   ingresados durante el proceso de registro de una nueva cuenta en la estructura Register. Si todo esta 
#   correcto devuelve un objeto de tipo Usuario, si no devuelve un string el cual contiene el motivo del
#   fallo de la validacion.

def verif_new_user_data(name,password,password_rep,email):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        error_msg = "Ingrese un nombre de usuario valido"
        return False,error_msg
    
    elif "@gmail.com" not in email or len(email) <= 10 or email == "" or len(email) > 40:
        error_msg = "La estructura del email no es correcta"
        return False,error_msg
    
    elif password == "" or len(password) > 20:
        error_msg = "No se ha ingresado la contraseña valida"
        return False,error_msg
    
    elif password != password_rep:
        error_msg = "Las contraseñas no coinciden"
        return False,error_msg


    status_search,res_search = exist_user(name,0)

    if not status_search:
        return status_search,res_search
    
    elif res_search is not None:
        return False,"Ese nombre de usuario ya existe escoja otro"
        
    status_search,res_search = exist_user(email,2)

    if not status_search:
        return status_search,res_search
    
    elif res_search is not None:
        return False,"Ese email ya esta registrado"
        
    user = Usuario(name,password,email)
    return True,user 

#   La funcion send_email es la que se encarga de enviar un email que contiene el numero de verificacion
#   al email del usuario que pretende registrarse. El remitente del email y la contraseña de dicha cuenta 
#   se acceden a traves del archivo .env donde en USER se encuentra el nombre de la cuenta de email del 
#   remitente y en PASSWORD se encuentra una contraseña de aplicacion generada para acceder a la cuenta
#   del remitente. Si logra enviar el email devuelve el numero de verificacion generado, si no devuelve
#   un string de error.

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

        return True,autenti_number
    except:
        return False,"Error al envial el mail, verifique que el remitente o el destinatario"

#   La funcion register_in_db es la que se encarga de validar completamente los datos ingresados en la 
#   operacion de registro de una nueva cuenta, y si todos estan correctos registra los datos en la BD. 
#   Esta funcion siempre devuelve una tupla de 3 elementos, los cuales son utilizados en la estructura
#   register para informarle al usuario la situacion del registro de su cuenta, el primer elemento es un
#   numero que representa si el mensaje es un error, una advertencia o informacion, el segundo elemento
#   es el titulo del mensaje y el tercero es el cuerpo del mensaje.
#   Las validaciones se hacen en el siguiente orden:
#   1. Se verifica si se puede conectar a la base de datos, si se puede se continua
#   2. Se verifica si los datos ingresados son correctos, si son correctos se continua
#   3. Se envia el email con el codigo de verifiacion, si se logro enviar el email se continua
#   4. Se abre la ventana Mini para pedir el codigo de verifiacion, si no se cancela el proceso se continua
#   5. Se trata de registrar los datos a la BD, si se puede se cierra la ventana Extra asociada al Register
#   y se finaliza el proceso de registro.

def register_in_db(register_struct,main_window,name,password,rep,email):

    check_conection = conect_DB()

    if check_conection == "Error al conectarse a la base de datos":
        return (0,"Error", str(check_conection))
    
    else:
        verif_state,verif_res = verif_new_user_data(name, password, rep, email)

        if not verif_state:
            return (1,"Error al registrar la cuenta", verif_res)
        
        else:
            email_state,email_res = send_email_autenti(verif_res.email)

            if not email_state:
                return (1,"Error de email", email_res)
            
            else:
                print(email_res)
                Mini(f"Verificacion del email", (400,150,100,50), True, "black", email_res, register_struct)
                register_struct.lift()

                if register_struct.ok == False:
                    return (1,"Registro cancelado","Vuelva a ingresar los datos para registrar una cuenta")
                
                else:
                    insert_db_res = insert_user(verif_res)

                    if insert_db_res is not None:
                       return (0,"Error",insert_db_res)
                    
                    else:
                        main_window.quit()
                        main_window.destroy()
                        return (2,"Usuario registrado","El usuario a sido creado y registrado con exito ingrese sesion en la pagina principal")
                           
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
                    if res_search[3] == "conectado":
                        return False,"El usuario ingresado ya se encuentra logeado en otro dispositivo"
                    
                    else:
                        user_state_switch(res_search[0],True)
                        return True,Usuario(res_search[0],res_search[1],res_search[2])
                    
                           

#
#
# 

def de_login(user_name):

    state_search,res_search = exist_user(user_name,0)

    if not state_search:
        return False,"El usuario que incio sesion dejo de estar registrado en la base de datos"
    else:
        if res_search[3] == "desconectado":
            return False,"La sesion no se puede cerrar porque el usuario no esta conectado"
        else:
            user_state_switch(user_name,False)
            return True,"La sesion fue cerrada con exito"

#
#
#
        
def verifiy_order(ropa,servicio,prioridad,comentario):

    if ropa == "" or servicio == "" or prioridad == "":
        return False,"Complete los campos antes de hacer un pedido"
    
    else:
        order = Pedido(ropa,servicio,prioridad,comentario)
        return True,order

#
#
#

def create_order_db(ropa,servicio,prioridad,conentario,user):

    if conentario[-1] == "\n":
            conentario = conentario[:-1]

    state_order,res_order = verifiy_order(ropa,servicio,prioridad,conentario)

    if not state_order:
       return 1,"Error al realizar el pedido",res_order
    
    else:
        option = messagebox.askyesno("Ultima confirmacion",f"El precio del pedido es de {res_order.precio} desea continuar?")
        if not option:
            return 2,"Pedido cancelado","Se cancelo el pedido"
        
        else:
            insert_res = insert_order(res_order,user)
            if insert_res is not None:
                return 0,"Error",insert_res
            
            else:
                return 2,"Pedido creado","Se pudo realizar el pedido exitosamente"

#
#
#

def get_user_orders(user):

    all_orders = select_order()
    display_orders = []

    if all_orders == "Error al mostrar los pedidos del ususario":
        return False,all_orders
    
    else:
        for order in all_orders:
            if order[1] == user.name:
                order = [order[0],order[2],order[3],order[4],order[5],order[6]]
                display_orders.append(order)
        return True,display_orders

#
#
#

def delete_order(id_order):

    option = messagebox.askyesno("Ultima confirmacion",f"Desea cancelar su pedido?")
    if not option:
        return True,"Se aborto la operacion con exito"
    else:
        delete_res = delete_order_db(id_order)
        if delete_res is not None:
            return False,delete_res
        else:
            return True,"Su pedido fue cancelado con exito"

    