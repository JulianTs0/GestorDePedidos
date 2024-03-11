from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from back_admin import *

#   Main es la ventana principal que va a tener el programa mientras se ejecute
#   solo va a contener las esctructuras Login y MainMenu.

class Main(Tk):
    def __init__(self, tittle, size, resize, back_color):

        #setup

        super().__init__()
        setup(self, tittle, size, resize, back_color)

        #var

        self.extra_bg = "#D7D6D2"
        self.secc_bg = "#000000"
        self.letter_color = "#DAFAD2"
        self.secc_letter_color = "#0928B4"
        self.url_letter_color = "#31F8EF"
        self.prim_bg_label = "#141416"
        self.secc_bg_label = "#890a36"
        self.prim_bg_button = "#AB0D43"
        self.secc_bg_button = "#1b1c36"
        self.exit_bg_button = "#712664"
        self.prim_hl_button = "#670828"
        self.secc_hl_button = "#101120"
        self.exit_hl_button = "#44173c"

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
        self.configure(bg=main_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #struct

        self.create_login(main_window)

    #   La funcion createlogin es la funcion que crea todos los widgets de la estructura Login
    
    def create_login(self, main_window):

        #var

        admin_name = StringVar()
        admin_password = StringVar()

        #create

        input_font = font.Font(weight="bold",size=9)

        login_title = Label(self, 
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=main_window.prim_bg_label, 
                            fg=main_window.letter_color, 
                            text="Panel de administracion de Volpe\nIngrese sesion con su cuenta de administrador"
                            )

        admin_label = Label(self, 
                           anchor="w",
                           width=18,
                           font=("Calibri",14), 
                           bg=main_window.prim_bg_label, 
                           fg=main_window.letter_color, 
                           text="Ingrese su Usuario:"
                           )
        password_label = Label(self, 
                               anchor="w", 
                               width=18, 
                               font=("Calibri",14), 
                               bg=main_window.prim_bg_label, 
                               fg=main_window.letter_color, 
                               text="Ingrese su contraseña:"
                               )

        user_input = Entry(self, 
                           font=input_font,
                           fg=main_window.prim_bg_label,
                           textvariable=admin_name
                           )
        password_input = Entry(self, font=input_font,
                               fg=main_window.prim_bg_label,
                               textvariable=admin_password,
                               show="*"
                               )
        
        login_button = Button(self, 
                              width=8, 
                              height=1, 
                              font=("Calibri",11), 
                              bg=main_window.prim_bg_button, 
                              fg=main_window.letter_color, 
                              activeforeground=main_window.letter_color, 
                              activebackground=main_window.prim_hl_button, 
                              relief="flat", 
                              text="Ingresar", 
                              command= lambda: self.login(main_window,admin_name.get(),admin_password.get())
                              )
        exit_button = Button(self, 
                             width=6, 
                             height=1, 
                             font=("Calibri",11), 
                             bg=main_window.exit_bg_button, 
                             fg=main_window.letter_color, 
                             activeforeground=main_window.letter_color, 
                             activebackground=main_window.exit_hl_button, 
                             relief="flat", 
                             text="Salir", 
                             command= lambda: close(main_window)
                             )

        #configure

        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        #title

        login_title.grid(column=0, row=0, columnspan=4, sticky="we")

        #label

        admin_label.grid(column=0, row=2, sticky="e", padx=30)
        password_label.grid(column=0, row=3, sticky="e", padx=30)

        #entry

        user_input.grid(column=1, row=2, sticky="we")
        password_input.grid(column=1, row=3, sticky="we")

        #button

        login_button.grid(column=0, row=5, columnspan=3)
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

#
#
#

class MainMenu(Frame):
    def __init__(self, main_window, user):

        #setup

        super().__init__(main_window)
        self.configure(bg=main_window.secc_bg,padx=10, pady=10)
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

        main_title = Label(self,
                           anchor="center",
                           font=("TkMenuFont",18),
                           fg=main_window.letter_color,
                           bg=main_window.prim_bg_label,
                           text=f"Bienvenido de nuevo {self.user.name}"
                           )
        first_label = Label(self, 
                           anchor="center",
                           width=20,
                           font=("Calibri",14), 
                           bg=main_window.prim_bg_label, 
                           fg=main_window.letter_color, 
                           text="Añadir administradores"
                           )
        secc_label = Label(self, 
                           anchor="center",
                           width=23,
                           font=("Calibri",14), 
                           bg=main_window.prim_bg_label, 
                           fg=main_window.letter_color, 
                           text="Modificar base de precios"
                           )
        thirt_label = Label(self, 
                           anchor="center",
                           width=18,
                           font=("Calibri",14), 
                           bg=main_window.prim_bg_label, 
                           fg=main_window.letter_color, 
                           text="Modificar usuarios"
                           )
        four_label = Label(self, 
                           anchor="center",
                           width=18,
                           font=("Calibri",14), 
                           bg=main_window.prim_bg_label, 
                           fg=main_window.letter_color, 
                           text="Modificar pedidos"
                           )

        first_btt = Button(self,
                          width=10,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.prim_bg_button,
                          activeforeground=main_window.letter_color,
                          activebackground=main_window.prim_hl_button, 
                          relief="flat" ,text="Seleccionar", 
                          command= lambda: self.register_account(main_window.extra_bg)
                          )
        secc_btt = Button(self,
                          width=10,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.prim_bg_button,
                          activeforeground=main_window.letter_color,
                          activebackground=main_window.prim_hl_button, 
                          relief="flat" ,text="Seleccionar", 
                          command= lambda: self.price_data(main_window.extra_bg)
                          )
        thirt_btt = Button(self,
                          width=10,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.prim_bg_button,
                          activeforeground=main_window.letter_color,
                          activebackground=main_window.prim_hl_button, 
                          relief="flat" ,text="Seleccionar", 
                          command= lambda: self.modify_users(main_window.extra_bg)
                          )
        four_btt = Button(self,
                          width=10,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.prim_bg_button,
                          activeforeground=main_window.letter_color,
                          activebackground=main_window.prim_hl_button, 
                          relief="flat" ,text="Seleccionar", 
                          command= lambda: self.modify_orders(main_window.extra_bg)
                          )
        exit_btt = Button(self,
                          width=12,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.exit_bg_button,
                          activeforeground=main_window.letter_color,
                          activebackground=main_window.exit_hl_button, 
                          relief="flat" ,text="Cerrar Sesion", 
                          command= lambda: self.backward(main_window,self.user.name)
                          )
        
        #configure

        self.columnconfigure((0,1,2,3) ,weight=1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8) ,weight=1)

        #title

        main_title.grid(column=0 ,row=0 ,columnspan=4 ,sticky="we")

        #label

        first_label.grid(column=1,row=2)
        secc_label.grid(column=2,row=2)
        thirt_label.grid(column=1,row=5)
        four_label.grid(column=2,row=5)

        #button

        first_btt.grid(column=1,row=3)
        secc_btt.grid(column=2,row=3)
        thirt_btt.grid(column=1,row=6)
        four_btt.grid(column=2,row=6)
        exit_btt.grid(column=0 ,row=8 ,columnspan=4,sticky="e" ,padx=25)
    
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
    
    def register_account(self,back_color):
        Extra("Registro de cuenta",[650,600,400,50],True,back_color,"r")
    
    #
    #
    #
    
    def price_data(self,back_color):
        Extra("Base de precios",[700,600,400,50],True,back_color,"p")
    
    #
    #
    #
    
    def modify_users(self,back_color):
        Extra("Base de usuarios",[600,600,400,50],True,back_color,"u")
    
    #
    #
    #
    
    def modify_orders(self,back_color):
        Extra("Base de pedidos",[1000,600,200,50],True,back_color,"o")
    
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

        self.secc_bg = "#000000"
        self.letter_color = "#DAFAD2"
        self.secc_letter_color = "#0928B4"
        self.url_letter_color = "#31F8EF"
        self.prim_bg_label = "#141416"
        self.secc_bg_label = "#890a36"
        self.prim_bg_button = "#AB0D43"
        self.secc_bg_button = "#1b1c36"
        self.exit_bg_button = "#712664"
        self.prim_hl_button = "#670828"
        self.secc_hl_button = "#101120"
        self.exit_hl_button = "#44173c"

        #status

        if op == "r":
            self.status = Register(self)
        elif op == "p":
            self.status = Price(self)
        elif op == "u":
            self.status = Users(self)
        elif op == "o":
            self.status = Orders(self)

        #loop

        self.mainloop()

#
#
#

class Register(Frame):
    def __init__(self,extra_window):

        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #struct

        self.create_register(extra_window)
    
    def create_register(self,extra_window):

        #var

        admin_name = StringVar()
        admin_pass = StringVar()
        admin_rep = StringVar()
        tree_columns = ("nombre","contra")
        
        #create

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=extra_window.prim_bg_label,
                        fieldbackground=extra_window.prim_bg_label,
                        foreground=extra_window.letter_color
                        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview",background=[("selected",extra_window.secc_bg)])
        
        style.configure("Treeview.Heading",
                        background=extra_window.prim_bg_button,
                        foreground=extra_window.letter_color,
                        relief="flat")
        style.map("Treeview.Heading",background=[("active","#44051b")])

        admins_tree = ttk.Treeview(self,columns=tree_columns,show="headings")
        admins_tree.column("nombre" ,width=80)
        admins_tree.column("contra" ,width=80)

        admins_tree.heading("nombre",text="Nombre")
        admins_tree.heading("contra",text="Contraseña")

        scroll = Scrollbar(self ,orient=VERTICAL ,command=admins_tree.yview)
        admins_tree.configure(yscroll=scroll.set)

        main_title = Label(self,
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Crear cuenta de administrador")

        user_label = Label(self, 
                            anchor="center", 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Ingrese un nombre de usuario: ", 
                            width=20, 
                            wraplength=150)
        password_label = Label(self,
                                anchor="center", 
                                font=("Calibri",11), 
                                bg=extra_window.prim_bg_label, 
                                fg=extra_window.letter_color, 
                                text="Ingrese una contraseña: ", 
                                width=20, 
                                wraplength=150)
        rep_label = Label(self,
                            anchor="center", 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Vuelva a ingresar su contraseña: ", 
                            width=20, 
                            wraplength=150)

        user_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=admin_name)
        password_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=admin_pass)
        rep_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=admin_rep)

        confirm_btt = Button(self,
                            fg=extra_window.letter_color, 
                            bg=extra_window.prim_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.prim_hl_button, 
                            relief="flat", 
                            text="Registrarse", 
                            width=8, 
                            height=1, 
                            command= lambda: self.register_admin()
                            )
        edit_btt = Button(self,
                            fg=extra_window.letter_color, 
                            bg=extra_window.secc_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.secc_hl_button, 
                            relief="flat", 
                            text="Modificar", 
                            width=8, 
                            height=1, 
                            command= lambda: self.edit_admin()
                            )
        exit_btt = Button(self,
                            fg=extra_window.letter_color, 
                            bg=extra_window.exit_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.exit_hl_button, 
                            relief="flat", 
                            text="Volver", 
                            width=8, 
                            height=1, 
                            command= lambda: close(extra_window)
                            )

        #configure

        self.columnconfigure((0,1,2,3,4),weight=1)
        self.rowconfigure((0,1,2,3,4,5),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=5,sticky="we")

        #label

        user_label.grid(column=2,row=1)
        password_label.grid(column=2,row=2)
        rep_label.grid(column=2,row=3)

        #entry

        user_entry.grid(column=3,row=1,columnspan=2)
        password_entry.grid(column=3,row=2,columnspan=2)
        rep_entry.grid(column=3,row=3,columnspan=2)

        #button

        confirm_btt.grid(column=2,row=5,sticky="e",padx=10)
        edit_btt.grid(column=3,row=5,sticky="w",padx=10)
        exit_btt.grid(column=4,row=5)

        #tree

        admins_tree.grid(column=0,row=1,columnspan=2,rowspan=3,sticky="nswe")

        #scroll

        scroll.grid(column=0,row=1,columnspan=2,rowspan=3,sticky="nse")

    def register_admin(self):
        pass

    def edit_admin(self):
        pass

#
#
#

class Price(Frame):
    def __init__(self,extra_window):
        
        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #struct

        self.create_price(extra_window)
    
    def create_price(self,extra_window):

        #var

        param_var = StringVar()
        price_var = StringVar()
        tree_columns = ("nombre","precio")

        #create

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=extra_window.prim_bg_label,
                        fieldbackground=extra_window.prim_bg_label,
                        foreground=extra_window.letter_color
                        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview",background=[("selected",extra_window.secc_bg)])
        
        style.configure("Treeview.Heading",
                        background=extra_window.prim_bg_button,
                        foreground=extra_window.letter_color,
                        relief="flat")
        style.map("Treeview.Heading",background=[("active","#44051b")])

        price_tree = ttk.Treeview(self,columns=tree_columns,show="headings")
        price_tree.column("nombre",width=80)
        price_tree.column("precio",width=80)

        price_tree.heading("nombre",text="Nombre")
        price_tree.heading("precio",text="Precio")

        scroll = Scrollbar(self ,orient=VERTICAL ,command=price_tree.yview)
        price_tree.configure(yscroll=scroll.set)

        main_title = Label(self, 
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Base de precios")

        param_label = Label(self, 
                            anchor="w",
                            width=18,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Nombre del parametro:")
        price_label = Label(self, 
                            anchor="w",
                            width=18,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Precio del parametro:")
        cb_label = Label(self, 
                            anchor="w",
                            width=18,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Eliga un parametro:")

        param_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=param_var)
        price_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=price_var)

        data_cb = ttk.Combobox(self)

        edit_btt = Button(self, 
                            width=6, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.prim_hl_button, 
                            relief="flat", 
                            text="Editar", 
                            command= lambda: self.edit_price())
        exit_btt = Button(self, 
                            width=6, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.exit_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.exit_hl_button, 
                            relief="flat", 
                            text="Volver", 
                            command= lambda: close(extra_window))

        #configure

        self.columnconfigure((0,1,2,3,4),weight=1)
        self.rowconfigure((0,1,2,3,4,5),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=5,sticky="we")

        #label

        param_label.grid(column=4,row=2,sticky="n")
        price_label.grid(column=4,row=3,sticky="n")
        cb_label.grid(column=0,row=1)

        #entry

        param_entry.grid(column=4,row=2)
        price_entry.grid(column=4,row=3)

        #combobox

        data_cb.grid(column=1,row=1)
        data_cb["values"] = ("Ropas","Servicios","Prioridades")
        data_cb["state"] = "readonly"

        #treeview

        price_tree.grid(column=0,row=2,columnspan=4,rowspan=3,sticky="nswe",padx=10)

        #scroll

        scroll.grid(column=0,row=2,columnspan=4,rowspan=3,sticky="nse")

        #button

        edit_btt.grid(column=4,row=4)
        exit_btt.grid(column=4,row=5,sticky="e")
    
    def edit_price(self):
        pass

#
#
#

class Users(Frame):
    def __init__(self,extra_window):
        
        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #struct

        self.create_user(extra_window)
    
    def create_user(self,extra_window):

        #var

        name_user = StringVar()
        email_user = StringVar()
        user_columns = ("nombre","email")

        #create

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=extra_window.prim_bg_label,
                        fieldbackground=extra_window.prim_bg_label,
                        foreground=extra_window.letter_color
                        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview",background=[("selected",extra_window.secc_bg)])
        
        style.configure("Treeview.Heading",
                        background=extra_window.prim_bg_button,
                        foreground=extra_window.letter_color,
                        relief="flat")
        style.map("Treeview.Heading",background=[("active","#44051b")])

        users_tree = ttk.Treeview(self,columns=user_columns,show="headings")
        users_tree.column("nombre",width=60)
        users_tree.column("email",width=140)

        users_tree.heading("nombre",text="Nombre")
        users_tree.heading("email",text="Email")

        scroll = Scrollbar(self ,orient=VERTICAL ,command=users_tree.yview)
        users_tree.configure(yscroll=scroll.set)

        main_title = Label(self, 
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Base de usuarios")

        name_label = Label(self, 
                            anchor="w",
                            width=16,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Nombre del usuario:")
        email_label = Label(self, 
                            anchor="w",
                            width=16,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Email del usuario:")

        name_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=name_user)
        email_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=email_user)

        edit_btt = Button(self, 
                            width=6, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.prim_hl_button, 
                            relief="flat", 
                            text="Editar", 
                            command= lambda: self.edit_user())
        exit_btt = Button(self, 
                            width=6, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.exit_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.exit_hl_button, 
                            relief="flat", 
                            text="Volver", 
                            command= lambda: close(extra_window))

        #configure 

        self.columnconfigure((0,1,2,3),weight=1)
        self.rowconfigure((0,1,2,3,4),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=4,sticky="we")

        #tree

        users_tree.grid(column=0,row=1,columnspan=4,rowspan=2,sticky="nswe")

        #scroll

        scroll.grid(column=0,row=1,columnspan=4,rowspan=2,sticky="nse")

        #label

        name_label.grid(column=0,row=3,sticky="n",pady=15)
        email_label.grid(column=1,row=3,sticky="n",pady=15)

        #entry

        name_entry.grid(column=0,row=3,sticky="s",pady=15)
        email_entry.grid(column=1,row=3,sticky="s",pady=15)

        #button

        edit_btt.grid(column=2,row=3,columnspan=2)
        exit_btt.grid(column=3,row=4,sticky="e",padx=10)
    
    def edit_user(self):
        pass

#
#
#

class Orders(Frame):
    def __init__(self,extra_window):
        
        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #struct

        self.create_order_struct(extra_window)

    def create_order_struct(self,extra_window):

        #var

        order_columns = ("usuario","ropa","servicio","prioridad","comentario","precio","estado")

        #create

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=extra_window.prim_bg_label,
                        fieldbackground=extra_window.prim_bg_label,
                        foreground=extra_window.letter_color
                        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview",background=[("selected",extra_window.secc_bg)])
        
        style.configure("Treeview.Heading",
                        background=extra_window.prim_bg_button,
                        foreground=extra_window.letter_color,
                        relief="flat")
        style.map("Treeview.Heading",background=[("active","#44051b")])

        tree_orders = ttk.Treeview(self,columns=order_columns,show="headings")
        tree_orders.column("usuario",width=70)
        tree_orders.column("ropa",width=120)
        tree_orders.column("servicio",width=120)
        tree_orders.column("prioridad",width=50)
        tree_orders.column("comentario",width=150)
        tree_orders.column("precio",width=60)
        tree_orders.column("estado",width=70)

        tree_orders.heading("usuario",text="Usuario")
        tree_orders.heading("ropa",text="Ropa")
        tree_orders.heading("servicio",text="Servicio")
        tree_orders.heading("prioridad",text="Prio.")
        tree_orders.heading("comentario",text="Comen.")
        tree_orders.heading("precio",text="Precio")
        tree_orders.heading("estado",text="Estado")

        scroll = Scrollbar(self ,orient=VERTICAL ,command=tree_orders.yview)
        tree_orders.configure(yscroll=scroll.set)

        main_title = Label(self, 
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Base de pedidos")

        state_label = Label(self, 
                            anchor="w",
                            width=18,
                            font=("Calibri",14), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Establezca el estado:")

        state_cb = ttk.Combobox(self)

        confirm_btt = Button(self, 
                            width=8, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.prim_hl_button, 
                            relief="flat", 
                            text="Establecer", 
                            command= lambda: self.change_state())
        exit_btt = Button(self, 
                            width=6, 
                            height=1, 
                            font=("Calibri",11), 
                            bg=extra_window.exit_bg_button, 
                            fg=extra_window.letter_color, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.exit_hl_button, 
                            relief="flat", 
                            text="Volver", 
                            command= lambda: close(extra_window))

        #configure
        
        self.columnconfigure((0,1,2,3),weight=1)
        self.rowconfigure((0,1,2,3,4,5),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=4,sticky="we")

        #tree

        tree_orders.grid(column=0,row=1,columnspan=4,rowspan=3,sticky="nswe")

        #scroll

        scroll.grid(column=0,row=1,columnspan=4,rowspan=3,sticky="nse")

        #label

        state_label.grid(column=0,row=4,sticky="e")

        #combobox

        state_cb.grid(column=1,row=4)
        state_cb["values"] = ("Pausado","En espera","Finalizado")
        state_cb["state"] = "readonly"

        #button

        confirm_btt.grid(column=2,row=4,columnspan=2)
        exit_btt.grid(column=3,row=5)
    
    def change_state(self):
        pass

#
#
#

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
    Main("Volpe project", (800,600,300,50), True, "#D7D6D2")