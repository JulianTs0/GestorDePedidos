from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from back_admin import *



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

        #struct

        self.create_login(main_window)

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

        #binds

        main_window.bind("<Return>", lambda e : self.login(main_window,user_input.get(),password_input.get()))

    def login(self, main_window, user_name, user_password):
        login_res = login_admin(user_name,user_password)
        if isinstance(login_res,str):
            messagebox.showwarning("Error al inciar sesion",login_res)
        else:
            messagebox.showinfo("Inicio de sesion","Inicio de sesion exitoso")
            main_window.status.destroy()
            main_window.status = MainMenu(main_window, login_res)



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
    
    def backward(self,main_window,user_name):
        delogin_res = de_login(user_name)
        if delogin_res is not None:
            messagebox.showerror("Error",delogin_res)
        else:
            messagebox.showinfo("Sesion cerrada","La sesion fue cerrada con exito")
            main_window.status.destroy()
            main_window.status = Login(main_window)

    def register_account(self,back_color):
        Extra("Registro de cuenta",[650,600,400,50],True,back_color,"r",self.user)

    def price_data(self,back_color):
        Extra("Base de precios",[700,600,400,50],True,back_color,"p")

    def modify_users(self,back_color):
        Extra("Base de usuarios",[600,600,400,50],True,back_color,"u")

    def modify_orders(self,back_color):
        Extra("Base de pedidos",[1000,600,200,50],True,back_color,"o")

    def close_and_delogin(self,main_window,user_name):
        de_login(user_name,True)
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
            self.status = Register(self,user_data)
        elif op == "p":
            self.status = Price(self)
        elif op == "u":
            self.status = Users(self)
        elif op == "o":
            self.status = Orders(self)

        #loop

        self.mainloop()



# Ordenar los arboles al hacer click en las cabeceras
# Sacar el print(id_content)
class Register(Frame):
    def __init__(self,extra_window,user):

        #setup

        super().__init__(extra_window)
        self.configure(bg=extra_window.secc_bg,padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.98, anchor="center")

        #var

        self.user = user

        #struct

        self.create_register(extra_window)

    def create_register(self,extra_window):

        #var

        admin_name = StringVar()
        admin_pass = StringVar()
        tree_columns = ("id","nombre","contra")
        
        #create

        style = ttk.Style(self)
        config_style(style,extra_window)

        admins_tree = ttk.Treeview(self,columns=tree_columns,show="headings")
        admins_tree.column("id" ,width=30)
        admins_tree.column("nombre" ,width=80)
        admins_tree.column("contra" ,width=80)

        admins_tree.heading("id",text="Id")
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

        id_label = Label(self, 
                            anchor="center", 
                            font=("Calibri",11), 
                            bg=extra_window.prim_bg_label, 
                            fg=extra_window.letter_color, 
                            text="Id del usuario: ", 
                            width=10, 
                            wraplength=80)
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

        id_text = Text(self,
                        height=1, 
                        width=4,
                        fg=extra_window.prim_bg_label
                        )

        user_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=admin_name)
        password_entry = Entry(self,
                            font=("Calibri",9), 
                            fg=extra_window.prim_bg_label, 
                            textvariable=admin_pass,
                            show="*")

        confirm_btt = Button(self,
                            fg=extra_window.letter_color, 
                            bg=extra_window.prim_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.prim_hl_button, 
                            relief="flat", 
                            text="Registrar", 
                            width=8, 
                            height=1, 
                            command= lambda: self.register_admin(user_entry,password_entry,id_text,admins_tree)
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
                            command= lambda: self.edit_admin(user_entry,password_entry,id_text,admins_tree)
                            )
        delete_btt = Button(self,
                            fg=extra_window.letter_color, 
                            bg=extra_window.secc_bg_button, 
                            activeforeground=extra_window.letter_color, 
                            activebackground=extra_window.secc_hl_button, 
                            relief="flat", 
                            text="Eliminar", 
                            width=8, 
                            height=1, 
                            command= lambda: self.select_admin_delete(admins_tree,user_entry,password_entry,id_text)
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

        self.update_tree(admins_tree,user_entry,password_entry,id_text)

        #configure

        self.columnconfigure((0,1,2,3,4,5),weight=1)
        self.rowconfigure((0,1,2,3,4),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=5,sticky="we")

        #label

        id_label.grid(column=3,row=1,sticky="n",columnspan=2)
        user_label.grid(column=3,row=2,sticky="n",columnspan=2)
        password_label.grid(column=3,row=3,sticky="n",columnspan=2)

        #text

        id_text.grid(column=3,row=1,columnspan=2)
        id_text["state"] = "disabled"

        #entry

        user_entry.grid(column=3,row=2,columnspan=2)
        password_entry.grid(column=3,row=3,columnspan=2)

        #button

        confirm_btt.grid(column=1,row=4,sticky="e")
        edit_btt.grid(column=2,row=4,padx=20)
        delete_btt.grid(column=3,row=4,sticky="w")
        exit_btt.grid(column=5,row=4)

        #tree

        admins_tree.grid(column=0,row=1,columnspan=2,rowspan=3,sticky="nswe")
        admins_tree.bind("<<TreeviewSelect>>",lambda e: self.select_tree(admins_tree,user_entry,password_entry,id_text))

        #scroll

        scroll.grid(column=2,row=1,rowspan=3,sticky="nsw")

    def register_admin(self,name,password,id,tree):

        option,title,body = register_admin_db(name.get(), password.get()).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)
            self.update_tree(tree,name,password,id)

    def edit_admin(self,name,password,id,tree):

        id_content = id.get("1.0","end-1c")

        print(id_content)

        if id_content == "":
            messagebox.showwarning("No se selecciono un usuario","No se puede modificar un usuario que no existe")
            return
        
        option,title,body  = modify_admin(name.get(), password.get(),id_content).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)
            self.update_tree(tree,name,password,id)

    def update_tree(self,tree,user_field,pass_field,id_field):

        for children in tree.get_children():
            tree.selection_remove(children)

        tree.delete(*tree.get_children())
        admins_result = get_admins(self.user)

        if isinstance(admins_result,str):
            messagebox.showerror("Error",admins_result)
        else:
            for item in admins_result:
                tree.insert("" ,END ,values=item)
            self.delete_fields(user_field,pass_field,id_field)

    def select_tree(event,tree,name_entry,pass_entry,id_text):

        select = tree.focus()

        try:

            selected_value = tree.item(select)["values"]

            id = selected_value[0]
            name = selected_value[1]
            password = selected_value[2]

            id_text["state"] = "normal"
            id_text.delete("1.0",END)
            id_text.insert("1.0",id)
            id_text["state"] = "disabled"
            name_entry.delete(0,END)
            name_entry.insert(0,name)
            pass_entry.delete(0,END)
            pass_entry.insert(0,password)

        except:
            pass

    def delete_fields(self,user_field,pass_field,id_field):
        id_field["state"] = "normal"
        id_field.delete("1.0",END)
        id_field["state"] = "disabled"
        user_field.delete(0,END)
        pass_field.delete(0,END)

    def select_admin_delete(self,tree,user_field,pass_field,id_field):
        select = tree.focus()

        if not select:
            messagebox.showwarning("No se pudo eliminar el administrador","Seleccione una cuenta para eliminarla")
        else:
            values = tree.item(select)["values"]
            option,title,body = delete_admin_user(values[0]).split("|")

            if option == "0":
                messagebox.showerror(title,body)
            else:
                messagebox.showinfo(title,body)

        self.update_tree(tree,user_field,pass_field,id_field)



# Añadir la cantidad de pedidos que tiene cada usuario
# Solo permitir cambiar el nombre
# Ordenar los arboles al hacer click en las cabeceras
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
        user_columns = ("nombre","email","id")

        #create

        style = ttk.Style(self)
        config_style(style,extra_window)

        users_tree = ttk.Treeview(self,columns=user_columns,show="headings")
        users_tree.column("id",width=20)
        users_tree.column("nombre",width=60)
        users_tree.column("email",width=140)

        users_tree.heading("id",text="ID")
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
                            command= lambda: self.edit_user(users_tree,name_entry,email_entry))
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

        self.update_tree(users_tree,name_entry,email_entry)

        #configure 

        self.columnconfigure((0,1,2,3),weight=1)
        self.rowconfigure((0,1,2,3,4),weight=1)

        #title

        main_title.grid(column=0,row=0,columnspan=4,sticky="we")

        #tree

        users_tree.grid(column=0,row=1,columnspan=4,rowspan=2,sticky="nswe")
        users_tree.bind("<<TreeviewSelect>>",lambda e: self.select_tree(users_tree,name_entry,email_entry))

        #scroll

        scroll.grid(column=0,row=1,columnspan=4,rowspan=2,sticky="nse")

        #label

        name_label.grid(column=0,row=3,sticky="n",pady=15)
        email_label.grid(column=1,row=3,sticky="n",pady=15)

        #entry

        name_entry.grid(column=0,row=3,sticky="s",pady=15)
        email_entry.grid(column=1,row=3,sticky="wes",pady=15,padx=35)

        #button

        edit_btt.grid(column=2,row=3,columnspan=2)
        exit_btt.grid(column=3,row=4,sticky="e",padx=10)
    
    def edit_user(self,tree,name,email):

        select = tree.focus()
        try:
            selected_value = tree.item(select)["values"]
            ide = selected_value[2]
        except:
            messagebox.showwarning("No hay ningun usuario seleccionado","Seleccione un usuario de la planilla")
            return
        
        option,title,body = modify_user(name.get(), email.get(),ide).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)
            self.update_tree(tree,name,email)

    def update_tree(self,tree,user_field,email_field):

        for children in tree.get_children():
            tree.selection_remove(children)

        tree.delete(*tree.get_children())
        user_result = get_users()

        if isinstance(user_result,str):
            messagebox.showerror("Error",user_result)
        else:
            for item in user_result:
                tree.insert("" ,END ,values=item)
            self.delete_fields(user_field,email_field)

    def delete_fields(self,user_field,pass_field):
        user_field.delete(0,END)
        pass_field.delete(0,END)

    def select_tree(event,tree,name_entry,email_entry):

        select = tree.focus()

        try:

            selected_value = tree.item(select)["values"]

            name = selected_value[0]
            email = selected_value[1]

            name_entry.delete(0,END)
            name_entry.insert(0,name)
            email_entry.delete(0,END)
            email_entry.insert(0,email)

        except:
            pass



# Añadir precios
# Eliminar precios
# Ordenar los arboles al hacer click en las cabeceras
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
        tree_columns = ("nombre","precio","id")

        #create

        style = ttk.Style(self)
        config_style(style,extra_window)

        price_tree = ttk.Treeview(self,columns=tree_columns,show="headings")
        price_tree.column("id",width=30)
        price_tree.column("nombre",width=80)
        price_tree.column("precio",width=80)

        price_tree.heading("id",text="Id")
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
                            command= lambda: self.edit_price(price_tree,data_cb,param_entry,price_entry))
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
        data_cb.bind("<<ComboboxSelected>>", lambda e: self.update_tree(price_tree,param_entry,param_entry,data_cb))

        #treeview

        price_tree.grid(column=0,row=2,columnspan=4,rowspan=3,sticky="nswe",padx=10)
        price_tree.bind("<<TreeviewSelect>>",lambda e: self.select_tree(price_tree,param_entry,price_entry))

        #scroll

        scroll.grid(column=0,row=2,columnspan=4,rowspan=3,sticky="nse")

        #button

        edit_btt.grid(column=4,row=4)
        exit_btt.grid(column=4,row=5,sticky="e")

    def edit_price(self,tree,param_cb,name,price):
        
        select = tree.focus()
        option = param_cb.current()

        try:
            selected_value = tree.item(select)["values"]
            ide = selected_value[2]
        except:
            messagebox.showwarning("No hay ningun parametro seleccionado","Seleccione un parametro de la planilla")
            return

        option,title,body = modify_params(name.get(), price.get(),ide,option).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)
            self.update_tree(tree,name,price,param_cb)

    def update_tree(self,tree,name_field,price_field,param_combo):

        option = param_combo.current()

        for children in tree.get_children():
            tree.selection_remove(children)
        tree.delete(*tree.get_children())

        param_result = get_params(option)

        if isinstance(param_result,str):
            messagebox.showerror("Error",param_result)
        else:
            for item in param_result:
                tree.insert("" ,END ,values=item)
            self.delete_fields(name_field,price_field)

    def delete_fields(self,name_field,price_field):
        name_field.delete(0,END)
        price_field.delete(0,END)
    
    def select_tree(self,tree,name_entry,price_entry):

        select = tree.focus()

        try:

            selected_value = tree.item(select)["values"]

            name = selected_value[0]
            price = selected_value[1]

            name_entry.delete(0,END)
            name_entry.insert(0,name)
            price_entry.delete(0,END)
            price_entry.insert(0,price)

        except:
            pass



# Ordenar los arboles al hacer click en las cabeceras
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

        order_columns = ("id","usuario","ropa","servicio","prioridad","comentario","precio","estado")

        #create

        style = ttk.Style(self)
        config_style(style,extra_window)

        tree_orders = ttk.Treeview(self,columns=order_columns,show="headings")
        tree_orders.column("id",width=30)
        tree_orders.column("usuario",width=70)
        tree_orders.column("ropa",width=120)
        tree_orders.column("servicio",width=120)
        tree_orders.column("prioridad",width=50)
        tree_orders.column("comentario",width=150)
        tree_orders.column("precio",width=60)
        tree_orders.column("estado",width=70)

        tree_orders.heading("id",text="ID")
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
                            command= lambda: self.change_state(tree_orders,state_cb))
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
        
        self.update_tree(tree_orders)

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
        state_cb["values"] = ("Pausado","En proceso","Finalizado")
        state_cb["state"] = "readonly"

        #button

        confirm_btt.grid(column=2,row=4,columnspan=2)
        exit_btt.grid(column=3,row=5)
    
    def change_state(self,tree,status_combo):

        
        select = tree.focus()
        status = status_combo.get()

        try:
            selected_value = tree.item(select)["values"]
            ide = selected_value[0]
        except:
            messagebox.showwarning("No hay ningun pedido seleccionado","Seleccione un pedido de la planilla")
            return

        option,title,body = modify_orders(status,ide).split("|")

        if option == "0":
            messagebox.showerror(title,body)
        elif option == "1":
            messagebox.showwarning(title,body)
        elif option == "2":
            messagebox.showinfo(title,body)
        
        self.update_tree(tree)

    def update_tree(self,tree):

        for children in tree.get_children():
            tree.selection_remove(children)

        tree.delete(*tree.get_children())
        order_result = get_orders()

        if isinstance(order_result,str):
            messagebox.showerror("Error",order_result)
        else:
            for item in order_result:
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



def config_style(style,extra_window):
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



if __name__ == "__main__":
    Main("Volpe project", (800,600,300,50), True, "#D7D6D2")