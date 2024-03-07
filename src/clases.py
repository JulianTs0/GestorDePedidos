from database import *

#   Clase Usuario, usada para crear objetos tipo Usuario y tenes mas comodamente los 3 campos que contiene

class Usuario:
    def __init__(self, name, password, email):

        self.name = name
        self.password = password
        self.email = email

#
#
#

class Bien:
    def __init__(self,ident,precio):

        self.ident = ident
        self.precio = precio

#
#
#

class Pedido:
    def __init__(self, ropa, servicio, prioridad, comentario):
        
        self.ropa = ropa
        self.servicio = servicio
        self.prioridad = prioridad
        self.comentario = comentario
        self.precio = self.calc_precio()

    def calc_precio(self):
        final = 0
        Ropas = self.get_field_stock("ropas")
        Servicios = self.get_field_stock("servicios")
        Prioridades = self.get_field_stock("prioridades")

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

    def get_field_stock(self,field):
        bienes = []
        field_stock = get_service_stock_data(field)
        if field_stock == "Error al mostrar el stock":
            return ""
        else:
            for stock in field_stock:
                bienes.append(Bien(stock[0],stock[1]))
            return bienes