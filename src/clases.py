class Usuario:
    def __init__(self ,name ,password ,email):

        self.name = name
        self.password = password
        self.email = email

    def __str__(self):
        return(f"Usuario: {self.name} Contraseña: {self.password} Email: {self.email}")