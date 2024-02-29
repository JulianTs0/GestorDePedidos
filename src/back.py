from clases import *
from tkinter import *
from tkinter import messagebox
from smtplib import *
from database import *
from decouple import config
import random

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
    
    def authentication(self ,verif, parent):

        #var

        code = IntVar()

        #create

        main_label = Label(self ,bg="red" ,text="Ingrese el codigo que le enviamos al email", wraplength=150)
        main_input = Entry(self ,textvariable=code)
        main_button = Button(self, text="Verificar" ,bg="blue" ,fg="white", command=lambda : self.verification(code.get(),verif,parent))
        exit_button = Button(self, text="Cancelar" ,bg="white" ,fg="black", command=lambda : self.close(self))

        #configure

        self.columnconfigure((0,1,2) ,weight=1)
        self.rowconfigure((0,1,2) ,weight=1)

        #grid

        main_label.grid(column=0, row=1, sticky="w", padx=10)
        main_input.grid(column=1, row=1, sticky="we")
        main_button.grid(column=2, row=2)
        exit_button.grid(column=0, row=2,sticky="w", padx=10)
    
    def verification(self,var,verif,parent):
        
        if var == verif:
            parent.ok = True
            self.close(self)
        else:
            messagebox.showerror("Error al verifcar su email","El codigo ingresado es incorrecto")
    
    def close(self,object):
        object.quit()
        object.destroy()

def is_a_number(word):

    output = False

    for i in word:
        if i in "0123456789":
            output = True
    
    return output

def register_user(name,password,rep,email):

    error = None

    if password != rep:
        error = "Las contraseñas no coinciden"

    if password == "":
        error = "No se ha ingresado la contraseña valida"

    if "@gmail.com" not in email or len(email) <= 10 or email == "":
        error = "La estructura del email no es correcta"

    if name == "" or is_a_number(name):
        error = "Ingrese un nombre de usuario valido"
    
    if error is None:
        user = Usuario(name,password,email)
        return user
    else:
        return error  

def send_email(mail):
    try:
        autentificacion = random.randint(10000,999999)
        msg = f"Subject: Mensaje de autentificacion de mail\n\nIngrese el siguiente codigo para terminar de registrar su cuenta en el sistema\nEl codigo es : {autentificacion}"
        remitente = config("USER_GMAIL")
        contra = config("PASSWORD_GMAIL")

        server = SMTP("smtp.gmail.com" ,587)
        server.starttls()
        server.login(remitente ,contra)

        server.sendmail(remitente ,mail ,msg)

        server.quit()

        return autentificacion
    except:
        return "Error al envial el mail, verifique que el remitente o el destinatario"

def check_conection():
    if type(conectBD()) == "<class 'str'>":
        return conectBD()
    else:
        return None

def register_in_db(self,parent,name,password,rep,email):
    showmsg = None

    if check_conection() is not None:
        showmsg = (0,"Error", str(check_conection()))
    else:
        user = register_user(name ,password ,rep ,email)
        try:
            number = send_email(user.email)
            try:
                number = int(number)
                Mini(f"Verificacion del email", (400,150,100,50), True, "black", number, self)
                if self.ok == False:
                    showmsg = (1,"Registro cancelado","Vuelva a ingresar los datos para registrar una cuenta")
                    parent.quit()
                    parent.destroy()
                else:
                    res = ingresarUsuarios(user)
                    if res is None:
                        showmsg = (2,"Usuario registrado","El usuario a sido creado y registrado con exito ingrese sesion en la pagina principal")
                        parent.quit()
                        parent.destroy()
                    else:
                        showmsg = (0,"Error",res)
            except:
                showmsg = (1,"Error de email", number)
        except:
            error = str(user)
            showmsg = (1,"Error al registrar la cuenta", error)
        
    return showmsg