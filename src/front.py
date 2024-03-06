from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from back import *

#   Main es la ventana principal que va a tener el programa mientras se ejecute
#   solo va a contener las esctructuras Login y MainMenu.

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

#   Login es una esctructura que se utiliza en la ventana principal Main y es la primera en aparecer
#   al ejecutar el programa, esta estrucutra nos permite iniciar sesion con los 3 tipos de cuenta
#   que hay en el programa Usuario,Administrador,Desarrollador, y verificando los datos ingresados con
#   los almacenados en la base de datos se acepta/denega el acceso al menu principal MainMenu.
#   Esta estructura tambien nos permite registrar una cuenta de usuario en la base de datos si es 
#   que no teniamos una antes de abrir el programa.

class Login(Frame):
    def __init__(self, main_window):

        #setup

        super().__init__(main_window)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #struct

        self.create_login(main_window)

    #   La funcion createlogin es la funcion que crea todos los widgets de la estructura Login
    
    def create_login(self, main_window):

        #var

        user_name = StringVar()
        user_password = StringVar()

        #create

        login_title = Label(self, anchor="center", font=("TkMenuFont",18), bg=main_window.prim_bg_label, fg=main_window.letter_color, text="Bienvenidos de nuevo a Volpe\nIngrese sesion o registrese")

        user_label = Label(self, anchor="w" ,width=18, font=("Calibri",14), bg=main_window.prim_bg_label, fg=main_window.letter_color, text="Ingrese su Usuario:")
        password_label = Label(self, anchor="w", width=18, font=("Calibri",14), bg=main_window.prim_bg_label, fg=main_window.letter_color, text="Ingrese su contraseña:")
        register_label = Label(self, anchor="center", font=("Calibri",11), bg=main_window.secc_bg_label, fg=main_window.url_letter_color, text="Si no tiene una cuenta registrada, Haga click aqui.")

        user_input = Entry(self, font=("Calibri",12) ,fg=main_window.letter_color ,textvariable=user_name)
        password_input = Entry(self, font=("Calibri",12) ,fg=main_window.letter_color ,textvariable=user_password)
        
        login_button = Button(self, width=8, height=1, font=("Calibri",11), bg=main_window.prim_bg_button, fg="white", text="Ingresar", command= lambda: self.login(main_window,user_name.get(),user_password.get()))
        exit_button = Button(self, width=6, height=1, font=("Calibri",11), bg=main_window.exit_bg_button, fg=main_window.letter_color, text="Salir", command= lambda: close(main_window))

        #configure

        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        #title

        login_title.grid(column=0, row=0, columnspan=4, sticky="we")

        #label

        user_label.grid(column=0, row=2, sticky="e", padx=30)
        password_label.grid(column=0, row=4, sticky="e", padx=30)
        register_label.grid(column=0, row=6, columnspan=4, sticky="s")
        register_label.bind("<Button-1>", lambda e: self.register())

        #entry

        user_input.grid(column=1, row=2, sticky="we")
        password_input.grid(column=1, row=4, sticky="we")

        #button

        login_button.grid(column=0, row=7, columnspan=3)
        exit_button.grid(column=2,row=7 ,padx=20 ,sticky="e")

    #
    #
    #

    def login(self, main_window, user_name, user_password):
        login_state,login_res = login_user(user_name,user_password)
        if login_state:
            messagebox.showinfo("Inicio de sesion","Inicio de sesion exitoso")
            main_window.status.destroy()
            main_window.status = MainMenu(main_window, login_res)
        else:
            messagebox.showwarning("Error al inciar sesion",login_res)
         
    #   La funcion register es la funcion que crea una nueva ventana de tipo Extra, la cual se le
    #   carga como ultimo parametro "r" el cual selecciona la estructura Register

    def register(self):
        Extra("Registro de cuenta",[450,600,700,50],True,"white","r")

#
#
#

class MainMenu(Frame):
    def __init__(self, main_window, user):

        #setup

        super().__init__(main_window)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.close_and_delogin(main_window,user.name))

        #var

        self.user = user

        #struct

        self.create_menu(main_window)
    
    #
    #
    #
    
    def create_menu(self,main_window):
        
        #create

        main_title = Label(self ,anchor="center" ,font=("TkMenuFont",18) ,fg=main_window.letter_color ,bg=main_window.prim_bg_label ,text=f"Bienvenido de nuevo {self.user.name}")

        first_lb = Label(self ,anchor="center" ,font=("Calibri",14) ,fg=main_window.letter_color ,bg=main_window.prim_bg_label, text="Realize un pedido", width=20)
        secc_lb = Label(self ,anchor="center" ,font=("Calibri",14) ,fg=main_window.letter_color ,bg=main_window.prim_bg_label, text="Ver mis pedidos", width=20)

        first_btt = Button(self ,width=9 ,height=1 ,font=("Calibri",12) ,fg=main_window.exit_bg_button ,bg=main_window.prim_bg_button ,text="Seleccionar", command= lambda: self.order(self.user))
        secc_btt = Button(self ,width=9 ,height=1 ,font=("Calibri",12) ,fg=main_window.exit_bg_button ,bg=main_window.prim_bg_button ,text="Seleccionar", command= lambda: self.show_orders(self.user))
        exit_btt = Button(self ,width=12 ,height=1 ,font=("Calibri",12) ,fg=main_window.letter_color ,bg=main_window.exit_bg_button, text="Cerrar Sesion", command= lambda: self.backward(main_window,self.user.name))
        
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
    
    #
    #
    #
    
    def order(self,user):
        Extra("Generador de pedidos",[500,600,700,50],True,"white","o",user)
    
    #
    #
    #
     
    def show_orders(self,user):
        Extra("Lista de pedidos", (800,600,350,100), True, "white", "s",user)
    
    #
    #
    #
    
    def backward(self,main_window,user_name):
        delogin_state,delogin_res = de_login(user_name)
        if delogin_state:
            messagebox.showinfo("Sesion cerrada",delogin_res)
            main_window.status.destroy()
            main_window.status = Login(main_window)
        else:
            messagebox.showerror("Error",delogin_res)
    
    #
    #
    #
            
    def close_and_delogin(self,main_window,user_name):
        de_login(user_name)
        close(main_window)

#   Extra es una ventana auxiliar que sirve para mostrar esctructuras temporales, estas 
#   estructuras no estan pensadas para permanecer mucho tiempo y se seleccionan con el 
#   parametro op.

class Extra(Toplevel):
    def __init__(self, tittle, size, resize, back_color, op, user_data=None):

        #setup

        super().__init__()
        setup(self, tittle, size, resize, back_color)

        self.lift() #Hace que la ventana este por encima de la ventana Main
        self.grab_set() #Hace que lo que este pasando en la pagina principal se congele

        #var

        self.letter_color = "black"
        self.url_letter_color = "lightblue"
        self.prim_bg_label = "red"
        self.secc_bg_label = "green"
        self.prim_bg_button = "blue"
        self.secc_bg_button = "yellow"
        self.exit_bg_button = "white"

        #status

        if op == "r":
            self.status = Register(self)
        elif op == "o":
            self.status = Order(self,user_data)
        elif op == "s":
            self.status = ShowOrder(self,user_data)

        #loop

        self.mainloop()

#   Register es una estrcutrua que se utiliza en una ventana auxiliar Extra, esta estructura nos permite
#   registrar correctamente una cuenta de usuario nueva con un nombre de usuario (que no debe estar vacio ni
#   poseer un numero) un gmail (que debe ser un email de google es decir terminar con @gmail.com) y una 
#   contraseña que no tiene muchas validaciones, al tener todos los datos correctos y poder efectuar otras 
#   validaciones extras (conexion con la base de datos, datos validos de la cuenta remitente de gmail) se 
#   envia un email a la direccion ingresada con un codigo numerico y se abre otra pestaña para ingresar dicho
#   codigo, si el usuario ingresa el codigo correcto se finaliza el proceso de registro, se añade la nueva 
#   cuenta de usuario a la base de datos y se cierran todas las ventanas emergentes volviendo a la ventana
#   principal.
 
class Register(Frame):
    def __init__(self,extra_window):

        #setup

        super().__init__(extra_window)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #var

        self.ok = False

        #struct

        self.create_account(extra_window)

    #   La funcion create_account crea todos los widgets de la estructura Register

    def create_account(self ,extra_window):

        #var
        
        user_name = StringVar()
        user_email = StringVar()
        user_pasword = StringVar()
        password_rep = StringVar()
        
        #create
        
        main_title = Label(self, anchor="center", font=("TkMenuFont",18), bg=extra_window.prim_bg_label, fg=extra_window.letter_color, text="Ingrese sus datos para\nRegistrar una cuenta")

        user_lb = Label(self, anchor="center", font=("Calibri",11), bg=extra_window.prim_bg_label, fg=extra_window.letter_color, text="Ingrese su nombre de usuario: ", width=18, wraplength=150)
        email_lb = Label(self, anchor="center", font=("Calibri",11), bg=extra_window.prim_bg_label, fg=extra_window.letter_color, text="Ingrese su correo electronico: ", width=18, wraplength=150)
        pass_lb = Label(self, anchor="center", font=("Calibri",11), bg=extra_window.prim_bg_label, fg=extra_window.letter_color, text="Ingrese su contraseña: ", width=18, wraplength=150)
        pass_rep_lb = Label(self, anchor="center", font=("Calibri",11), bg=extra_window.prim_bg_label, fg=extra_window.letter_color, text="Vuelva a ingresar su contraseña: ", width=18, wraplength=150)

        user_entry = Entry(self, font=("Calibri",9), fg=extra_window.letter_color, textvariable=user_name)
        email_entry = Entry(self, font=("Calibri",9), fg=extra_window.letter_color, textvariable=user_email)
        pass_entry = Entry(self, font=("Calibri",9), fg=extra_window.letter_color, textvariable=user_pasword, show="*")
        pass_rep_entry = Entry(self, font=("Calibri",9), fg=extra_window.letter_color, textvariable=password_rep, show="*")

        confirm_btt = Button(self, fg=extra_window.exit_bg_button, bg=extra_window.prim_bg_button, text="Registrarse", width=8, height=1, command= lambda: self.register_account(extra_window,user_name.get(),user_pasword.get(),password_rep.get(),user_email.get()))
        exit_btt = Button(self, fg=extra_window.letter_color, bg=extra_window.exit_bg_button, text="Volver", width=8, height=1, command= lambda: close(extra_window))

        #configure

        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1,2,3,4,5), weight=1)

        #title

        main_title.grid(column=0, row=0, sticky="we", columnspan=5)

        #label

        user_lb.grid(column=0, row=1, sticky="e", padx=20)
        email_lb.grid(column=0, row=2, sticky="e", padx=20)
        pass_lb.grid(column=0, row=3, sticky="e", padx=20)
        pass_rep_lb.grid(column=0, row=4, sticky="e", padx=20) 

        #entry

        user_entry.grid(column=1, row=1, sticky="we")
        email_entry.grid(column=1, row=2, sticky="we")
        pass_entry.grid(column=1, row=3, sticky="we")
        pass_rep_entry.grid(column=1, row=4, sticky="we")

        #button

        confirm_btt.grid(column=0, row=5, columnspan=2)
        exit_btt.grid(column=4, row=5)

    #   La funcion register_account muestra distintos tipos de ventanas emergentes (messagebox)
    #   las cuales muestran si hubo algun error de validacion de datos, problemas con el envio
    #   de emails, problemas con la conexion a la base de datos o problemas con el registro de
    #   nuevas cuentas a la base de datos, caso contrario si no hubo ninguna complicacion en 
    #   el registro, muestra una ventana informando el exito de la operacion y esto garantiza
    #   el definitivo registro en la base de datos.

    def register_account(self, extra_window, name, password, rep, email):

        msg = register_in_db(self, extra_window, name, password, rep, email)
        title = msg[1]
        body = msg[2]

        if msg[0] == 0:
            messagebox.showerror(title,body)
        elif msg[0] == 1:
            messagebox.showwarning(title,body)
        elif msg[0] == 2:
            messagebox.showinfo(title,body)

#
#
#

class Order(Frame):
    def __init__(self ,extra_window, user):

        #setup

        super().__init__(extra_window)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #var

        self.user = user

        #struct

        self.create_order(extra_window)

    #
    #
    #

    def create_order(self,extra_window):

        #create

        main_title = Label(self ,anchor="center" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("TkMenuFont",18) ,text="Realize su pedido")

        ropa_lb = Label(self, anchor="w" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione la ropa del pedido:")
        servicio_lb = Label(self, anchor="w" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione el servicio deseado:")
        prioridad_lb = Label(self, anchor="w" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Seleccione la prioridad que desee:")
        comentario_lb = Label(self, anchor="w" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("Calibri",12) ,width=24 ,wraplength=180 ,text="Añada un comentario si desea:")

        ropa_cb = ttk.Combobox(self)
        servicio_cb = ttk.Combobox(self)
        prioridad_cb = ttk.Combobox(self)

        comentario_input = Text(self,height=8, width=25)

        confirm_btt = Button(self, width=10 ,height=1 ,bg=extra_window.prim_bg_button ,fg=extra_window.exit_bg_button ,text="Hacer pedido" ,command= lambda: self.make_order(ropa_cb.get(),servicio_cb.get(),prioridad_cb.get(),comentario_input.get("1.0","end"),self.user))
        exit_btt = Button(self, width=8 ,height=1 ,bg=extra_window.exit_bg_button ,fg=extra_window.letter_color ,text="Volver" ,command= lambda: close(extra_window))

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

    #
    #
    #

    def make_order(self,ropa,servicio,prioridad,conentario,user):

        msg = create_order_db(ropa,servicio,prioridad,conentario,user)

        if msg[0] == 0:
            messagebox.showerror(msg[1],msg[2])
        elif msg[0] == 1:
            messagebox.showwarning(msg[1],msg[2])
        elif msg[0] == 2:
            messagebox.showinfo(msg[1],msg[2]) 

#
#
#

class ShowOrder(Frame):
    def __init__(self ,extra_window,user):

        #setup

        super().__init__(extra_window)
        self.configure(bg="black",padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")
    
        #var
        
        self.user = user

        #struct

        self.show_display(extra_window)

    #
    #
    #

    def show_display(self ,extra_window):

        #var

        tree_columns = ("num_pedido","ropa","servicio","prioridad","precio","estado")

        #create

        main_title = Label(self ,anchor="center" ,fg=extra_window.letter_color ,bg=extra_window.prim_bg_label ,font=("TkMenuFont",18) ,text="Sus pedidos")
   
        orders_tree = ttk.Treeview(self ,columns=tree_columns ,show="headings")
        orders_tree.heading("num_pedido", text="Nº Pedido")
        orders_tree.heading("ropa" ,text="Ropa")
        orders_tree.heading("servicio" ,text="Servicio")
        orders_tree.heading("prioridad" ,text="Prioridad")
        orders_tree.heading("precio" ,text="Precio")
        orders_tree.heading("estado" ,text="Estado")
        orders_tree.column("num_pedido", width=20, anchor="center")
        orders_tree.column("ropa" ,width=80)
        orders_tree.column("servicio" ,width=120)
        orders_tree.column("prioridad" ,width=80)
        orders_tree.column("precio" ,width=80)
        orders_tree.column("estado" ,width=120)
        self.update_tree(orders_tree)

        scroll = Scrollbar(self ,orient=VERTICAL ,command=orders_tree.yview)
        orders_tree.configure(yscroll=scroll.set)

        delete_btt = Button(self,height=1 ,width=8 ,fg=extra_window.letter_color ,bg=extra_window.secc_bg_button ,text="Cancelar" ,command=lambda: self.select_tree(orders_tree))
        exit_btt = Button(self ,height=1 ,width=8 ,fg=extra_window.letter_color ,bg=extra_window.exit_bg_button ,text="Volver" ,command=lambda: close(extra_window))

        #configure

        self.columnconfigure((0,1,2),weight=1)
        self.rowconfigure((0,1,2) ,weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,columnspan=3 ,sticky="we")

        #display

        orders_tree.grid(column=0 ,row=1 ,sticky="nswe", columnspan=3)

        #scroll

        scroll.grid(column=2 ,row=1 ,sticky="nse")

        #button

        exit_btt.grid(column=2 ,row=2, sticky="e")
        delete_btt.grid(column=0 ,row=2)
  
    #
    #
    #
  
    def select_tree(self,tree):
        select = tree.focus()

        if not select:
           messagebox.showwarning("No se pudo cancelar el pedido","Seleccione un pedido para cancelarlo")
        else:
            values = tree.item(select)["values"]
            delete_state,delete_result = delete_order(values[0])
            if not delete_state:
               messagebox.showerror("Error",delete_result)
            else:
                messagebox.showinfo("Accion exitosa",delete_result)
        
        self.update_tree(tree)
    
    #
    #
    #

    def update_tree(self,tree):
        tree.delete(*tree.get_children())
        orders_state, orders_result = get_user_orders(self.user)
        if orders_state:
            for item in orders_result:
                tree.insert("" ,END ,values=item)
        else:
            messagebox.showerror("Error",orders_result)


#   La funcion setup basicamente tiene una lista de lineas de codigo que inicializan ciertos parametros de
#   las ventanas como el titulo, el tamaño, el reescalado, el color, etc.

def setup(self, tittle, size, resize, back_color):
    self.title(tittle)
    self.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
    self.resizable(resize, resize)
    self.config(bg=back_color)
    self.protocol("WM_DELETE_WINDOW", lambda: close(self))

#   La funcion close se usa en todos los botones de salida y basicamente termina definitivamente
#   el funcionamiento de las ventanas Extra o MainMenu.

def close(object):
    object.quit()
    object.destroy()

#
# 
#

if __name__ == "__main__":
   Main("Volpe project", (800,600,300,50), True, "white")