from clases import *
from smtplib import *
from decouple import config
import random

def register_user(name,password,rep,email):

    error = None

    try:
        number = send_email(email)
    except:
        error = "Error al envial el mail, verifique que el remitente o el destinatario"

    if password != rep or password == "":
        error = "Las contraseñas no coinciden o no ah ingresado la contraseña"

    if "@gmail.com" not in email or len(email) <= 10 or " " in email:
        error = "La estructura del email no es correcta"

    try:
        name = int(name)
        if name <= 0:
            error = "El usuario debe ser un numero entre 1 y 1.000.000, sin comas ni puntos"
    except:
        error = "El usuario debe ser un numero entre 1 y 1.000.000, sin comas ni puntos"
    
    if error is None:
        user = Usuario(name,password,email)
        return number,user
    else:
        return error  

def send_email(mail):

    autentificacion = random.randint(10000,999999)
    msg = f"Subject: Mensaje de autentificacion de mail\n\nIngrese el siguiente codigo para terminar de registrar su cuenta en el sistema\nEl codigo es : {autentificacion}"
    remitente = config("USER")
    contra = config("PASSWORD")

    server = SMTP("smtp.gmail.com" ,587)
    server.starttls()
    server.login(remitente ,contra)

    server.sendmail(remitente ,mail ,msg)

    server.quit()

    return autentificacion

def register_in_db(user):
    print(user)