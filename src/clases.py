from database import *



class Usuario:
    def __init__(self, name, password, email):

        self.name = name
        self.password = password
        self.email = email



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
            if ropa[0] == self.ropa:
                final += ropa[1]
                break
        
        for servicio in Servicios:
            if servicio[0] == self.servicio:
                final += servicio[1]
                break
        
        for prioridad in Prioridades:
            if prioridad[0] == self.prioridad:
                final += prioridad[1]
                break
        
        return final

    def get_field_stock(self,field):
        field_stock = get_service_stock_data(field)
        if field_stock == "Error al mostrar el stock":
            return ""
        else:
            return field_stock