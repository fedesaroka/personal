import customtkinter as ctk
from bicicleteria import Bicicleteria
from usuario import Usuario, Administrador, Empleado, Cliente
from calendar import monthrange
from analisis import *
from typing import Literal
from bicicleta import Bicicleta, Playera, Carrera, Ciudad
from auxiliares import pack, pack_forget, graficos
from datetime import date, datetime
from lista_enlazada import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Interfaz( ctk.CTk ) :
    
    def __init__(self):
        super().__init__()
        self.title('Bicicletería')
        ctk.set_appearance_mode("dark")
        self.inicio()
    
    def inicio(self) :
        
        self.error_archivo = ctk.CTkLabel(  self , 
                                            text='''
Es posible que el archivo con la información de la 
bicicletería no se encuentre ubicado correctamente. 
Para utilizar el programa, debe cerrar la ventana, 
ubicar el archivo y ejecutar el programa nuevamente.''' , 
                                            text_color='red')
        
        try :
            datos_bicicleteria = np.genfromtxt( 'datos_bicicleteria.csv' , 
                                                dtype=float , 
                                                encoding=None , 
                                                delimiter=',' , 
                                                usecols=1 )  
            
            self.bicicleteria = Bicicleteria(   precio_carrera = datos_bicicleteria[0],
                                                precio_ciudad = datos_bicicleteria[1],
                                                precio_playera = datos_bicicleteria[2],
                                                monto_caja = datos_bicicleteria[3],
                                                descuento_semanal = datos_bicicleteria[4],
                                                descuento_mensual = datos_bicicleteria[5],
                                                cant_reparadores = datos_bicicleteria[6] )
            
            self.bicicleteria.crear_archivos()
            self.bicicleteria.abrir_taller()
            
            # determina lo que sucede cuando el usuario cierra la ventana (se actualizan los archivos)  
            self.protocol( "WM_DELETE_WINDOW" , self.finalizar )
            
            # creamos un frame que va a contener a todos los frames
            self.contenedor = ctk.CTkFrame(self)
            self.contenedor.pack(side="top", fill="both", expand=True)
            
            self.frame_actual = None
            
            self.mostrar_frame(InicioSesion)
        except :
            self.geometry('360x100')
            self.error_archivo.pack()
    
    def mostrar_frame(self, F : type, activeUser : Usuario = None) :
        if self.frame_actual is not None :
            self.frame_actual.borrar_widgets()
            self.frame_actual.destroy()
            
        frame_nuevo = F(self.contenedor, self, self.bicicleteria, activeUser)
        self.frame_actual = frame_nuevo
        frame_nuevo.place(x=0, y=0, relwidth=1, relheight=1)
        
        
    def finalizar(self) :
        self.bicicleteria.actualizar_archivos()
        self.destroy()
    
    
class FrameObj(ctk.CTkFrame) :
    
    def __init__(   self, 
                    master : ctk.CTkFrame, 
                    interfaz : Interfaz, 
                    bicicleteria : Bicicleteria, 
                    width : int = 400, 
                    height : int = 400,
                    activeUser : Usuario = None ):
        
        super().__init__(master)
        
        self.master : ctk.CTkFrame = master
        self.interfaz : Interfaz = interfaz
        self.bicicleteria : Bicicleteria = bicicleteria
        self.activeUser : Administrador | Empleado | Cliente = activeUser
        
        self._width = width
        self._height = height
        self.interfaz.geometry( f'{self._width}x{self._height}' )
        self.interfaz.minsize( width=self._width, height=self._height)
        
        self.crear_widgets()
        
    @property   
    def width(self) :
        return self._width
    
    @width.setter
    def width(self, valor : int) :
        self._width = valor
        self.interfaz.geometry( f'{self._width}x{self._height}' )
        self.interfaz.minsize( width=self._width, height=self._height)
        
    @property   
    def height(self) :
        return self._height
    
    @height.setter
    def height(self, valor : int) :
        self._height = valor
        self.interfaz.geometry( f'{self._width}x{self._height}' )
        self.interfaz.minsize( width=self._width, height=self._height)
        
    def crear_widgets(self) :
        ctk.CTkLabel(self, text='Frame').pack()
     
    def borrar_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
 

class InicioSesion(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : Interfaz,  bicicleteria : Bicicleteria, activeUser=None):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=320,
                            height=235)
    
    def crear_widgets( self ) :
        
        self.mensaje_primer_uso = ctk.CTkLabel( self , 
                                                text=
'''Al ser el primer ingreso, debe iniciar sesión con
los siguientes datos y crear su usuario:

Nombre de usuario: admin2024
Contraseña: Admin123''')
        
        self.id_usuario = ctk.CTkEntry(self, placeholder_text="Nombre de usuario" , width=200 )
        self.id_usuario.bind( '<Return>' , self.validar_inicio ) # bind sirve para asociar una accion (en este caso apretar el boton enter) con una funcion
        
        self.contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña" , width=200 )
        self.contrasena.bind( '<Return>' , self.validar_inicio )
        
        self.boton_inicio = ctk.CTkButton(self, command=self.validar_inicio , text='Iniciar sesión' )
        self.boton_inicio.bind( '<Return>' , self.validar_inicio )
        
        self.incorrecto = ctk.CTkLabel( self , text_color='red' ,
                                        text=
'''El nombre de usuario o contraseña 
que ha proporcionado no son correctos.
Intente nuevamente.'''  )

        if self.bicicleteria.primer_uso() :
            self.height += 100
            pack(self.mensaje_primer_uso)
        
        pack( self.id_usuario , self.contrasena , self.boton_inicio )
    
        
    def validar_inicio(self, event=None) :
        
        id_usuario = self.id_usuario.get()
        contra = self.contrasena.get()
        
        info_usuario = self.bicicleteria.usuarios.get(id_usuario)
        
        if info_usuario is None or info_usuario[1] != contra  :
            pack(self.incorrecto)
        else :
            mapa = {'Administrador' : Administrador, 'Empleado' : Empleado, 'Cliente' : Cliente}
            
            usuario = mapa[info_usuario[2]](id = id_usuario ,
                                            nombre = info_usuario[0] , 
                                            contrasena = info_usuario[1] , 
                                            fecha_registro = info_usuario[3] ,
                                            bicicleteria = self.bicicleteria ) 
            
            self.activeUser = usuario
            
            mapa = {Administrador: MenuGeneral, Empleado : MenuGeneral, Cliente : MenuClientes}
            
            self.interfaz.mostrar_frame(mapa[type(self.activeUser)], self.activeUser)
            
    
# INTERFAZ PARA CLIENTES
#-----------------------------------------------------------------------------------------------------------------------------------------
class MenuClientes(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz,
                            bicicleteria=bicicleteria,
                            activeUser=activeUser)
        self.height += 34
        
    def crear_widgets(self) :
        
        self.cerrar_sesion = ctk.CTkButton( self , 
                                            text='Cerrar sesión' ,
                                            command=lambda : self.interfaz.mostrar_frame(InicioSesion) ,
                                            width=100 )
        self.cerrar_sesion.place( x=10 , y=10 )
        
        pack(ctk.CTkLabel( self , text='Bicicletas en alquiler' ))
        
        bicicletas = self.activeUser.bicis_en_alquiler()
        Muestreo(self).muestreo_menu_clientes(bicicletas)
    
        #Boton para que el cliente pueda realizar un alquiler
        self.nuevo_alq = ctk.CTkButton( self , 
                            text='Nuevo alquiler' , 
                            command=lambda : self.interfaz.mostrar_frame(AlqClientes, self.activeUser) )
        
        self.reparar = ctk.CTkButton(   self , 
                                        text='Reparar bicicleta' , 
                                        command=lambda : self.interfaz.mostrar_frame(RepClientes, self.activeUser))
        pack(self.nuevo_alq, self.reparar)
        
    def devolver_extender( self , bicicleta : Bicicleta , extender : bool ) :
        if not extender :
            self.activeUser.devolucion_extension( bicicleta , extender )
            self.interfaz.mostrar_frame(type(self), self.activeUser)
        else :
            while True :
                self.dias = ctk.CTkInputDialog( title='Extensión de alquiler' ,
                                                text='Ingrese la cantidad de días a extender' )
                dias = self.dias.get_input()
                if dias is None :
                    break
                if dias.isnumeric() and dias != '0' :
                    self.activeUser.devolucion_extension( bicicleta , extender , int(dias) )
                    break
                    
        
class AlqClientes(FrameObj) :
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master,
                            interfaz=interfaz,
                            bicicleteria=bicicleteria,
                            activeUser=activeUser,
                            width=330,
                            height=520)
     
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Volver' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuClientes, self.activeUser) ,
                        width=80 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel(self , 
                                    text = 'Seleccione una categoría' ,
                                    text_color= 'white' )
        self.mensaje.pack(pady=(40,0))
        
        self.muestreo = Muestreo(self)
        self.categoria = ctk.CTkOptionMenu( self , 
                                            values= ['Carrera' , 'Ciudad' , 'Playera'] ,
                                            command = lambda categoria : self.muestreo.muestreo_alq_clientes(categoria) )
        self.categoria.set( 'Categoria' )
        
        self.dias = ctk.CTkEntry( self , placeholder_text='Cantidad de días' , width=200 )
        
        pack(self.dias, self.categoria)
        
        
    def validar_alquiler(self, bicicleta : Bicicleta) :
        
        dias = self.dias.get()
        
        if dias.isnumeric() and int(dias) > 0 :
            
            self.confirmacion = ctk.CTkToplevel(self)
            self.confirmacion.title('Confirmación de alquiler')
            self.confirmacion.geometry('300x140')
            self.confirmacion.columnconfigure((0,1), weight=1)
            
            monto = self.bicicleteria.calcular_monto(bicicleta, int(dias))
            ctk.CTkLabel(   self.confirmacion, 
                            text=f'Información del alquiler\n\nDuracion: {dias} días\nMonto: ${monto}'
                            ).grid(row=0, columnspan=2, pady=(10,20))
            
            ctk.CTkButton(  self.confirmacion, 
                                text='Confirmar alquiler',
                                command=lambda : self.alquilar(bicicleta, int(dias)),
                                height=35
                                ).grid(row=1, column=0, padx=12, sticky='EW')
            
            ctk.CTkButton(  self.confirmacion, 
                                text='Cancelar',
                                command=self.confirmacion.destroy,
                                height=35
                                ).grid(row=1, column=1, padx=12, sticky='EW')
            
            self.confirmacion.grab_set()

        else :
            self.mensaje.configure( text = 'Ingreso inválido en el campo\n"Cantidad de días"' ,
                                    text_color = 'red')
        
    def alquilar(self, bicicleta : Bicicleta, dias : int ) :
        self.confirmacion.destroy()
        self.activeUser.alquilar( bicicleta , dias )
        self.interfaz.mostrar_frame(MenuClientes, self.activeUser)


class RepClientes(FrameObj) :
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master,
                            interfaz=interfaz,
                            bicicleteria=bicicleteria,
                            activeUser=activeUser,
                            width=330,
                            height=520)
     
    def crear_widgets(self) :
        pack_forget(self.pack_slaves())
        self.height = 440
        
        ctk.CTkButton(  self , 
                        text='Volver' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuClientes, self.activeUser) ,
                        width=80 ).place( x=10 , y=10 )
        
        
        if not hasattr(self, 'texto') :
            self.texto = 'Ingrese los datos de la bicicleta'
        self.mensaje = ctk.CTkLabel( self , text_color='white',text=self.texto)
        self.mensaje.pack(pady=(50,10))

        self.marca  = ctk.CTkEntry( self , placeholder_text='Marca' , width=250 )
        self.color  = ctk.CTkEntry( self , placeholder_text='Color' , width=250 )
        self.precio = ctk.CTkEntry( self , placeholder_text='Precio' , width=250 )
        
        self.estado = ctk.CTkEntry( self , placeholder_text='Estado (1-10)' , width=250 )
        
        self.categoria = ctk.CTkOptionMenu( self , values= ['Carrera' , 'Ciudad' , 'Playera']  )
        self.categoria.set( 'Categoria' )
        
        self.reparar = ctk.CTkButton( self , text='Reparar' , command = self.validar_datos )
        
        pack(self.marca, self.color, self.precio, self.estado, self.categoria, self.reparar)
        
    def validar_datos(self):
        try :
            if (self.marca.get()+self.color.get()).isalpha() and self.estado.get().isnumeric() and 0 < int(self.estado.get()) < 11 and self.categoria.get() != 'Categoria' :
                
                categoria_class_map = { 'Carrera' : Carrera , 
                                        'Ciudad'  : Ciudad ,
                                        'Playera' : Playera }
                
                bicicleta = categoria_class_map[self.categoria.get()](  id = self.bicicleteria.generar_id() , 
                                                                        marca = self.marca.get() , 
                                                                        color = self.color.get() , 
                                                                        precioCompra = float(self.precio.get()) , 
                                                                        estado = int(self.estado.get()) )
                
                self.texto = self.activeUser.reparacion( bicicleta, self.activeUser.id )
                
                pack_forget(self.marca, self.color, self.precio, self.estado, self.categoria, self.reparar)
                self.crear_widgets()
            else : 
                raise ValueError
        except ValueError :
            self.mensaje.configure( text_color='red', text = 
'''Los datos ingresados no son válidos.
Intente nuevamente''' )         
#-----------------------------------------------------------------------------------------------------------------------------------------


# INTERFAZ PARA EMPLEADOS Y ADMINISTRADORES
#-----------------------------------------------------------------------------------------------------------------------------------------
class MenuGeneral(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=250, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Cerrar sesión' ,
                        command=lambda : self.interfaz.mostrar_frame(InicioSesion) ,
                        width=100 ).place( x=10 , y=10 )
        
        titulo = ctk.CTkLabel( self , text='Menú principal' )
        titulo.pack( pady=(50,20) )
        
            #gestion bicicletas
        opciones_gb = { 'Registrar compra'       : Compra, 
                        'Resgistrar venta'       : Venta,
                        'Registrar alquiler'     : Alquiler,
                        'Administrar alquileres' : AdmAlquiler,
                        'Reparaciones'           : Reparacion }
        menu_gb = ctk.CTkOptionMenu(    self , width=185,
                                        values=list(opciones_gb.keys()) , 
                                        command=lambda opcion : self.interfaz.mostrar_frame(opciones_gb[opcion], self.activeUser) )
        menu_gb.set('Gestión de bicicletas')
        
            # gestion usuarios
        opciones_gu = { 'Crear usuario'                            : CrearUsuario, 
                        'Listado de clientes'                      : ListClientes, 
                        'Historial según el cliente'               : HistClientes }
        menu_gu = ctk.CTkOptionMenu(    self , width=185,
                                        values=list(opciones_gu.keys()) ,
                                        command=lambda opcion : self.interfaz.mostrar_frame(opciones_gu[opcion], self.activeUser) )
        menu_gu.set('Gestión de usuarios')
        
            #estadisticas
        opciones_est = {'Porcentaje de alquileres por categoría en una fecha'   : AlqXCateg,
                        'Porcentaje de reparaciones por categoría en una fecha' : RepXCateg, 
                        'Balance del día'                                       : Balance }
        menu_est = ctk.CTkOptionMenu(   self , width=185,
                                        values=list(opciones_est.keys()) ,
                                        command=lambda opcion : self.interfaz.mostrar_frame(opciones_est[opcion], self.activeUser) )
        menu_est.set('Estadísticas del negocio')
        
            #analisis del mercado
        opciones_an = { 'Análisis por comunas' : AnXComuna,
                        'Análisis por género'  : AnXGenero,
                        'Análisis por edad'    : AnXEdad,
                        'Análisis por hora'    : AnXHora }
        menu_an = ctk.CTkOptionMenu(    self , width=185,
                                        values=list(opciones_an.keys()) ,
                                        command=lambda opcion : self.interfaz.mostrar_frame(opciones_an[opcion], self.activeUser) )
        menu_an.set('Análisis de mercado')
            
        if isinstance( self.activeUser , Administrador ) :
            self.height += 100
            pack(menu_gb , menu_gu , menu_est , menu_an)
        else :
            menu_gb.configure( values = list(opciones_gb.keys())[2:] )
            pack(menu_gb , menu_gu )
 
            
# GESTION DE BICICLETAS
class Compra(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Administrador):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=400, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        if not hasattr(self, 'mensaje') :
            ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
            
            self.mensaje = ctk.CTkLabel(self, text='Ingrese los datos de la bicicleta', text_color='white')
            self.mensaje.pack(pady=(60,0))
        
        self.marca  = ctk.CTkEntry( self , placeholder_text='Ingrese la marca' , width=250 )
        self.color  = ctk.CTkEntry( self , placeholder_text='Ingrese el color' , width=250 )
        self.precio = ctk.CTkEntry( self , placeholder_text='Ingrese el precio' , width=250 )
        
        self.estado = ctk.CTkEntry( self , placeholder_text='Ingrese el estado (1-10)' , width=250 )
        
        self.categoria = ctk.CTkOptionMenu( self , values= ['Carrera' , 'Ciudad' , 'Playera']  )
        self.categoria.set( 'Seleccione una categoria' )
        
        self.comprar = ctk.CTkButton( self , text='Comprar' , command = self.validar_compra )
        
        pack(self.marca, self.color, self.precio, self.estado, self.categoria, self.comprar)
        
    def validar_compra(self):
        try :
            if (self.marca.get()+self.color.get()).isalpha() and self.estado.get().isnumeric() and 0 < int(self.estado.get()) < 11 and self.categoria.get() != 'Seleccione una categoria' :
                
                categoria_class_map = { 'Carrera' : Carrera , 
                                        'Ciudad'  : Ciudad ,
                                        'Playera' : Playera }
                
                bicicleta = categoria_class_map[self.categoria.get()](  id = self.bicicleteria.generar_id() , 
                                                                        marca = self.marca.get() , 
                                                                        color = self.color.get() , 
                                                                        precioCompra = float(self.precio.get()) , 
                                                                        estado = int(self.estado.get()) )
                
                mensaje = self.activeUser.comprar(bicicleta)
                self.mensaje.configure( text_color='white', text = mensaje)
                pack_forget(self.marca, self.color, self.precio, self.estado, self.categoria, self.comprar)
                self.crear_widgets()
            else : 
                raise ValueError
        except ValueError :
            self.mensaje.configure( text_color='red', text = 
'''Los datos ingresados no son válidos.
Intente nuevamente''' )
        
                
class Venta(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=510, 
                            activeUser=activeUser)
    
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel( self , text=                              
'''Seleccione una categoria''' )
        
        self.mensaje.pack(pady=(50,10))
        
        self.muestreo = Muestreo(self)
        self.categoria = ctk.CTkOptionMenu( self , 
                                            values= ['Carrera' , 'Ciudad' , 'Playera'] , 
                                            command= lambda categoria : self.muestreo.muestreo_admin(categoria , accion='vender') )
        self.categoria.set( 'Categoria' )
        self.categoria.pack(pady=10)
        
    def validar_venta(self, bicicleta : Bicicleta) :
        self.confirmacion = ctk.CTkToplevel(self)
        self.confirmacion.title('Confirmación de venta')
        self.confirmacion.geometry('300x173')
        self.confirmacion.columnconfigure((0,1), weight=1)
        
        ctk.CTkLabel(   self.confirmacion, 
                        text=str(bicicleta)
                        ).grid(row=0, columnspan=2, pady=(10,20))
        
        ctk.CTkButton(  self.confirmacion, 
                            text='Confirmar venta',
                            command=lambda : self.vender(bicicleta),
                            height=35
                            ).grid(row=1, column=0, padx=12, sticky='EW')
        
        ctk.CTkButton(  self.confirmacion, 
                            text='Cancelar',
                            command=self.confirmacion.destroy,
                            height=35
                            ).grid(row=1, column=1, padx=12, sticky='EW')
        
        self.confirmacion.grab_set()
        
    def vender(self, bicicleta : Bicicleta) :
        self.confirmacion.destroy()
        self.activeUser.vender(bicicleta)
        self.interfaz.mostrar_frame(Venta, self.activeUser)
        
        
class Alquiler(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=600, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel( self ,text_color='white', text='Ingrese los siguientes datos')
        
        self.mensaje.pack(pady=(50,10))
        
        self.id_cliente = ctk.CTkEntry( self , placeholder_text="ID del cliente" , width=200 )
        
        self.dias = ctk.CTkEntry( self , placeholder_text="Cantidad de días" , width=200 )
        
        self.muestreo = Muestreo(self)
        self.categoria = ctk.CTkOptionMenu( self , 
                                            values= ['Carrera' , 'Ciudad' , 'Playera'] , 
                                            command= lambda categoria : self.muestreo.muestreo_admin(categoria , accion='alquilar') )
        self.categoria.set( 'Categoria' )
        
        
        pack(self.id_cliente, self.dias, self.categoria)
        
    def validar_alquiler(self, bicicleta : Bicicleta) :
        dias = self.dias.get()
        id_cliente = self.id_cliente.get()
        info_cliente = self.bicicleteria.usuarios.get( id_cliente )
        
        if dias.isnumeric() and int(dias) > 0 and info_cliente is not None :
            self.confirmacion = ctk.CTkToplevel(self)
            self.confirmacion.title('Confirmación de alquiler')
            self.confirmacion.geometry('300x140')
            self.confirmacion.columnconfigure((0,1), weight=1)
            
            monto = self.bicicleteria.calcular_monto(bicicleta, int(dias))
            ctk.CTkLabel(   self.confirmacion, 
                            text=f'Información del alquiler\n\nDuracion: {dias} días\nMonto: ${monto}'
                            ).grid(row=0, columnspan=2, pady=(10,20))
            
            ctk.CTkButton(  self.confirmacion, 
                                text='Confirmar alquiler',
                                command=lambda : self.alquilar(id_cliente, bicicleta, int(dias) ) ,
                                height=35
                                ).grid(row=1, column=0, padx=12, sticky='EW')
            
            ctk.CTkButton(  self.confirmacion, 
                                text='Cancelar',
                                command=self.confirmacion.destroy,
                                height=35
                                ).grid(row=1, column=1, padx=12, sticky='EW')
            
            self.confirmacion.grab_set()
        else :
            self.mensaje.configure( text_color='red', 
                                    text = 
'''Los datos ingresados no son válidos.
Intente nuevamente''' )
            
    def alquilar(self, id_cliente : str, bicicleta : Bicicleta, dias : int) :
        self.confirmacion.destroy()
        self.activeUser.alquilar( id_cliente , bicicleta , dias )
        self.interfaz.mostrar_frame(Alquiler, self.activeUser)
        
        
class AdmAlquiler(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            activeUser=activeUser)
        
        self.height += 80
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel(self, 
                                    text_color='white',
                                    text='Ingrese el ID del cliente para\nadministrar sus alquileres')
        self.mensaje.pack(pady=(50,10))
        
        self.id_cliente = ctk.CTkEntry( self , placeholder_text="ID del cliente" , width=200 )
        self.id_cliente.bind('<Return>', command=self.muestreo)
        
        pack(self.id_cliente, ctk.CTkButton(self, 
                                            text='Buscar alquileres',
                                            command=self.muestreo))
        
    def muestreo(self, event=None) :
        id_cliente = self.id_cliente.get()
        info_cliente = self.bicicleteria.usuarios.get( id_cliente )
        
        if info_cliente is not None :
            self.cliente = Cliente(id_cliente,info_cliente[0],info_cliente[1],self.bicicleteria,info_cliente[2])
           
            self.mensaje.configure(text_color='white',
                                   text=f'Alquileres del cliente\n{self.cliente.nombre}')
        
            if hasattr(self, 'muestra') :
                pack_forget(self.muestra)
                
            bicicletas = self.cliente.bicis_en_alquiler()
            
            self.muestra = Muestreo(self)
            self.muestra.muestreo_menu_clientes(bicicletas)
            
        else :
            self.mensaje.configure(text_color='red',
                                   text='El ID de cliente ingresado no existe.\nIntente nuevamente')
            
    def devolver_extender( self , bicicleta : Bicicleta , extender : bool ) :
        if not extender :
            self.activeUser.devolucion_extension(self.cliente.id, bicicleta , extender)
            self.interfaz.mostrar_frame(type(self), self.activeUser)
        else :
            while True :
                self.dias = ctk.CTkInputDialog( title='Extensión de alquiler' ,
                                                text='Ingrese la cantidad de días a extender' )
                dias = self.dias.get_input()
                if dias is None :
                    break
                if dias.isnumeric() and dias != '0' :
                    self.activeUser.devolucion_extension( self.cliente.id , bicicleta , extender , int(dias) )
                    break
        
       
class Reparacion(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=150, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        self.boton_menu = ctk.CTkButton(self , 
                                        text='Menú principal' ,
                                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                                        width=100 )
        self.boton_menu.place( x=10 , y=10 )
        
        if isinstance(self.activeUser, Administrador) :
            ctk.CTkButton(  self, 
                            text='Reparar bicicleta del stock',
                            command=self.propia
                            ).pack(pady=(70,10))
            
            ctk.CTkButton( self, 
                            text='Reparar bicicleta ajena',
                            command=self.ajena
                            ).pack()
            
        else :
            self.ajena()
    
       
    def propia(self) :
        pack_forget(self.pack_slaves())
        self.height = 470
        self.boton_menu.place_forget()
        
        ctk.CTkButton(  self , 
                        text='Volver' ,
                        command=lambda : self.interfaz.mostrar_frame(Reparacion, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        if not hasattr(self, 'texto') :
            self.texto = 'Seleccione una categoria'
        self.mensaje = ctk.CTkLabel( self , text=self.texto)
        self.mensaje.pack(pady=(50,10))
        
        self.muestreo = Muestreo(self)
        self.categoria = ctk.CTkOptionMenu( self , 
                                            values= ['Carrera' , 'Ciudad' , 'Playera'] , 
                                            command= lambda categoria : self.muestreo.muestreo_admin(categoria , accion='reparar') )
        self.categoria.set( 'Categoria' )
        
        self.categoria.pack()
    
    def validar_reparacion(self, bicicleta : Bicicleta) :
        self.confirmacion = ctk.CTkToplevel(self)
        self.confirmacion.title('Confirmación de reparación')
        self.confirmacion.geometry('340x108')
        self.confirmacion.columnconfigure((0,1), weight=1)
        
        duracion = 9 - bicicleta.estado
        
        costo = type(bicicleta).precio_alq * duracion
         
        ctk.CTkLabel(   self.confirmacion, 
                        text=f"Duración de la reparación: {duracion} {'días' if duracion>1 else 'día'}\nMonto: ${costo}"
                        ).grid(row=0, columnspan=2, pady=(10,20))
        
        ctk.CTkButton(  self.confirmacion, 
                            text='Confirmar reparación',
                            command=lambda : self.reparar(bicicleta),
                            height=35
                            ).grid(row=1, column=0, padx=12, sticky='EW')
        
        ctk.CTkButton(  self.confirmacion, 
                            text='Cancelar',
                            command=self.confirmacion.destroy,
                            height=35
                            ).grid(row=1, column=1, padx=12, sticky='EW')
        
        self.confirmacion.grab_set()
        
    def reparar(self, bicicleta : Bicicleta) :
        self.confirmacion.destroy()
        self.texto = self.activeUser.reparacion(bicicleta)
        self.propia()
    

    def ajena(self) :
        pack_forget(self.pack_slaves())
        self.height = 440
        self.boton_menu.place_forget()
        if isinstance(self.activeUser, Administrador) :
            ctk.CTkButton(  self , 
                            text='Volver' ,
                            command=lambda : self.interfaz.mostrar_frame(Reparacion, self.activeUser) ,
                            width=100 ).place( x=10 , y=10 )
        else :
            self.boton_menu.place( x=10 , y=10 )
        
        if not hasattr(self, 'texto') :
            self.texto = 'Ingrese los siguientes datos'
        self.mensaje = ctk.CTkLabel( self , text_color='white',text=self.texto)
        self.mensaje.pack(pady=(50,10))

        self.id_cliente = ctk.CTkEntry( self , placeholder_text='ID del cliente' , width=250 )
        
        self.marca  = ctk.CTkEntry( self , placeholder_text='Marca' , width=250 )
        self.color  = ctk.CTkEntry( self , placeholder_text='Color' , width=250 )
        self.precio = ctk.CTkEntry( self , placeholder_text='Precio' , width=250 )
        
        self.estado = ctk.CTkEntry( self , placeholder_text='Estado (1-10)' , width=250 )
        
        self.categoria = ctk.CTkOptionMenu( self , values= ['Carrera' , 'Ciudad' , 'Playera']  )
        self.categoria.set( 'Categoria' )
        
        self.confirmar = ctk.CTkButton( self , text='Reparar' , command = self.validar_datos )
        
        pack(self.id_cliente, self.marca, self.color, self.precio, self.estado, self.categoria, self.confirmar)
        
    def validar_datos(self):
        try :
            id_cliente = self.id_cliente.get()
            info_cliente = self.bicicleteria.usuarios.get(id_cliente )
            
            if (self.marca.get()+self.color.get()).isalpha() and self.estado.get().isnumeric() and 0 < int(self.estado.get()) < 11 and self.categoria.get() != 'Categoria' and info_cliente is not None  :
                
                categoria_class_map = { 'Carrera' : Carrera , 
                                        'Ciudad'  : Ciudad ,
                                        'Playera' : Playera }
                
                bicicleta = categoria_class_map[self.categoria.get()](  id = self.bicicleteria.generar_id() , 
                                                                        marca = self.marca.get() , 
                                                                        color = self.color.get() , 
                                                                        precioCompra = float(self.precio.get()) , 
                                                                        estado = int(self.estado.get()) )
                
                self.texto = self.activeUser.reparacion(bicicleta, id_cliente)
                
                pack_forget(self.id_cliente, self.marca, self.color, self.precio, self.estado, self.categoria, self.confirmar)
                self.ajena()
            else : 
                raise ValueError
        except ValueError :
            self.mensaje.configure( text_color='red', text = 
'''Los datos ingresados no son válidos.
Intente nuevamente''' ) 
     
        
# GESTION DE USUARIOS
class CrearUsuario(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=400, 
                            height=350, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        pack_forget(self.pack_slaves())
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        if not hasattr(self, 'mensaje') :
            self.mensaje = ctk.CTkLabel(self, text_color='white' ,
                                        text = f"Ingrese los datos del {'cliente' if isinstance( self.activeUser , Empleado ) else 'usuario'} a registrar" ) 
        self.mensaje.pack(pady=(50,10))
        
        self.nombre = ctk.CTkEntry( self , placeholder_text="Nombre completo" , width=300 )
        self.id_usuario = ctk.CTkEntry( self , placeholder_text="Nombre de usuario" , width=300 )
        self.contrasena = ctk.CTkEntry( self , placeholder_text="Contraseña" , width=300 )

        self.rol = ctk.CTkOptionMenu( self , values=['Administrador' , 'Empleado' , 'Cliente'] )
        self.rol.set('Rol')
           
        self.crear = ctk.CTkButton( self , 
                                    text = 'Crear usuario' , 
                                    command=self.validar_datos_usuario )
        if isinstance(self.activeUser, Administrador) :
            pack(self.nombre, self.id_usuario, self.contrasena, self.rol, self.crear)
        else :
            self.height -= 50
            self.rol.set('Cliente')
            pack(self.nombre, self.id_usuario, self.contrasena, self.crear)
        
            
    def validar_datos_usuario(self) :
        id_usuario = self.id_usuario.get()
        contrasena = self.contrasena.get()
        nombre = self.nombre.get()
        rol = self.rol.get()
        
        if not any([ char.isalpha() for char in id_usuario ]) or not contrasena or not all([ char.isalpha() or char.isspace() for char in nombre ]) or rol == 'Rol' : # validacion de strings
            self.mensaje.configure(text_color='red',
                                   text='Los datos ingresados no son válidos.\nIntente nuevamente')
            
        elif self.bicicleteria.usuarios.get(id_usuario) is not None : # validacion de unicidad del id del usuario
            self.mensaje.configure(text_color='red', 
                                   text='El nombre de usuario ingresado ya existe.\nIntente nuevamente')
            
        else :
            rol_class_map = {
                'Administrador' : Administrador ,
                'Empleado'      : Empleado ,
                'Cliente'       : Cliente
            }
            
            usuario = rol_class_map[rol](id_usuario,
                                            nombre,
                                            contrasena,
                                            self.bicicleteria)
            
            self.activeUser.registrar_usuario(usuario)
            self.mensaje.configure(text=f'El usuario {nombre}\nfue creado con éxito.' ,
                                   text_color='white')
            
    
class ListClientes(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=400, 
                            height=350, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        mensaje = ctk.CTkLabel(self, text='Listado de clientes')
        
        frame_clientes = ctk.CTkScrollableFrame(self, width=300, height=250)
        
        clientes = self.bicicleteria.listar_clientes()
        
        if clientes is None :
            mensaje.configure(text='No hay clientes registrados')
        else :
            while not clientes.is_empty() :
                cliente = clientes.pop()
                cliente = Cliente(
                    id=cliente[0] ,
                    nombre=cliente[1][0] ,
                    contrasena=cliente[1][1] ,
                    bicicleteria=self.bicicleteria ,
                    fecha_registro=cliente[1][3]
                )
                
                ctk.CTkLabel(frame_clientes, text=cliente).pack(pady=10)
            
        pack(mensaje, frame_clientes)
        
        
class HistClientes(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=250, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel(self, 
                                    text_color='white',
                                    text='Ingrese el ID del cliente para\nvisualizar su historial')
        self.mensaje.pack(pady=(50,10))
        
        self.id_cliente = ctk.CTkEntry( self , placeholder_text="ID del cliente" , width=200 )
        self.id_cliente.bind('<Return>', command=self.muestreo)
        
        pack(self.id_cliente, ctk.CTkButton(self, 
                                            text='Buscar historial',
                                            command=self.muestreo))
        
    def muestreo(self, event=None) :
        if hasattr(self, 'frame_historial') :
            self.frame_historial.destroy()
        hist_alquileres, hist_reparaciones = self.bicicleteria.listar_historial( self.id_cliente.get() )
        
        if hist_alquileres.is_empty() and hist_reparaciones.is_empty() :
            self.mensaje.configure(text='No hay registros con el ID ingresado')
        else :
            self.width = 600
            self.height = 500
            self.mensaje.configure(text='Historial del cliente')
            
            self.frame_historial = ctk.CTkFrame(self, width=500, height=700)
            self.frame_historial.pack(pady=20, padx=50,)
            self.frame_historial.grid_columnconfigure(1, weight=1)
            
            
            ctk.CTkLabel(self.frame_historial,
                         text='Alquileres').grid(column=0,row=0, pady=10)
            
            ctk.CTkLabel(self.frame_historial,
                         text='Reparaciones').grid(column=1,row=0, pady=10)
            
            self.alquileres = ctk.CTkScrollableFrame(self.frame_historial, width=200)
            while not hist_alquileres.is_empty() :
                
                alquiler = hist_alquileres.pop()
                
                pack(ctk.CTkLabel(self.alquileres,
                                    text=f"ID: {alquiler['id']}\nMarca: {alquiler['marca']}\nColor: {alquiler['color']}\nCategoria: {alquiler['categoria']}\nFecha de inicio: {alquiler['fecha_inicio']}\nFecha de fin: {alquiler['fecha_fin']}\nMonto: {alquiler['monto']}"))
            
            self.reparaciones = ctk.CTkScrollableFrame(self.frame_historial, width=200)
            while not hist_reparaciones.is_empty() :
                
                reparacion = hist_reparaciones.pop()
                
                pack(ctk.CTkLabel(self.reparaciones,
                                    text=f"ID: {reparacion['id']}\nMarca: {reparacion['marca']}\nColor: {reparacion['color']}\nCategoria: {reparacion['categoria']}\nFecha de inicio: {reparacion['fecha_inicio']}\nFecha de fin: {reparacion['fecha_fin']}\nMonto: {reparacion['monto']}"))
            
            self.alquileres.grid(column=0,row=1, pady=10,padx=10,sticky='NSEW')
            
            self.reparaciones.grid(column=1,row=1, pady=10, padx=10, sticky='NSEW')
            
               
# ESTADISTICAS DEL NEGOCIO
class AlqXCateg(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=300, 
                            height=320, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        self.mensaje = ctk.CTkLabel( self , text='Ingrese la fecha que desea consultar' )
        self.mensaje.pack( pady=(50,10) )
        
        self.anno = ctk.CTkOptionMenu(  self , 
                                        values = list( map ( str , range( 2024 , datetime.now().year + 1 ) ) ) ,
                                        command = lambda anno : self.pedir_mes(anno) )
        self.anno.set( 'Seleccione un año' )
        self.anno.pack(pady=10)
    
        self.mes = ctk.CTkOptionMenu( self , state='disabled' )
        self.mes.set( 'Seleccione un mes' )
        self.mes.pack(pady=10)
        
        self.dia = ctk.CTkOptionMenu( self , state='disabled' )
        self.dia.set( 'Seleccione un día' )
        self.dia.pack(pady=10)
        
        self.consultar = ctk.CTkButton( self , 
                                        text='Consultar porcentajes'  , 
                                        command= lambda : self.validar_fecha( self.anno.get() , self.mes.get() , self.dia.get() ) ) 
        self.consultar.pack(pady=10)
        
    def pedir_mes( self , anno : str) :
        self.mes.configure( values = list( map( str , range(1,13) ) ) , 
                            state='normal' , 
                            command = lambda mes : self.pedir_dia( anno , mes ) )
        self.mes.set( 'Seleccione un mes' )
        
    def pedir_dia( self , anno : str , mes : str ) :
        self.dia.configure( state = 'normal' ,
                            values = list( map( str , range( 1 , monthrange( int(anno) , int(mes) )[1] + 1 ) ) ))
        self.dia.set( 'Seleccione un día' )
        self.dia.pack( pady=10 )
    
    def validar_fecha( self , anno : str , mes : str , dia : str ) :
        if (anno + mes + dia).isnumeric() :
            fecha = date( int(anno) , int(mes) , int(dia) )
            alq_X_categoria = self.bicicleteria.listar_porcentaje(fecha, 0)
            
            self.porcentaje(fecha, alq_X_categoria, 'alquileres')
        else :
            self.mensaje.configure( text='Debe ingresar todos los datos\nde la fecha para continuar' )
       
    def porcentaje(self, fecha : date, cant_X_categoria : dict, tipo : str ) :
        if cant_X_categoria is None :
            self.mensaje.configure(text=f'No se registraron {tipo}\nen la fecha ingresada')
        else :
            pack_forget(self.mensaje, self.anno, self.mes, self.dia, self.consultar)
            self.width = 540
            self.height = 400
            self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
            self.plot_frame.pack(pady=(50,10))

            fig = graficos( 'pie' , cant_X_categoria , f'Porcentaje de {tipo} por categoría del día\n{fecha}' )
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(padx=10,pady=10)
        

class RepXCateg(AlqXCateg) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            activeUser=activeUser)
    
    def validar_fecha( self , anno : str , mes : str , dia : str ) :
        if (anno + mes + dia).isnumeric() :
            fecha = date( int(anno) , int(mes) , int(dia) )
            rep_X_categoria = self.bicicleteria.listar_porcentaje(fecha, 1)
            
            self.porcentaje(fecha, rep_X_categoria, 'reparaciones')
        else :
            self.mensaje.configure( text='Debe ingresar todos los datos\nde la fecha para continuar' )
    
 
class Balance(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=1200, 
                            height=500, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        self.frame_balance = ctk.CTkFrame(self)
        self.frame_balance.grid_columnconfigure((0,1,2,3), weight=1)
        self.frame_balance.pack(fill='both', pady=10)
        
        ctk.CTkButton(  self.frame_balance , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=15 , y=5 )
        
        
        compras, total_compras, ventas, total_ventas, alquileres, total_alquileres, reparaciones, total_reparaciones, monto_caja = self.bicicleteria.listar_balance()
        
        ctk.CTkLabel(self.frame_balance, text=f'Balance del día\nMonto de caja actual: {monto_caja}').grid(columnspan=4, row=0)
        
        self.compras = ctk.CTkScrollableFrame( self.frame_balance , width=250 , height=300 , label_text='Compras del día'  )
        self.compras.grid(row=1, column=0, pady=5)
        self.total_compras = ctk.CTkLabel( self.frame_balance , text = f"Total compras del día ${total_compras}" )
        self.total_compras.grid(row=2, column=0, pady=5)
        
        self.ventas = ctk.CTkScrollableFrame( self.frame_balance , width=250 , height=300 , label_text='Ventas del día')
        self.ventas.grid(row=1, column=1, pady=5)
        self.total_ventas = ctk.CTkLabel( self.frame_balance , text = f"Total ventas del día ${total_ventas}" )
        self.total_ventas.grid(row=2, column=1, pady=5)
        
        self.alquileres = ctk.CTkScrollableFrame( self.frame_balance , width=250 , height=300 , label_text='Alquileres del día' )
        self.alquileres.grid(row=1, column=2, pady=5)
        self.total_alquileres = ctk.CTkLabel( self.frame_balance , text = f"Total alquileres del día ${total_alquileres}" )
        self.total_alquileres.grid(row=2, column=2, pady=5)
        
        self.reparaciones = ctk.CTkScrollableFrame( self.frame_balance , width=250 , height=300 , label_text='Reparaciones del día' )
        self.reparaciones.grid(row=1, column=3, pady=5)
        self.total_reparaciones = ctk.CTkLabel( self.frame_balance , text = f"Total alquileres del día ${total_reparaciones}" )
        self.total_reparaciones.grid(row=2, column=3, pady=5)

        if not compras.is_empty() :
            while True :
                if compras.is_empty() :
                    break
                compra = compras.pop()
                self.compra = ctk.CTkLabel( self.compras , 
                                            text= f"Fecha: {compra[2]}\nID bicicleta: {compra[0]}\nMonto: ${compra[3]}" )
                self.compra.pack( pady=10  )
                
        if not ventas.is_empty() :
            while True :
                if ventas.is_empty() :
                    break
                venta = ventas.pop()
                self.venta = ctk.CTkLabel(  self.ventas , 
                                            text= f"Fecha: {venta[2]}\nID bicicleta: {venta[0]}\nMonto: ${venta[3]}" )
                self.venta.pack( pady=10  )
                
        if not alquileres.is_empty() :
            while True :
                if alquileres.is_empty() :
                    break
                alquiler = alquileres.pop()
                self.alquiler = ctk.CTkLabel(   self.alquileres , 
                                                text= f"Fecha de inicio: {alquiler[2]}\nFecha de fin: {alquiler[3]}\nID bicicleta: {alquiler[0]}\nID cliente: {alquiler[1]}\nMonto: ${alquiler[4]}" )
                self.alquiler.pack( pady=10  )
            
        while not reparaciones.is_empty() :
            reparacion = reparaciones.pop()
            
            bicicleta = reparacion[1]['bicicleta']
            if isinstance(bicicleta, Bicicleta) :
                bicicleta = bicicleta.id
                
            self.reparacion = ctk.CTkLabel(   self.reparaciones , 
                                            text= f"Fecha de inicio: {reparacion[0]}\nFecha de fin: {reparacion[1]['fecha_fin']}\nID bicicleta: {bicicleta}\nID cliente: {reparacion[1]['cliente']}\nMonto: ${reparacion[1]['monto']}" )
            self.reparacion.pack( pady=10  )

        self.total_balance = ctk.CTkLabel(  self.frame_balance , 
                                            text = f"Balance total del día ${round(total_ventas+total_alquileres+total_reparaciones-total_compras , 2)}" )
        self.total_balance.grid(row=3,columnspan=4, pady=5)


# ANALISIS DEL MERCADO
class AnXComuna(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=700, 
                            height=600, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        dict_comunas , mejores_comunas = analisis_por_comuna()
        
        if dict_comunas is not None :
            analisis = f'Las comunas a invertir son:\nComuna {mejores_comunas[0][0]}\nComuna {mejores_comunas[1][0]}\nComuna {mejores_comunas[2][0]}'
            
            self.analisis = ctk.CTkLabel(self, text=analisis )
            self.analisis.pack( pady=(60,10) )

            self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
            self.plot_frame.pack(expand=True)

            fig = graficos('bars', dict_comunas, 'Uso de bicicletas por comuna', 'Comunas', 'Uso de bicicletas')
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(padx=10,pady=10)
        
        else :
            self.width = 300
            self.height = 100
            
            ctk.CTkLabel(self, 
                         text='Para utilizar esta opción, debe ubicar\nel archivo "bicicletas.csv" correctamente.' 
                         ).pack( pady=(60,10) )
        

class AnXGenero(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=700, 
                            height=600, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        dict_genero , menos_uso = generos()
        
        if dict_genero is not None :
            analisis = f'Género que menos utiliza las bicicletas:\n{menos_uso}\n\nPara fomentar un mayor uso de las bicicletas\nal género {menos_uso.lower()} de la poblacion,\nse deberian otorgar descuentos a este grupo. '
            
            self.analisis = ctk.CTkLabel( self , text=analisis )
            self.analisis.pack( pady=(60,10) )
            
            self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
            self.plot_frame.pack(expand=True)

            fig = graficos('pie', dict_genero, 'Uso de bicicletas por genero')
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(padx=10,pady=10)
            
        else :
            self.width = 300
            self.height = 100
            
            ctk.CTkLabel(self, 
                         text='Para utilizar esta opción, debe ubicar\nel archivo "bicicletas.csv" correctamente.' 
                         ).pack( pady=(60,10) )
        

class AnXEdad(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=700, 
                            height=600, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        dict_edades , mejores_edades = usos_por_edad()
        
        if dict_edades is not None :
            analisis = f'Las edades que más demanda de bicicletas han tenido son:\n{mejores_edades[0][0]} con {mejores_edades[0][1]} usos\n{mejores_edades[1][0]} con {mejores_edades[1][1]} usos\n{mejores_edades[2][0]} con {mejores_edades[2][1]} usos\nSe recomienda realizar descuentos a estas edades'
            self.analisis = ctk.CTkLabel( self , text=analisis )
            self.analisis.pack( pady=(60,10) )
            
            self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
            self.plot_frame.pack(expand=True)

            fig = graficos( 'bars', dict_edades, 'Usos por edad ', 'Edades', 'Cantidad usada')
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(padx=10,pady=10)
            
        else :
            self.width = 300
            self.height = 100
            
            ctk.CTkLabel(self, 
                         text='Para utilizar esta opción, debe ubicar\nel archivo "bicicletas.csv" correctamente.' 
                         ).pack( pady=(60,10) )


class AnXHora(FrameObj) :
    
    def __init__(self, master : ctk.CTkFrame, interfaz : ctk.CTk, bicicleteria : Bicicleteria, activeUser : Usuario):
        super().__init__(   master=master, 
                            interfaz=interfaz, 
                            bicicleteria=bicicleteria, 
                            width=700, 
                            height=600, 
                            activeUser=activeUser)
        
    def crear_widgets(self):
        
        ctk.CTkButton(  self , 
                        text='Menú principal' ,
                        command=lambda : self.interfaz.mostrar_frame(MenuGeneral, self.activeUser) ,
                        width=100 ).place( x=10 , y=10 )
        
        dict_horas , mejores_horas = usos_por_hora()
        
        if dict_horas is not None :
            analisis = f'Las horas pico son:\n{mejores_horas[0]}\n{mejores_horas[1]}\n{mejores_horas[2]}\nSe recomienda aumentar la tarifa en estos horarios'
            self.analisis = ctk.CTkLabel( self , text=analisis )
            self.analisis.pack( pady=(60,10) )
            
            self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
            self.plot_frame.pack(expand=True)

            fig = graficos( 'plot', dict_horas, 'Usos por hora', 'Horas', 'Cantidad usada')
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(padx=10,pady=10)
            
        else :
            self.width = 300
            self.height = 100
            
            ctk.CTkLabel(self, 
                         text='Para utilizar esta opción, debe ubicar\nel archivo "bicicletas.csv" correctamente.' 
                         ).pack( pady=(60,10) )
#-----------------------------------------------------------------------------------------------------------------------------------------
 

# CLASE AUXILIAR PARA MUESTREOS  
class Muestreo(ctk.CTkScrollableFrame) :
    
    def __init__(self, master : ctk.CTkFrame) :
        super().__init__(master, height=240 , width=300)
        self.grid_columnconfigure(0, weight=1)
        self.master : FrameObj = master
        self.bicicleteria : Bicicleteria = self.master.bicicleteria
    
    def muestreo_alq_clientes(self, categoria : Literal['Playera','Ciudad','Carrera']) :
        pack_forget(self.pack_slaves())
        self.configure(width=200, height=300)
        self.pack(pady=(20,0))
        
        bicicletas = self.bicicleteria.muestreo_bicis( categoria , 'alquilar' )
        
        if bicicletas is None :
                self.master.mensaje.configure(text_color= 'white' , 
                                    text = 
'''No hay bicicletas disponibles para
la categoria seleccionada''' )
                
        else :
            
            self.master.mensaje.configure(  text = f'Haga click sobre la bicicleta\nque desea alquilar' ,
                                    text_color= 'white')
            
            while not bicicletas.is_empty() :
                bicicleta = bicicletas.pop()
                mostrar = ctk.CTkButton(    self , 
                                            text=str( bicicleta ) , 
                                            command=lambda : self.master.validar_alquiler(bicicleta) )
                mostrar.pack(pady=5)
        
    def muestreo_menu_clientes(self, bicicletas : ListaEnlazada) :
        self.pack(pady=(20,0))
        if bicicletas is None :
            pass
        else :
            fila = 0
            while True :
    
                frame_bici = ctk.CTkFrame(self, height=50, width = 200 )
                frame_bici.grid( row=fila , column=0 , pady=10 , padx=0 )
                frame_bici.grid_columnconfigure(1, weight=1)
                
                bicicleta = bicicletas.pop()
                
                label_bicicleta = ctk.CTkLabel( frame_bici , text=str(bicicleta) )
                label_bicicleta.grid(row=0 , column=0, padx=(0,10))
                
                self.acciones = ctk.CTkOptionMenu(  frame_bici ,
                                                    values=['Devolver bicicleta',
                                                            'Extender alquiler'] ,
                                                    width=60 )
                self.acciones.configure(command=self.devolver_extender(bicicleta, self.acciones))
                self.acciones.set('Acciones')
                self.acciones.grid(row=0, column=1, padx=(10,0))
                
                if not bicicletas.is_empty() :
                    linea = ctk.CTkFrame(self, height=2, width=200, bg_color='grey', fg_color='grey')
                    linea.grid(row=fila+1, column=0)
                else :
                    break
                
                fila += 2
                
    def devolver_extender(self, bicicleta : Bicicleta, widget : ctk.CTkOptionMenu) :
        
        def command(accion : Literal['Devolver bicicleta','Extender alquiler']) :
            widget.set('Acciones')
            self.master.devolver_extender( bicicleta, accion=='Extender alquiler' )

        return command    
    
    
    
    def muestreo_admin(self, categoria : str, accion : Literal['vender','alquilar','reparar']) :
        pack_forget(self.pack_slaves())
        self.configure(width=200, height=300)
        self.pack(pady=(20,0))
        
        bicicletas = self.bicicleteria.muestreo_bicis(categoria , accion )
        
        if bicicletas is None :
            self.master.mensaje.configure(  text_color='white',
                                            text = 
'''No hay bicicletas disponibles para
la categoria seleccionada''' )
            
        else :
            self.master.mensaje.configure(  text_color='white',
                                            text = 
'''Haga click sobre la bicicleta\nque desea {}'''.format(accion) )
            
            while not bicicletas.is_empty() :
                
                bicicleta = bicicletas.pop()
                mostrar = ctk.CTkButton(    self , 
                                            text=str( bicicleta ) , 
                                            command= self.seleccionar_bicicleta( bicicleta , accion ) )
                mostrar.pack(pady=5)
    
    def seleccionar_bicicleta(self , bicicleta : Bicicleta , accion : Literal['vender','alquilar','reparar'] ):
        
        def command():
            match accion :
                case 'vender' :
                    self.master.validar_venta(bicicleta)
                case 'alquilar' :
                    self.master.validar_alquiler(bicicleta)
                case'reparar' :
                    self.master.validar_reparacion(bicicleta)
        
        return command
