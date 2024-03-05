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
    def __init__(self, tittle, size, resize, back_color, verif, parent):

        #setup

        super().__init__()
        self.title(tittle)
        self.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
        self.resizable(resize, resize)
        self.config(bg=back_color)
        self.attributes("-topmost", True)
        self.grab_set() #Hace que lo que este pasando en la pagina principal se congele
        self.protocol("WM_DELETE_WINDOW", lambda: self.close(self))

        #strcut

        self.authentication(verif,parent)

        #loop

        self.mainloop()
    
    #   La funcion aunthrntication es la estructura peronalizada hecha exclusivamente para la ventana Mini
    #   la cual crea todos los widgets que se van a mostrar.

    def authentication(self ,verif, parent):

        #var

        code = IntVar()

        #create

        main_label = Label(self, bg="red", text="Ingrese el codigo que le enviamos al email", wraplength=150)
        main_input = Entry(self, textvariable=code)
        main_button = Button(self, text="Verificar", bg="blue", fg="white", command=lambda : self.verification(code.get(),verif,parent))
        
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

    def verification(self,var,verif,parent):
        
        if var == verif:
            parent.ok = True
            self.close(self)
        else:
            messagebox.showerror("Error al verifcar su email","El codigo ingresado es incorrecto")
    
    #   La funcion close cierra y termina definitivamente los procesos de la ventana Mini

    def close(self,object):
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

def exist_user(search,parameter):
    data = buscarUsuario()

    if data == "Error al mostrar los datos del ususario":
        return False,data
    else:
        for row in data:
            if row[parameter] == search:
                return True,row
        return True,None

#   La funcion register_user basicamente es la que se encarga de las validaciones iniciales de los valores
#   ingresados durante el proceso de registro de una nueva cuenta en la estructura Register. Si todo esta 
#   correcto devuelve un objeto de tipo Usuario, si no devuelve un string el cual contiene el motivo del
#   fallo de la validacion.

def register_user(name,password,rep,email):

    if name == "" or not is_a_valid_char(name) or len(name) > 30:
        error = "Ingrese un nombre de usuario valido"
        return False,error
    
    if "@gmail.com" not in email or len(email) <= 10 or email == "" or len(email) > 40:
        error = "La estructura del email no es correcta"
        return False,error
    
    if password == "" or len(password) > 20:
        error = "No se ha ingresado la contraseña valida"
        return False,error
    
    if password != rep:
        error = "Las contraseñas no coinciden"
        return False,error

    search = exist_user(name,0)
    if not search[0]:
        return search
    elif search[1] is not None:
        return False,"Ese nombre de usuario ya existe escoja otro"
        
    search = exist_user(email,2)
    if not search[0]:
        return search
    elif search[1] is not None:
        return False,"Ese email ya esta registrado"
        
    user = Usuario(name,password,email)
    return True,user 

#   La funcion send_email es la que se encarga de enviar un email que contiene el numero de verificacion
#   al email del usuario que pretende registrarse. El remitente del email y la contraseña de dicha cuenta 
#   se acceden a traves del archivo .env donde en USER se encuentra el nombre de la cuenta de email del 
#   remitente y en PASSWORD se encuentra una contraseña de aplicacion generada para acceder a la cuenta
#   del remitente. Si logra enviar el email devuelve el numero de verificacion generado, si no devuelve
#   un string de error.

def send_email(mail):
    try:
        autentificacion = random.randint(10000,999999)
        msg = f"Subject: Mensaje de autentificacion de mail\n\nIngrese el siguiente codigo para terminar de registrar su cuenta en el sistema\nEl codigo es : {autentificacion}"
        remitente = config("USER_GMAIL")
        contra = config("PASSWORD_GMAIL")

        server = SMTP("smtp.gmail.com" ,587)
        server.starttls()
        server.login(remitente, contra)

        server.sendmail(remitente, mail, msg)

        server.quit()

        return True,autentificacion
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

def register_in_db(self,parent,name,password,rep,email):

    check = conectBD()

    if check == "Error al conectarse a la base de datos":
        return (0,"Error", str(check))
    else:
        re_user = register_user(name, password, rep, email)
        if re_user[0]:
            email_number = send_email(re_user[1].email)
            if email_number[0]:
                print(email_number[1])
                Mini(f"Verificacion del email", (400,150,100,50), True, "black", email_number[1], self)
                if self.ok == False:
                    return (1,"Registro cancelado","Vuelva a ingresar los datos para registrar una cuenta")
                else:
                    res = ingresarUsuarios(re_user[1])
                    if res is None:
                        parent.quit()
                        parent.destroy()
                        return (2,"Usuario registrado","El usuario a sido creado y registrado con exito ingrese sesion en la pagina principal")
                    else:
                        return (0,"Error",res)
            else:
                return (1,"Error de email", email_number[1])
        else:
            return (1,"Error al registrar la cuenta", re_user[1])

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

def login_user(user):

    verify_key  = verify_user(user[0],user[1])

    if verify_key[0]:
        data = exist_user(user[0],0)
        
        if not data[0]:
            return data
        else:
            if data[1] is not None:
                if data[1][1] == user[1]:
                    if data[1][3] == "desconectado":
                        cambiarEstadoUsuario(data[1][0],True)
                        return True,Usuario(data[1][0],data[1][1],data[1][2])
                    else:
                        return False,"El usuario ingresado ya se encuentra logeado en otro dispositivo"
                else:
                    return False,"Contraseña incorrecta"
            else:
                return False,"El usuario no existe"
    else:
        return False, verify_key[1]

#
#
# 

def de_login(user_name):

    data = exist_user(user_name,0)

    if not data[0]:
        return False,"El usuario que incio sesion dejo de estar registrado en la base de datos"
    else:
        if data[1][3] == "conectado":
            cambiarEstadoUsuario(user_name,False)
            return True,"La sesion fue cerrada con exito"
        else:
            return False,"La sesion no se puede cerrar porque el usuario no esta conectado"

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

def create_order_db(data_order,user):

    if data_order[3][-1] == "\n":
            data_order[3] = data_order[3][:-1]

    order = verifiy_order(data_order[0],data_order[1],data_order[2],data_order[3])

    if order[0]:
        opcion = messagebox.askyesno("Ultima confirmacion",f"El precio del pedido es de {order[1].precio} desea continuar?")
        if opcion:
            value = ingresarPedidos(order[1],user)
            if value is None:
                return 2,"Pedido creado","Se pudo realizar el pedido exitosamente"
            else:
                return 0,"Error",value
        else:
            return 2,"Pedido cancelado","Se cancelo el pedido"
    else:
        return 1,"Error al realizar el pedido",order[1]

#
#
#

def get_user_orders(usuario):

    pedidos = buscarPedido()
    user_pedidos = []

    if pedidos == "Error al mostrar los pedidos del ususario":
        return False,pedidos
    else:
        for ped in pedidos:
            if ped[1] == usuario.name:
                ped = [ped[0],ped[2],ped[3],ped[4],ped[5],ped[6]]
                user_pedidos.append(ped)
        return True,user_pedidos

#
#
#

def delete_order(id_order):

    opcion = messagebox.askyesno("Ultima confirmacion",f"Desea cancelar su pedido?")
    if opcion:
        delete = eliminarPedido(id_order)
        if delete is None:
            return True,"Su pedido fue cancelado con exito"
        else:
            return False,delete
    else:
        return True,"Se aborto la operacion con exito"

    