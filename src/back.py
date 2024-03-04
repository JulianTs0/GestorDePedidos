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

def is_a_number(word):

    output = False

    for i in word:
        if i in "0123456789":
            output = True
    
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

    if name == "" or is_a_number(name):
        error = "Ingrese un nombre de usuario valido"
        return False,error
    
    if "@gmail.com" not in email or len(email) <= 10 or email == "":
        error = "La estructura del email no es correcta"
        return False,error
    
    if password == "":
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

def login_user(name,password):

    if name == "" or password == "":
        return False,"Complete los campos antes de iniciar sesion"
    
    data = exist_user(name,0)

    if not data[0]:
        return data
    else:
        if data[1] is not None:
            if data[1][1] == password:
                return True,"Inicio de sesion exitoso"
            else:
                return False,"Contraseña incorrecta"
        else:
            return False,"El usuario no existe"