
#   Clase Usuario, usada para crear objetos tipo Usuario y tenes mas comodamente los 3 campos que contiene

class Usuario:
    def __init__(self, name, password, email):

        self.name = name
        self.password = password
        self.email = email

    def __str__(self):
        return(f"Usuario: {self.name} Contraseña: {self.password} Email: {self.email}")
    
class Bien:
    def __init__(self,ident,precio):

        self.ident = ident
        self.precio = precio

class Pedido:
    def __init__(self, ropa, servicio, prioridad, comentario):
        
        self.ropa = ropa
        self.servicio = servicio
        self.prioridad = prioridad
        self.comentario = comentario
        self.precio = self.calc_precio()

    def calc_precio(self):
        final = 0
        Ropas = (Bien("Ropa 1",100),Bien("Ropa 2",200),Bien("Ropa 3",300),Bien("Ropa 4",400))
        Servicios = (Bien("Servicio 1",50),Bien("Servicio 2",100),Bien("Servicio 3",150),Bien("Servicio 4",200))
        Prioridades = (Bien("Alta",500),Bien("Media",300),Bien("Baja",100))

        for ropa in Ropas:
            if ropa.ident == self.ropa:
                final += ropa.precio
                break
        
        for servicio in Servicios:
            if servicio.ident == self.servicio:
                final += servicio.precio
                break
        
        for prioridad in Prioridades:
            if prioridad.ident == self.prioridad:
                final += prioridad.precio
                break
        
        return final
    
    def __str__(self):
        if self.comentario == "":
            return(f"Ropa: {self.ropa} Servicio: {self.servicio} Prioridad: {self.prioridad} Precio: {self.precio} ")
        else:
            return(f"Ropa: {self.ropa} Servicio: {self.servicio} Prioridad: {self.prioridad} Comentario: {self.comentario} Precio: {self.precio} ")