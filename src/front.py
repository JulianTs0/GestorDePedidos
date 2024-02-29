from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from back import *

class Main(Tk):
    def __init__(self, tittle, size, resize, back_color):

        #setup

        super().__init__()
        setup(self, tittle, size, resize, back_color)

        #var

        self.letter_color = "black"
        self.url_letter_color = "lightblue"
        self.prim_bg_label = "red"
        self.secc_bg_label = "green"
        self.prim_bg_button = "blue"
        self.secc_bg_button = "yellow"
        self.exit_bg_button = "white"

        #status

        self.status = Login(self)

        #loop

        self.mainloop()

class Extra(Toplevel):
    def __init__(self, tittle, size, resize, back_color, op):

        #setup

        super().__init__()
        setup(self, tittle, size, resize, back_color)
        self.lift()
        self.grab_set() #Hace que lo que este pasando en la pagina principal se congele

        #var

        self.letter_color = "black"
        self.url_letter_color = "lightblue"
        self.prim_bg_label = "red"
        self.secc_bg_label = "green"
        self.prim_bg_button = "blue"
        self.secc_bg_button = "yellow"
        self.exit_bg_button = "white"

        #window

        if op == "r":
            self.status = Register(self)
        elif op == "o":
            self.status = Order(self)
        elif op == "s":
            self.status = ShowOrder(self)

        #loop

        self.mainloop()

class Login(Frame):
    def __init__(self, parent):

        #setup

        super().__init__(parent)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #struct

        self.createlogin(parent)
    
    def createlogin(self, parent):

        #var

        user = StringVar()
        lvl = StringVar()
        password = StringVar()

        #create

        login_title = Label(self, anchor="center",font=("TkMenuFont",18) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Bienvenidos de nuevo a Volpe\nIngrese sesion o registrese")

        user_label = Label(self, anchor="w" ,width=18 ,font=("Calibri",14) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese su Usuario:")
        lvl_label = Label(self, anchor="w" ,width=18 ,font=("Calibri",14) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Seleccione su Nivel:")
        password_label = Label(self, anchor="w" ,width=18 ,font=("Calibri",14) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese su contraseña:")
        register_label = Label(self, anchor="center" ,font=("Calibri",11) ,bg=parent.secc_bg_label ,fg=parent.url_letter_color ,text="Si no tiene una cuenta registrada, Haga click aqui.")

        user_input = Entry(self ,font=("Calibri",12) ,fg=parent.letter_color ,textvariable=user)
        password_input = Entry(self ,font=("Calibri",12) ,fg=parent.letter_color ,textvariable=password)

        lvl_cb = ttk.Combobox(self ,textvariable=lvl)
        
        login_button = Button(self ,width=8 ,height=1 ,font=("Calibri",11) ,bg=parent.prim_bg_button ,fg="white" ,text="Ingresar" ,command= lambda: self.login(parent,("user","pasword","lvl")))
        exit_button = Button(self ,width=6 ,height=1 ,font=("Calibri",11) ,bg=parent.exit_bg_button ,fg=parent.letter_color ,text="Salir", command= lambda: close(parent))

        #configure

        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        #title

        login_title.grid(column=0 ,row=0 ,columnspan=4, sticky="we")

        #label

        user_label.grid(column=0 ,row=2, sticky="e", padx=30)
        lvl_label.grid(column=0 ,row=3, sticky="e", padx=30)
        password_label.grid(column=0 ,row=4, sticky="e", padx=30)
        register_label.grid(column=0 ,row=6, columnspan=4, sticky="s")
        register_label.bind("<Button-1>", lambda e: self.register())

        #entry

        user_input.grid(column=1 ,row=2, sticky="we")
        password_input.grid(column=1 ,row=4, sticky="we")

        #combobox

        lvl_cb.grid(column=1 ,row=3 ,sticky="we")
        lvl_cb['values'] = ("Desarollador","Administrador","Usuario")
        lvl_cb['state'] = "readonly"

        #button

        login_button.grid(column=0 ,row=7 ,columnspan=3)
        exit_button.grid(column=2 ,row=7 ,padx=20 ,sticky="e")
    
    def login(self, parent, data):
        parent.status.destroy()
        parent.status = MainMenu(parent,data)
        
    def register(self):
        Extra("Registro de cuenta",[450,600,700,50],True,"white","r")

class Register(Frame):
    def __init__(self,parent):

        #setup

        super().__init__(parent)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #var

        self.ok = False

        #struct

        self.create_account(parent)

    def create_account(self ,parent):

        #var
        
        user = StringVar()
        email = StringVar()
        pasword = StringVar()
        rep = StringVar()
        
        #create
        
        main_title = Label(self ,anchor="center" ,font=("TkMenuFont",18) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese sus datos para\nRegistrar una cuenta")

        user_lb = Label(self, anchor="center" ,font=("Calibri",11) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese su nombre de usuario: " ,width=18 ,wraplength=150)
        email_lb = Label(self, anchor="center" ,font=("Calibri",11) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese su correo electronico: " ,width=18 ,wraplength=150)
        pass_lb = Label(self, anchor="center" ,font=("Calibri",11) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Ingrese su contraseña: " ,width=18 ,wraplength=150)
        pass_rep_lb = Label(self, anchor="center" ,font=("Calibri",11) ,bg=parent.prim_bg_label ,fg=parent.letter_color ,text="Vuelva a ingresar su contraseña: " ,width=18 ,wraplength=150)

        user_entry = Entry(self ,font=("Calibri",9) ,fg=parent.letter_color ,textvariable=user)
        email_entry = Entry(self ,font=("Calibri",9) ,fg=parent.letter_color ,textvariable=email)
        pass_entry = Entry(self ,font=("Calibri",9) ,fg=parent.letter_color ,textvariable=pasword ,show="*")
        pass_rep_entry = Entry(self ,font=("Calibri",9) ,fg=parent.letter_color ,textvariable=rep ,show="*")

        confirm_btt = Button(self ,fg=parent.exit_bg_button ,bg=parent.prim_bg_button ,text="Registrarse" ,width=8 ,height=1 ,command= lambda: self.register_account(parent,user.get(),pasword.get(),rep.get(),email.get()))
        exit_btt = Button(self ,fg=parent.letter_color ,bg=parent.exit_bg_button ,text="Volver" ,width=8 ,height=1 ,command= lambda: close(parent))

        #configure

        self.columnconfigure((0,1,2,3,4) ,weight=1)
        self.rowconfigure((0,1,2,3,4,5) ,weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,sticky="we" ,columnspan=5)

        #label

        user_lb.grid(column=0 ,row=1 ,sticky="e" ,padx=20)
        email_lb.grid(column=0 ,row=2 ,sticky="e", padx=20)
        pass_lb.grid(column=0 ,row=3 ,sticky="e", padx=20)
        pass_rep_lb.grid(column=0 ,row=4 ,sticky="e", padx=20) 

        #entry

        user_entry.grid(column=1 ,row=1 ,sticky="we")
        email_entry.grid(column=1 ,row=2 ,sticky="we")
        pass_entry.grid(column=1 ,row=3 ,sticky="we")
        pass_rep_entry.grid(column=1 ,row=4 ,sticky="we")

        #button

        confirm_btt.grid(column=0 ,row=5, columnspan=2)
        exit_btt.grid(column=4 ,row=5)

    def register_account(self ,parent ,name ,password ,rep ,email):

        msg = register_in_db(self, parent ,name ,password ,rep ,email)
        title = msg[1]
        body = msg[2]

        if msg[0] == 0:
            messagebox.showerror(title,body)
        elif msg[0] == 1:
            messagebox.showwarning(title,body)
        elif msg[0] == 2:
            messagebox.showinfo(title,body)
            
class MainMenu(Frame):
    def __init__(self, parent, data):

        #setup

        super().__init__(parent)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #var

        self.data = data

        #struct

        if self.data[2] == "desarollador":
            pass
        elif self.data[2] == "administrador":
            pass
        elif self.data[2] == "usuario":
            pass

        self.createmenu(parent)
    
    def createmenu(self,parent):
        
        #create

        main_title = Label(self ,anchor="center" ,font=("TkMenuFont",18) ,fg=parent.letter_color ,bg=parent.prim_bg_label ,text="Bienvenido usuario")

        first_lb = Label(self ,anchor="center" ,font=("Calibri",14) ,fg=parent.letter_color ,bg=parent.prim_bg_label, text="Realize un pedido", width=20)
        secc_lb = Label(self ,anchor="center" ,font=("Calibri",14) ,fg=parent.letter_color ,bg=parent.prim_bg_label, text="Ver mis pedidos", width=20)

        first_btt = Button(self ,width=9 ,height=1 ,font=("Calibri",12) ,fg=parent.exit_bg_button ,bg=parent.prim_bg_button ,text="Seleccionar", command= lambda: self.order())
        secc_btt = Button(self ,width=9 ,height=1 ,font=("Calibri",12) ,fg=parent.exit_bg_button ,bg=parent.prim_bg_button ,text="Seleccionar", command= lambda: self.show_orders())
        exit_btt = Button(self ,width=12 ,height=1 ,font=("Calibri",12) ,fg=parent.letter_color ,bg=parent.exit_bg_button, text="Cerrar Sesion", command= lambda: self.backward(parent))
        
        #configure

        self.columnconfigure((0,1,2) ,weight=1)
        self.rowconfigure((0,1,2,3,4,5) ,weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,columnspan=3 ,sticky="we")

        #label

        first_lb.grid(column=0 ,row=1 ,columnspan=3)
        secc_lb.grid(column=0 ,row=3 ,columnspan=3)

        #button

        first_btt.grid(column=0 ,row=2 ,columnspan=3)
        secc_btt.grid(column=0 ,row=4 ,columnspan=3)
        exit_btt.grid(column=2 ,row=5 ,sticky="e" ,padx=25)

    def order(self):
        Extra("Generador de pedidos",[500,600,700,50],True,"white","o")
    
    def show_orders(self):
        Extra("Lista de pedidos", (800,600,350,100), True, "white", "s")

    def backward(self,parent):
        parent.status.destroy()
        parent.status = Login(parent)

class Order(Frame):
    def __init__(self ,parent):

        #setup

        super().__init__(parent)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #struct

        self.createorder(parent)

    def createorder(self,parent):

        #var

        ropa = StringVar()
        servicio = StringVar()
        prioridad = StringVar()
        comentario = ""

        #create

        main_title = Label(self ,anchor="center" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("TkMenuFont",18) ,text="Realize su pedido")

        ropa_lb = Label(self, anchor="w" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione la ropa del pedido:")
        servicio_lb = Label(self, anchor="w" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione el servicio deseado:")
        prioridad_lb = Label(self, anchor="w" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione la prioridad que desee:")
        comentario_lb = Label(self, anchor="w" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Añada un comentario si desea:")

        ropa_cb = ttk.Combobox(self, textvariable=ropa)
        servicio_cb = ttk.Combobox(self, textvariable=servicio)
        prioridad_cb = ttk.Combobox(self, textvariable=prioridad)

        comentario_input = Text(self,height=8, width=25)

        confirm_btt = Button(self, width=10 ,height=1 ,bg=parent.prim_bg_button ,fg=parent.exit_bg_button ,text="Hacer pedido" ,command= lambda: self.makeOrder())
        exit_btt = Button(self, width=8 ,height=1 ,bg=parent.exit_bg_button ,fg=parent.letter_color ,text="Volver" ,command= lambda: close(parent))

        #configure 

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2,3,4,5), weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,columnspan=3, sticky="we")

        #label

        ropa_lb.grid(column=0 ,row=1, sticky="w")
        servicio_lb.grid(column=0, row=2, sticky="w")
        prioridad_lb.grid(column=0, row=3, sticky="w")
        comentario_lb.grid(column=0, row=4, sticky="w")

        #combobox

        ropa_cb.grid(column=1, row=1, sticky="w" ,padx=20)
        ropa_cb["values"] = ("Ropa 1","Ropa 2","Ropa 3","Ropa 4")
        ropa_cb["state"] = "readonly"
        servicio_cb.grid(column=1, row=2, sticky="w" ,padx=20)
        servicio_cb["values"] = ("Servicio 1","Servicio 2","Servicio 3","Servicio 4")
        servicio_cb["state"] = "readonly"
        prioridad_cb.grid(column=1, row=3, sticky="w" ,padx=20)
        prioridad_cb["values"] = ("Alta","Media","Baja")
        prioridad_cb["state"] = "readonly"

        #entry

        comentario_input.grid(column=1, row=4, sticky="w" ,padx=20)

        #button

        confirm_btt.grid(column=0 ,row=5, columnspan=2)
        exit_btt.grid(column=2, row=5)   

    def makeOrder(self):
        print("mo")

class ShowOrder(Frame):
    def __init__(self ,parent):

        #setup

        super().__init__(parent)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")
    
        #struct

        self.showdisplay(parent)

    def showdisplay(self ,parent):

        #var

        columnas = ("ropa","servicio","prioridad")
        pedidos = self.getorder()

        #create

        main_title = Label(self ,anchor="center" ,fg=parent.letter_color ,bg=parent.prim_bg_label ,font=("TkMenuFont",18) ,text="Sus pedidos")
   
        pedidios_tree = ttk.Treeview(self ,columns=columnas ,show="headings")
        pedidios_tree.heading("ropa" ,text="Ropa")
        pedidios_tree.heading("servicio" ,text="Servicio")
        pedidios_tree.heading("prioridad" ,text="Prioridad")
        for item in pedidos:
            pedidios_tree.insert("" ,END ,values=item)

        scroll = Scrollbar(self ,orient=VERTICAL ,command=pedidios_tree.yview)
        pedidios_tree.configure(yscroll=scroll.set)

        exit_btt = Button(self ,height=1 ,width=8 ,fg=parent.letter_color ,bg=parent.exit_bg_button ,text="Volver" ,command=lambda: close(parent))

        #configure

        self.columnconfigure((0,1,2),weight=1)
        self.rowconfigure((0,1,2) ,weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,columnspan=3 ,sticky="we")

        #display

        pedidios_tree.grid(column=1 ,row=1 ,sticky="nswe")

        #scroll

        scroll.grid(column=2 ,row=1 ,sticky="nsw")

        #button

        exit_btt.grid(column=2 ,row=2 )
 
    def getorder(self):
        pedidos = []
        for n in range(16):
            pedidos.append((f"Ropa {n}", f"Servicio {n}", f"Prioridad {n}"))
        return pedidos

def setup(self, tittle, size, resize, back_color):
    self.title(tittle)
    self.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
    self.resizable(resize, resize)
    self.config(bg=back_color)

def close(object):
    object.quit()
    object.destroy()
    
if __name__ == "__main__":
   Main("Volpe project", (800,600,300,50), True, "white")