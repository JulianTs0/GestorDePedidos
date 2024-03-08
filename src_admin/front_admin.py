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
                           text="Modificar base de servicios"
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
                          command= lambda: self.first()
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
                          command= lambda: self.secc()
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
                          command= lambda: self.thirt()
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
                          command= lambda: self.four()
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
    
    def first(self):
        pass
    
    #
    #
    #
    
    def secc(self):
        pass
    
    #
    #
    #
    
    def thirt(self):
        pass
    
    #
    #
    #
    
    def four(self):
        pass
    
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
            self.status = None
        elif op == "o":
            self.status = None
        elif op == "s":
            self.status = None

        #loop

        self.mainloop()

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