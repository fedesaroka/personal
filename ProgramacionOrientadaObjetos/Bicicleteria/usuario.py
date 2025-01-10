from datetime import datetime
from bicicleta import Bicicleta
from bicicleteria import Bicicleteria
from lista_enlazada import *
from auxiliares import d_to_str

class Usuario :
    '''
    Representacion de usuarios de bicicleterias en python.
    
    ATRIBUTOS DE INSTANCIA:
    - id: identificador unico que diferencia a todos los usuarios (str)
    - nombre: nombre completo del usuario (str)
    - contrasena: contraseña del usuario (str)
    - fecha_registro: fecha en la que el usuario fue registrado en la bicicleteria (str)
    - bicicleteria: bicicleteria en la que opera el usuario (Bicicleteria)
    '''
    def __init__(   self , 
                    id : str , 
                    nombre : str , 
                    contrasena : str , 
                    fecha_registro : str ,
                    bicicleteria : Bicicleteria ):
        
        self.nombre = nombre
        self.contrasena = contrasena
        self.fecha_registro = fecha_registro
        self.id = id
        self.bicicleteria = bicicleteria

    def __eq__( self , other ) :
        return self.id == other.id
    
    def __str__(self):
        return f'Nombre: {self.nombre}\nIdentificador: {self.id}\nFecha de registro: {self.fecha_registro}'
    
    def alquilar( self , id_cliente : str , bicicleta : Bicicleta , dias : int ) :
        '''
        Metodo para alquilar una bicicleta
        (solamente se puede ejecutar cuando el activeUser de la interfaz no es un cliente)
        '''
        self.bicicleteria.alquilar_bicicleta( id_cliente , bicicleta , dias )
        
    def devolucion_extension( self , id_cliente : str , bicicleta : Bicicleta , extender : bool , dias : int = 1) :
        '''
        Metodo para recibir una bicicleta o extender un alquiler
        (solamente se puede ejecutar cuando el activeUser de la interfaz no es un cliente)
        '''
        self.bicicleteria.devolucion_extension( id_cliente, bicicleta , extender , dias )
    
    def reparacion( self , bicicleta : Bicicleta, id_cliente : str | None = None ) :
        '''
        Metodo para ingresar una bicicleta al taller de reparaciones.
        Los empleados solo pueden reparar bicicletas ajenas. Esto se debe a que las 
        bicicletas del stock de la propia bicicleteria se reparan sistematicamente 
        cuando su estado es menor o igual a 4. Es posible que una bicicleta 
        con estado mayor que 4 sea reparada, pero tiene que ser por decision 
        de un administrador dado que cada reparacion implica un gasto y 
        las decisiones sobre gastos las toman los administradores.
        '''
        en_stock : bool = self.bicicleteria.stock.get(bicicleta.id) is not None
        
        if en_stock :
            return 'Solo los administradores pueden ingresar\nbicicletas del stock al taller de reparaciones.'
        
        self.bicicleteria.registrar_bicicleta(bicicleta)
        
        return self.bicicleteria.reparacion( bicicleta, en_stock, id_cliente )


class Administrador(Usuario):
    '''
    Representacion de administradores de bicicleterias en python.
    
    ATRIBUTOS DE INSTANCIA:
    - id: identificador unico que diferencia a todos los usuarios (str)
    - nombre: nombre completo del usuario (str)
    - contrasena: contraseña del usuario (str)
    - fecha_registro: fecha en la que el usuario fue registrado en la bicicleteria (str)
    - bicicleteria: bicicleteria en la que opera el usuario (Bicicleteria)
    '''
    def __init__(   self , 
                    id : str , 
                    nombre : str , 
                    contrasena : str , 
                    bicicleteria : Bicicleteria ,
                    fecha_registro : str = d_to_str(datetime.now().date()) ) :
        
        super().__init__( id , nombre , contrasena , fecha_registro, bicicleteria )
        
    def comprar( self , bicicleta : Bicicleta ) :
        '''
        Metodo para comprar una bicicleta y archivarla en 
        el historial de bicicletas de la bicicleteria
        '''   
        self.bicicleteria.registrar_bicicleta(bicicleta)
        return self.bicicleteria.comprar_bicicleta( bicicleta )
        
    def vender( self , bicicleta : Bicicleta ) :
        '''
        Metodo para vender una bicicleta
        '''
        self.bicicleteria.vender_bicicleta( bicicleta )
    
    def reparacion( self, bicicleta : Bicicleta, id_cliente = None ) :
        '''
        Metodo para ingresar una bicicleta al taller de reparaciones.
        Los administradores pueden reparar tanto bicicletas ajenas como 
        bicicletas del stock de la propia bicicleteria. Si la bicicleta
        no pertenece al stock de la bicicleteria, debe ser archivada
        en el historial de bicicletas de la bicicleteria.
        '''
        en_stock : bool = self.bicicleteria.stock.get(bicicleta.id) is not None
        
        if not en_stock :
            self.bicicleteria.registrar_bicicleta(bicicleta)
        
        return self.bicicleteria.reparacion(bicicleta, en_stock, id_cliente)
        
    def registrar_usuario( self , usuario : Usuario ) :
        '''
        Metodo para registrar un usuario en la bicicleteria.
        Los administradores pueden registrar cualquier tipo
        de usuario.
        '''
        self.bicicleteria.registrar_usuario(
            usuario.id, 
            usuario.nombre, 
            usuario.contrasena, 
            type(usuario).__name__, 
            usuario.fecha_registro 
        )

        
class Empleado(Usuario):
    '''
    Representacion de empleados de bicicleterias en python.
    
    ATRIBUTOS DE INSTANCIA:
    - id: identificador unico que diferencia a todos los usuarios (str)
    - nombre: nombre completo del usuario (str)
    - contrasena: contraseña del usuario (str)
    - fecha_registro: fecha en la que el usuario fue registrado en la bicicleteria (str)
    - bicicleteria: bicicleteria en la que opera el usuario (Bicicleteria)
    '''
    def __init__(   self , 
                    id : str , 
                    nombre : str , 
                    contrasena : str , 
                    bicicleteria : Bicicleteria ,
                    fecha_registro : str = d_to_str(datetime.now().date()) ) :
        
        super().__init__( id , nombre , contrasena , fecha_registro, bicicleteria )
    
    def registrar_usuario( self, usuario : Usuario ) :
        '''
        Metodo para registrar un usuario en la bicicleteria.
        Los empleados solo pueden registrar usuarios del tipo "Cliente".
        '''
        self.bicicleteria.registrar_usuario(
            usuario.id, 
            usuario.nombre, 
            usuario.contrasena, 
            'Cliente', 
            usuario.fecha_registro 
        )
        
     
class Cliente(Usuario) :
    '''
    Representacion de clientes de bicicleterias en python.
    
    ATRIBUTOS DE INSTANCIA:
    - id: identificador unico que diferencia a todos los usuarios (str)
    - nombre: nombre completo del usuario (str)
    - contrasena: contraseña del usuario (str)
    - fecha_registro: fecha en la que el usuario fue registrado en la bicicleteria (str)
    - bicicleteria: bicicleteria en la que opera el usuario (Bicicleteria)
    '''
    def __init__(   self , 
                    id : str , 
                    nombre : str , 
                    contrasena : str , 
                    bicicleteria : Bicicleteria ,
                    fecha_registro : str = d_to_str(datetime.now().date()) ) :
        
        super().__init__( id , nombre , contrasena , fecha_registro, bicicleteria )
    
    def alquilar(self, bicicleta : Bicicleta, dias : int ) :
        '''
        Metodo para alquilar una bicicleta
        '''
        self.bicicleteria.alquilar_bicicleta( self.id , bicicleta , dias )

    def devolucion_extension( self, bicicleta : Bicicleta , extender : bool , dias : int = 1 ) :
        '''
        Metodo para devolver una bicicleta o extender un alquiler
        '''
        self.bicicleteria.devolucion_extension( self.id, bicicleta , extender , dias )

    def bicis_en_alquiler(self) :
        '''
        Metodo que recibe el id de un cliente y devuelve una lista enlazada 
        con todas las bicicletas que tiene en alquiler.
        '''
        stock : dict = self.bicicleteria.stock
        
        alquileres = self.bicicleteria.alquileres
        mask = (alquileres[:,1] == self.id) & (alquileres[:,4] == '')    # mascara utilizada para filtrar los alquileres que no son del cliente o que ya hayan finalizado
        
        bicicletas = ListaEnlazada()
        
        for alquiler in alquileres[mask] :
            bicicletas.add_to_end(stock[ int(alquiler[0]) ])
            
        if bicicletas.is_empty() :
            return None
        return bicicletas
