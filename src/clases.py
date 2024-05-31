from database import *



#Aprovechar mas el uso de las clases
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
        Ropas = get_service_stock_data("ropas")
        Servicios = get_service_stock_data("servicios")
        Prioridades = get_service_stock_data("prioridades")

        if isinstance(Ropas,str) or isinstance(Servicios,str) or isinstance(Prioridades,str):
            return 0
        else:
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