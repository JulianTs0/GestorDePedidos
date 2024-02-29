from clases import *
from smtplib import *
from database import *
from decouple import config
import random

def register_user(name,password,rep,email):

    error = None

    if password != rep or password == "":
        error = "Las contraseñas no coinciden o no ah ingresado la contraseña"

    if "@gmail.com" not in email or len(email) <= 10 or " " in email:
        error = "La estructura del email no es correcta"

    if len(name) <= 0:
        error = "Ingrese un nombre de usuario"
    
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
    if conectBD() == "Error al conectarse a la base de datos":
        return conectBD()
    else:
        return None

def register_in_db(user):
    res = ingresarUsuarios(user)
    return res