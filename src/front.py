from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from back import *



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



class Login(Frame):
    def __init__(self, main_window):

        #setup

        super().__init__(main_window)
        self.configure(bg=main_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #init func

        result = unexpected_delogin()

        if result != "":
            title,msg = result.split("|")
            messagebox.showerror(title,msg)
            close(main_window)

        else:
            #struct
            self.create_login(main_window)

    def create_login(self, main_window):

        #var

        user_name = StringVar()
        user_password = StringVar()

        #create

        url_font = font.Font(underline=True,size=11)
        input_font = font.Font(weight="bold",size=9)

        login_title = Label(self, 
                            anchor="center", 
                            font=("TkMenuFont",18), 
                            bg=main_window.prim_bg_label, 
                            fg=main_window.letter_color, 
                            text="Bienvenidos de nuevo a Volpe\nIngrese sesion o registrese"
                            )

        user_label = Label(self, 
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
        register_label = Label(self, 
                               anchor="center", 
                               font=url_font, 
                               bg=main_window.secc_bg, 
                               fg=main_window.url_letter_color,
                               cursor="mouse", 
                               text="Si no tiene una cuenta registrada, Haga click aqui."
                               )

        user_input = Entry(self, 
                           font=input_font,
                           fg=main_window.prim_bg_label,
                           textvariable=user_name
                           )
        password_input = Entry(self, font=input_font,
                               fg=main_window.prim_bg_label,
                               textvariable=user_password,
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
                              command= lambda: self.login(main_window,user_name.get(),user_password.get())
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
        self.rowconfigure((0,1,2,3,4,5,6), weight=1)

        #title

        login_title.grid(column=0, row=0, columnspan=4, sticky="we")

        #label

        user_label.grid(column=0, row=2, sticky="e", padx=30)
        password_label.grid(column=0, row=3, sticky="e", padx=30)
        register_label.grid(column=0, row=4, columnspan=4, sticky="s",padx=20)
        register_label.bind("<Button-1>", lambda e: self.register(main_window.extra_bg))


        #entry

        user_input.grid(column=1, row=2, sticky="we")
        password_input.grid(column=1, row=3, sticky="we")

        #button

        login_button.grid(column=0, row=6, columnspan=3)
        exit_button.grid(column=2,row=6 ,padx=20 ,sticky="e")

        #binds

        main_window.bind("<Return>", lambda e : self.login(main_window,user_name.get(),user_password.get()))

    def login(self, main_window, user_name, user_password):

        login_res = login_user(user_name,user_password)

        if isinstance(login_res,str):
            messagebox.showwarning("Error al inciar sesion",login_res)

        else:
            messagebox.showinfo("Inicio de sesion","Inicio de sesion exitoso")
            main_window.status.destroy()
            main_window.status = MainMenu(main_window, login_res)

    def register(self,back_color):
        Extra("Registro de cuenta",[450,600,700,50],True,back_color,"r")



class MainMenu(Frame):
    def __init__(self, main_window, user):

        #setup

        super().__init__(main_window)
        self.configure(bg=main_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.close_and_delogin(main_window,user.name))
        main_window.unbind("<Return>")

        #var

        self.user = user

        #struct

        self.create_menu(main_window)

    def create_menu(self,main_window):
        
        #create

        main_title = Label(self,
                           anchor="center",
                           font=("TkMenuFont",18),
                           fg=main_window.letter_color,
                           bg=main_window.prim_bg_label,
                           text=f"Bienvenido de nuevo {self.user.name}"
                           )

        first_lb = Label(self,
                         anchor="center",
                         font=("Calibri",14),
                         fg=main_window.letter_color,
                         bg=main_window.prim_bg_label, 
                         text="Realize un pedido", width=20
                         )
        secc_lb = Label(self,
                        anchor="center",
                        font=("Calibri",14),
                        fg=main_window.letter_color,
                        bg=main_window.prim_bg_label, 
                        text="Ver mis pedidos",
                        width=20
                        )

        first_btt = Button(self,
                           width=9,
                           height=1,
                           font=("Calibri",12),
                           fg=main_window.letter_color,
                           bg=main_window.prim_bg_button,
                           activeforeground=main_window.letter_color, 
                           activebackground=main_window.prim_hl_button, 
                           relief="flat" ,text="Seleccionar", 
                           command= lambda: self.order(self.user,main_window.extra_bg)
                           )
        secc_btt = Button(self,
                          width=9,
                          height=1,
                          font=("Calibri",12),
                          fg=main_window.letter_color,
                          bg=main_window.prim_bg_button ,
                          activeforeground=main_window.letter_color, 
                          activebackground=main_window.prim_hl_button, 
                          relief="flat" ,text="Seleccionar", 
                          command= lambda: self.show_orders(self.user,main_window.extra_bg)
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

    def order(self,user,back_color):
        Extra("Generador de pedidos",[500,600,700,50],True,back_color,"o",user)

    def show_orders(self,user,back_color):
        Extra("Lista de pedidos", (800,600,350,100), True, back_color, "s",user)

    def backward(self,main_window,user_name):

        delogin_res = de_login(user_name)

        if delogin_res is not None:
            messagebox.showerror("Error",delogin_res)
            close(main_window)

        else:
            messagebox.showinfo("Sesion cerrada","La sesion fue cerrada con exito")
            main_window.status.destroy()
            main_window.status = Login(main_window)

    def close_and_delogin(self,main_window,user_name):

        de_login(user_name)
        close(main_window)



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
        elif op == "o":
            self.status = Order(self,user_data)
        elif op == "s":
            self.status = ShowOrder(self,user_data)

        #loop

        self.mainloop()



class Register(Frame):
    def __init__(self,extra_window):

        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #var

        self.ok = False

        #struct

        self.create_account(extra_window)

    def create_account(self ,extra_window):

        #var
        
        user_name = StringVar()
        user_email = StringVar()
        user_pasword = StringVar()
        password_rep = StringVar()
        
        #create
        
        main_title = Label(self,
                           anchor="center", 
                           font=("TkMenuFont",18), 
                           bg=extra_window.prim_bg_label, 
                           fg=extra_window.letter_color, 
                           text="Ingrese sus datos para\nRegistrar una cuenta"
                           )

        user_lb = Label(self, 
                        anchor="center", 
                        font=("Calibri",11), 
                        bg=extra_window.prim_bg_label, 
                        fg=extra_window.letter_color, 
                        text="Ingrese su nombre de usuario: ", 
                        width=18, 
                        wraplength=150
                        )
        email_lb = Label(self, 
                         anchor="center", 
                         font=("Calibri",11), 
                         bg=extra_window.prim_bg_label, 
                         fg=extra_window.letter_color, 
                         text="Ingrese su correo electronico: ", 
                         width=18, 
                         wraplength=150
                         )
        pass_lb = Label(self, 
                        anchor="center", 
                        font=("Calibri",11), 
                        bg=extra_window.prim_bg_label, 
                        fg=extra_window.letter_color, 
                        text="Ingrese su contraseña: ", 
                        width=18, 
                        wraplength=150
                        )
        pass_rep_lb = Label(self, 
                            anchor="center", 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Vuelva a ingresar su contraseña: ", 
                            width=18, 
                            wraplength=150
                            )

        user_entry = Entry(self, 
                           font=("Calibri",9), 
                           fg=extra_window.prim_bg_label, 
                           textvariable=user_name
                           )
        email_entry = Entry(self, 
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=user_email
                            )
        pass_entry = Entry(self, 
                           font=("Calibri",9), 
                           fg=extra_window.prim_bg_label, 
                           textvariable=user_pasword, 
                           show="*"
                           )
        pass_rep_entry = Entry(self, 
                               font=("Calibri",9), 
                               fg=extra_window.prim_bg_label, 
                               textvariable=password_rep, 
                               show="*"
                               )

        confirm_btt = Button(self, 
                             fg=extra_window.letter_color, 
                             bg=extra_window.prim_bg_button, 
                             activeforeground=extra_window.letter_color, 
                             activebackground=extra_window.prim_hl_button, 
                             relief="flat", 
                             text="Registrarse", 
                             width=8, 
                             height=1, 
                             command= lambda: self.register_account(extra_window,user_name.get(),user_pasword.get(),password_rep.get(),user_email.get())
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

    def register_account(self, extra_window, name, password, rep, email):

        option,title,body = register_in_db(self, extra_window, name, password, rep, email).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)



class Order(Frame):
    def __init__(self ,extra_window, user):

        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")

        #var

        self.user = user

        #struct

        self.create_order(extra_window)

    def create_order(self,extra_window):

        #var

        ropa_stock = get_fields_name("ropas")
        servicio_stock = get_fields_name("servicios")
        prioridad_available = get_fields_name("prioridades")

        #create

        main_title = Label(self,
                           anchor="center",
                           fg=extra_window.letter_color,
                           bg=extra_window.prim_bg_label,
                           font=("TkMenuFont",18),
                           text="Realize su pedido"
                           )

        ropa_lb = Label(self, 
                        anchor="center",
                        fg=extra_window.letter_color,
                        bg=extra_window.prim_bg_label,
                        font=("Calibri",12),
                        width=24,
                        wraplength=180,
                        text="Seleccione la ropa del pedido:"
                        )
        servicio_lb = Label(self, 
                            anchor="center",
                            fg=extra_window.letter_color,
                            bg=extra_window.prim_bg_label,
                            font=("Calibri",12),
                            width=24,
                            wraplength=180,
                            text="Seleccione el servicio deseado:"
                            )
        prioridad_lb = Label(self, 
                             anchor="center",
                             fg=extra_window.letter_color,
                             bg=extra_window.prim_bg_label,
                             font=("Calibri",12),
                             width=24,
                             wraplength=180,
                             text="Seleccione la prioridad que desee:"
                             )
        comentario_lb = Label(self, 
                              anchor="center",
                              fg=extra_window.letter_color,
                              bg=extra_window.prim_bg_label,
                              font=("Calibri",12),
                              width=24,
                              wraplength=180,
                              text="Añada un comentario si desea:"
                              )

        ropa_cb = ttk.Combobox(self)
        servicio_cb = ttk.Combobox(self)
        prioridad_cb = ttk.Combobox(self)

        comentario_input = Text(self,
                                height=6, 
                                width=25, 
                                wrap="word", 
                                spacing3="5",
                                fg=extra_window.prim_bg_label
                                )

        confirm_btt = Button(self, 
                             width=10,
                             height=1,
                             bg=extra_window.prim_bg_button,
                             fg=extra_window.letter_color,
                             activeforeground=extra_window.letter_color, 
                             activebackground=extra_window.prim_hl_button, 
                             relief="flat",
                             text="Hacer pedido",
                             command= lambda: self.make_order(ropa_cb.get(),servicio_cb.get(),prioridad_cb.current(),comentario_input.get("1.0","end"),self.user)
                             )
        exit_btt = Button(self, 
                          width=8,
                          height=1,
                          bg=extra_window.exit_bg_button,
                          fg=extra_window.letter_color, 
                          activeforeground=extra_window.letter_color, 
                          activebackground=extra_window.exit_hl_button, 
                          relief="flat",
                          text="Volver",
                          command= lambda: close(extra_window)
                          )

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
        ropa_cb["values"] = ropa_stock
        ropa_cb["state"] = "readonly"
        servicio_cb.grid(column=1, row=2, sticky="w" ,padx=20)
        servicio_cb["values"] = servicio_stock
        servicio_cb["state"] = "readonly"
        prioridad_cb.grid(column=1, row=3, sticky="w" ,padx=20)
        prioridad_cb["values"] = prioridad_available
        prioridad_cb["state"] = "readonly"

        #entry

        comentario_input.grid(column=1, row=4, sticky="w" ,padx=20)

        #button

        confirm_btt.grid(column=0 ,row=5, columnspan=2)
        exit_btt.grid(column=2, row=5)   

    def make_order(self,ropa,servicio,prioridad,conentario,user):

        option,title,body = create_order_db(ropa,servicio,prioridad,conentario,user).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body) 



class ShowOrder(Frame):
    def __init__(self ,extra_window,user):

        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.95, anchor="center")
    
        #var
        
        self.user = user

        #struct

        self.show_display(extra_window)

    def show_display(self ,extra_window):

        #var

        tree_columns = ("num_pedido","ropa","servicio","prioridad","precio","estado")

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

        main_title = Label(self,
                           anchor="center",
                           fg=extra_window.letter_color,
                           bg=extra_window.prim_bg_label,
                           font=("TkMenuFont",18),
                           text="Sus pedidos"
                           )
   
        orders_tree = ttk.Treeview(self ,columns=tree_columns ,show="headings")
        orders_tree.column("num_pedido", width=20, anchor="center")
        orders_tree.column("ropa" ,width=80)
        orders_tree.column("servicio" ,width=120)
        orders_tree.column("prioridad" ,width=80)
        orders_tree.column("precio" ,width=80)
        orders_tree.column("estado" ,width=120)

        orders_tree.heading("num_pedido", text="Nº Pedido",)
        orders_tree.heading("ropa" ,text="Ropa")
        orders_tree.heading("servicio" ,text="Servicio")
        orders_tree.heading("prioridad" ,text="Prioridad")
        orders_tree.heading("precio" ,text="Precio")
        orders_tree.heading("estado" ,text="Estado")
        
        self.update_tree(orders_tree)

        scroll = Scrollbar(self ,orient=VERTICAL ,command=orders_tree.yview)
        orders_tree.configure(yscroll=scroll.set)

        delete_btt = Button(self,
                            height=1,
                            width=8,
                            fg=extra_window.letter_color,
                            bg=extra_window.secc_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.secc_hl_button, 
                            relief="flat",
                            text="Cancelar",
                            command=lambda: self.select_tree(orders_tree)
                            )
        exit_btt = Button(self,
                          height=1,
                          width=8,
                          fg=extra_window.letter_color,
                          bg=extra_window.exit_bg_button,
                          activeforeground=extra_window.letter_color,
                          activebackground=extra_window.exit_hl_button, 
                          relief="flat",
                          text="Volver",
                          command=lambda: close(extra_window)
                          )

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

        exit_btt.grid(column=2 ,row=2, sticky="e", padx=20)
        delete_btt.grid(column=0 ,row=2, sticky="w", padx=20)

    def select_tree(self,tree):
        select = tree.focus()

        if not select:
            messagebox.showwarning("No se pudo cancelar el pedido","Seleccione un pedido para cancelarlo")
        else:
            values = tree.item(select)["values"]
            delete_result = delete_order(values[0])
            if delete_result is not None:
                messagebox.showerror("Error",delete_result)
            else:
                messagebox.showinfo("Accion exitosa","Su pedido fue cancelado con exito")
        
        self.update_tree(tree)

    def update_tree(self,tree):
        tree.delete(*tree.get_children())
        orders_result = get_user_orders(self.user)

        if isinstance(orders_result,str):
            messagebox.showerror("Error",orders_result)
        else:
            for item in orders_result:
                tree.insert("" ,END ,values=item)



def setup(self, tittle, size, resize, back_color):
    self.title(tittle)
    self.geometry(f"{size[0]}x{size[1]}+{size[2]}+{size[3]}")
    self.resizable(resize, resize)
    self.config(bg=back_color)
    self.protocol("WM_DELETE_WINDOW", lambda: close(self))



def close(object):
    object.quit()
    object.destroy()



if __name__ == "__main__":
   Main("Volpe project", (800,600,300,50), True, "#D7D6D2")