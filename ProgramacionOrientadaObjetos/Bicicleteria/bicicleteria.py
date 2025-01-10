import numpy as np
from auxiliares import dt_to_str, str_to_dt, d_to_str, str_to_d, crear_archivo
from bicicleta import Bicicleta, Playera, Carrera, Ciudad
from taller import Taller
from collections import defaultdict
from lista_enlazada import *
import csv
from typing import Literal, ValuesView
from datetime import datetime, date


class Bicicleteria() :
    '''
    Representacion de bicicleterias en python.
    
    ATRIBUTOS DE INSTANCIA:
    - arch_stock: string que define el nombre del archivo que contiene toda la informacion de las bicicletas en el stock de la bicicleteria
    - arch_hist_bicicletas: string que define el nombre del archivo que contiene informacion de todas las bicicletas que alguna vez estuvieron en la bicicleteria
    - arch_usuarios: string que define el nombre del archivo que contiene toda la informacion de los usuarios registrados en la bicicleteria
    - arch_movimientos: string que define el nombre del archivo que contiene la informacion de todas las compras y ventas de la bicicleteria
    - arch_rep_alq: string que define el nombre del archivo que contiene la informacion de todas las reparaciones y los alquileres de la bicicleteria
    - monto_caja: monto de dinero que tiene actualmente la bicicleteria (float)
    - descuento_semanal: porcentaje de descuento semanal que se le otorga a un alquiler
    - descuento_mensual: porcentaje de descuento mensual que se le otorga a un alquiler
    - cant_reparadores: cantidad de reparadores con los que cuenta el taller de la bicicleteria
    '''
    def __init__(   self , 
                    precio_carrera : float = 30.0 ,
                    precio_ciudad : float = 20.0, 
                    precio_playera : float = 10.0 ,
                    monto_caja : float = 200000.0 , 
                    descuento_semanal : float = 0.2 , 
                    descuento_mensual : float = 0.5 ,
                    cant_reparadores : int = 3  ) :
        
        self.arch_stock : str = 'stock.csv' 
        self.arch_hist_bicicletas : str = 'historial_bicicletas.csv'
        self.arch_usuarios : str = 'usuarios.csv'
        self.arch_movimientos : str = 'movimientos.csv'
        self.arch_rep_alq : str = 'rep_alq.csv'
        
        self._stock = self._hist_bicicletas = self._usuarios = self._movimientos = self._alquileres = self._taller = None

        self.monto_caja = float(monto_caja)
        self.descuento_semanal = float(descuento_semanal)
        self.descuento_mensual = float(descuento_mensual)
        self.cant_reparadores = int(cant_reparadores)
        
        Playera.precio_alq = precio_playera
        Ciudad.precio_alq = precio_ciudad
        Carrera.precio_alq = precio_carrera
            
    @property
    def stock(self)  :
        '''
        Diccionario que contiene todas las bicicletas que se encuentran en stock.
        Las claves son identificadores unicos de bicicletas y los valores
        son objetos del tipo bicicleta.
        '''
        if self._stock is None :
            try :
                datos_bicicletas = np.genfromtxt( self.arch_stock , delimiter=',' , encoding=None , dtype=str , skip_header=1 ).reshape(-1,10)
                
                self._stock = {}
                categoria_class_map = { 'Playera' : Playera ,
                                        'Carrera' : Carrera ,
                                        'Ciudad'  : Ciudad }
                
                for bici in datos_bicicletas :
                    
                    self._stock[int(bici[0])] = categoria_class_map[ bici[4] ]( id = int(bici[0]) ,
                                                                                marca = bici[1] , 
                                                                                color = bici[2] , 
                                                                                precioCompra = float(bici[3]) ,
                                                                                estado = int(bici[5]) ,
                                                                                diasDeUso = int(bici[6]) , 
                                                                                disponible = bool(int(bici[7])) ,
                                                                                vendible = bool(int(bici[8])) ,
                                                                                alquilable = bool(int(bici[9])) )
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
                
        return self._stock
    
    @property
    def hist_bicicletas(self) :
        '''
        Array con la informacion de todas las bicicletas
        que alguna vez estuvieron en la bicicleteria.
        '''
        if self._hist_bicicletas is None :
            try :
                self._hist_bicicletas = np.genfromtxt(  fname = self.arch_hist_bicicletas ,
                                                        dtype = str , 
                                                        delimiter=',' , 
                                                        encoding=None ,
                                                        skip_header=1 ).reshape(-1,6)
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
                
        return self._hist_bicicletas
    
    @hist_bicicletas.setter
    def hist_bicicletas(self, valor : np.ndarray) :
        self._hist_bicicletas = valor
    
    @property
    def usuarios(self) :
        '''
        Diccionario que contiene la informacion de todos los usuarios
        registrados en la bicicleteria. Las claves son identificadores
        unicos de los usuarios y los valores son tuplas con su informacion
        '''
        if self._usuarios is None :
            try :
                datos_usuarios = np.genfromtxt( self.arch_usuarios , delimiter=',' , encoding=None , dtype=str , skip_header=1 ).reshape(-1,5)
                self._usuarios = { usuario[0] : tuple(usuario[1:]) for usuario in datos_usuarios }
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
                
        return self._usuarios
    
    @property
    def movimientos(self) : 
        '''
        Array que contiene la informacion de todas las 
        compras y ventas de la bicicleteria.
        ''' 
        if self._movimientos is None :
            try :
                self._movimientos = np.genfromtxt( self.arch_movimientos , delimiter=',' , encoding=None , dtype=str ).reshape( -1,4 )
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
                
        return self._movimientos
    
    @movimientos.setter
    def movimientos(self, valor : np.ndarray) :
        self._movimientos = valor
        
    @property
    def alquileres(self) :
        '''
        Array que contiene la informacion de todos los alquileres de la bicicleteria.
        '''
        if self._alquileres is None :
            try :
                datos_rep_alq = np.genfromtxt( self.arch_rep_alq , delimiter=',' , encoding=None , dtype=str ).reshape(-1,7)
                self._alquileres = datos_rep_alq[ np.array(datos_rep_alq[:,6] == 'ALQ').flatten() ]
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
                
        return self._alquileres
    
    @alquileres.setter
    def alquileres(self, valor : np.ndarray) :
        self._alquileres = valor
    
    @property
    def taller(self) :
        '''
        Objeto del tipo taller que representa el taller de la bicicleteria.
        '''
        if self._taller is None :
            try :
                datos_rep_alq = np.genfromtxt( self.arch_rep_alq , delimiter=',' , encoding=None , dtype=str ).reshape(-1,7)
                datos_rep = datos_rep_alq[ np.array(datos_rep_alq[:,6] == 'REP').flatten() ]
                reparaciones = {}
                
                for reparacion in datos_rep :

                    bicicleta = self.stock.get(int(reparacion[0]))
                    
                    reparaciones[reparacion[3]] =  {'bicicleta' : int(reparacion[0]) if bicicleta is None else bicicleta ,
                                                    'cliente' : reparacion[1] if reparacion[1] != '' else None ,
                                                    'duracion' : int(reparacion[2]) ,
                                                    'fecha_fin' : str_to_dt(reparacion[4]) ,
                                                    'monto' : float(reparacion[5]) }
                
                self._taller = Taller( reparaciones , self.cant_reparadores )
            
            except FileNotFoundError :
                print('Para utilizar la clase Bicicleteria, debe ejecutar el método "crear_archivos"')
        
        return self._taller
    
    @taller.setter
    def taller(self, valor : Taller) :
        self._taller = valor
         
    def __str__( self ) :
        fecha_creacion = self.usuarios['admin2024'][3]
        clientes = self.listar_clientes()
        cant_clientes = 0 if clientes is None else clientes.size()
        
        return f'Bicicletería creada en la fecha {fecha_creacion}.\nActualmente cuenta con {len(self.stock)} bicicleta(s) en stock y {cant_clientes} cliente(s) registrados.'


    #GESTION DE USUARIOS
    def validar_usuario( self , id : str , contrasena : str ):
        '''
        Metodo que valida el id y la contrasena ingresados en el inicio sesion
        '''
        if self.usuarios.get( id ) is not None and self.usuarios.get( id )[1] == contrasena :
            return self.usuarios[id]
        return None
     
    def registrar_usuario(  self, 
                            id : str , 
                            nombre : str , 
                            contrasena : str , 
                            rol : str, 
                            fecha_registro : str) :
        '''
        Metodo para registrar usuarios en el diccionario de usuarios de la bicicleteria
        '''
        self.usuarios[id] = np.array([nombre, contrasena, rol, fecha_registro])
    
    def listar_clientes(self) :
        '''
        Metodo que devuelve una lista enlazada de todos los clientes registrados en la bicicleteria
        '''
        clientes = ListaEnlazada()
        
        for id,info_usuario in self.usuarios.items() :
            if info_usuario[2] == 'Cliente' :
                clientes.add_to_start( (id,info_usuario) )
                
        if clientes.is_empty() :
            clientes = None
            
        return clientes

    def listar_historial(self , id_cliente : str ) :
        '''
        Metodo que, dado un ID de cliente, devuelve una lista enlazada con cada alquiler que realizo
        '''
        bicis_historicas = self.hist_bicicletas
        
        hist_alquileres = ListaEnlazada() # se usa como una pila porque los elementos se agregan al principio y se extraen con pop()
        
        for alquiler in self.alquileres :
            if alquiler[1] == id_cliente :
                
                bicicleta : Bicicleta | None = self.stock.get( int(alquiler[0]) )
                en_stock = isinstance( bicicleta , Bicicleta )
                
                if not en_stock :
                    mask : np.ndarray = bicis_historicas[:,0] == alquiler[0]
                    bicicleta = bicis_historicas[ mask.flatten() ]
                
                
                hist_alquileres.add_to_start( {   
                    'id' : bicicleta.id if en_stock else bicicleta[0] , 
                    'marca' : bicicleta.marca if en_stock else bicicleta[1] , 
                    'color' : bicicleta.color if en_stock else bicicleta[2] ,
                    'categoria' : type(bicicleta).__name__ if en_stock else bicicleta[3] , 
                    'fecha_inicio' : alquiler[2][:11] , 
                    'fecha_fin' : alquiler[3][:11] , 
                    'monto' : alquiler[4] 
                } )
                
        hist_reparaciones = ListaEnlazada()
        
        for fecha_inicio, reparacion in self.taller.registro.items() :
            if reparacion['cliente'] == id_cliente :
                
                bicicleta : Bicicleta | int = reparacion['bicicleta']
                en_stock = isinstance( bicicleta , Bicicleta )
                
                if not en_stock :
                    mask : np.ndarray = bicis_historicas[:,0] == str(bicicleta)
                    bicicleta = bicis_historicas[ mask ].flatten()
                    
                hist_reparaciones.add_to_start( {   
                    'id' : bicicleta.id if en_stock else bicicleta[0] , 
                    'marca' : bicicleta.marca if en_stock else bicicleta[1] , 
                    'color' : bicicleta.color if en_stock else bicicleta[2] ,
                    'categoria' : type(bicicleta).__name__ if en_stock else bicicleta[3] , 
                    'fecha_inicio' : fecha_inicio[:11] , 
                    'fecha_fin' : dt_to_str(reparacion['fecha_fin'])[:11] , 
                    'monto' : reparacion['monto'] 
                } )
                
        return hist_alquileres, hist_reparaciones
    
    
    #GESTION DE BICICLETAS
    def comprar_bicicleta(self , bicicleta : Carrera | Ciudad | Playera ) :
        '''
        Metodo para comprar bicicletas y guardarlas en el diccionario de bicicletas de la bicicleteria.
        Tambien se registra el movimiento y actualiza la caja
        '''
        if bicicleta.precioCompra < self.monto_caja :
            self.monto_caja -= bicicleta.precioCompra
            self.stock[bicicleta.id] = bicicleta
            
            self.movimientos = np.append(   self.movimientos , 
                                            np.array([[ bicicleta.id , 
                                                        'COMPRA' , 
                                                        dt_to_str(datetime.now()) , 
                                                        bicicleta.precioCompra ]]) , 
                                            axis=0 )
            return 'La compra ha sido realizada'
        else :
            return 'La compra no ha sido realizada.\nLos fondos son insuficientes'
    
    def vender_bicicleta( self , bicicleta : Carrera | Ciudad | Playera ):
        '''
        Metodo para vender bicicletas, borrandolas del diccionario de bicicletas.
        Tambien se registra el movimiento y actualiza la caja
        '''
        self.monto_caja += bicicleta.precioVenta
        
        self.movimientos = np.append(   self.movimientos , 
                                        np.array([[ bicicleta.id , 
                                                    'VENTA' , 
                                                    dt_to_str(datetime.now()) , 
                                                    bicicleta.precioVenta ]]) , 
                                        axis=0 )
        del self.stock[bicicleta.id]
          
    def alquilar_bicicleta(self , id_cliente : str , bicicleta : Carrera | Ciudad | Playera , dias : int ) :
        '''
        Metodo para alquilar bicicletas, registrar el alquiler y actualizar la caja
        '''
        monto = self.calcular_monto(bicicleta, dias)
        
        self.monto_caja += monto
        
        bicicleta.alquilar()
        
        self.alquileres = np.append(    self.alquileres , 
                                        np.array([[ bicicleta.id , 
                                                    id_cliente , 
                                                    dias ,
                                                    dt_to_str(datetime.now()) , 
                                                    '' , 
                                                    monto ,
                                                    'ALQ']]) , 
                                        axis=0 ) 
     
    def devolucion_extension( self , 
                              id_cliente : str, 
                              bicicleta : Carrera | Ciudad | Playera , 
                              extender : bool , 
                              dias : int = 1 ) :
        '''
        Metodo que recibe una bicicleta que esta en alquiler, 
        un parametro que define si se devuelve o se extiende el 
        alquiler y, si se desea extender, una cantidad de dias por la cual 
        se desea extender el alquiler (si no se especifica se extiende por un dia)
        '''
        alquileres = self.alquileres
        
        mask = (alquileres[:,0] == str(bicicleta.id)) & (alquileres[:,4] == '') # creamos una mascara para filtrar todos los alquileres menos el alquiler actual de la bicicleta pedida
        
        alquiler = alquileres[ mask ].flatten()
        
        inicio = str_to_dt(alquiler[3])
        
        if extender :
            fin = ''
            dias_alquiler = int(alquiler[2]) + dias
        else :
            fin = datetime.now()
            dias_alquiler = (fin - inicio).days + 1     # calculamos la cantidad de dias de alquiler que se le cobran al cliente
        
        monto_anterior = float(alquiler[5])
        monto_nuevo = self.calcular_monto(bicicleta, dias_alquiler)
        
        if not extender :
            monto_nuevo += abs(monto_anterior - monto_nuevo) / 2 # se "penaliza" con un monto adicional a los clientes que no devuelven la bicicleta en la fecha prevista (sea por devolverla antes o tarde). La penalizacion es un 50%  de la diferencia entre el monto previsto y el monto real del alquiler.
            
            bicicleta.devolver( dias_alquiler )
            
            if bicicleta.estado <= 4 :  # Una vez que se devuelve la bicicleta hay que chequear el estado en el que se encuentra para ver si debe ser reparada.
                costo_reparacion = self.taller.ingresar( bicicleta, en_stock=True )
                self.monto_caja -= costo_reparacion
        
        self.monto_caja -= (monto_anterior - monto_nuevo)  # reembolsamos o cobramos dependiendo de si se devolvio antes de tiempo o si se extendio/devolvio tarde
        
        # Reemplazamos el registro del alquiler con la informacion actualizada despues de la devolucion o extension
        fecha_fin = fin if isinstance(fin, str) else dt_to_str(fin)
        fecha_inicio : str = alquiler[3]
        
        self.alquileres[ self.alquileres[:,3] == fecha_inicio ] = np.array([ bicicleta.id,
                                                                            id_cliente,
                                                                            dias_alquiler ,
                                                                            fecha_inicio ,
                                                                            fecha_fin ,
                                                                            monto_nuevo ,
                                                                            'ALQ'] )
                   
    def reparacion( self , bicicleta : Bicicleta | int, en_stock : bool, id_cliente : str | None = None ) :
        '''
        Metodo para ingresar una bicicleta al taller de reparaciones
        de la bicicleteria y actualizar el monto_caja con el monto de 
        la reparacion.
        ''' 
        if bicicleta.estado >= 9 :
            return 'La bicicleta se encuentra en estado óptimo,\nno es necesario repararla.'

        monto_reparacion : float = self.taller.ingresar( bicicleta , en_stock, id_cliente )
        
        self.monto_caja += monto_reparacion
    
        return 'La bicicleta ha ingresado\nal taller de reparaciones.'
      
       
    #ESTADISTICAS DEL NEGOCIO
    def listar_porcentaje(self , fecha : date , criterio : Literal[0,1] ) :
        '''
        Metodo que recibe una fecha , un criterio (0 o 1) y devuelve un diccionario 
        con la cantidad de alquileres (criterio == 0) o de reparaciones (criterio == 1) 
        por categoria realizadas en esa fecha
        '''
        cant_X_categoria = defaultdict(int)
        
        bicis_historicas = self.hist_bicicletas
        
        match criterio :
            case 0 :
                for alquiler in self.alquileres :
                    fecha_alquiler = str_to_d(alquiler[3])

                    if fecha_alquiler == fecha :
                        
                        bicicleta : Bicicleta | None = self.stock.get(int(alquiler[0]))
                        
                        if bicicleta is None :
                            mask : np.ndarray = bicis_historicas[:,0] == alquiler[0] # mascara para filtrar todas las bicicletas menos la que deseamos actualizar el precio de venta
                            bicicleta = bicis_historicas[ mask ].flatten()
                            
                        categoria = type(bicicleta).__name__ if isinstance(bicicleta, Bicicleta) else bicicleta[3]
                        
                        cant_X_categoria[ categoria ] += 1
            case 1 :                
                for fecha_inicio,reparacion in self.taller.registro.items() :
            
                    if fecha != str_to_dt(fecha_inicio).date() :
                        continue
                
                    bicicleta : Bicicleta = reparacion['bicicleta']
                    if not isinstance(bicicleta, Bicicleta) :
                        mask : np.ndarray = bicis_historicas[:,0] == str(bicicleta) # mascara para filtrar todas las bicicletas menos la que deseamos actualizar el precio de venta
                        bicicleta = bicis_historicas[ mask ].flatten()
                            
                    categoria = type(bicicleta).__name__ if isinstance(bicicleta, Bicicleta) else bicicleta[3]
                        
                    cant_X_categoria[ categoria ] += 1
                          
        if sum( [ valor for valor in cant_X_categoria.values() ] ) == 0 :
            cant_X_categoria = None
            
        return cant_X_categoria
    
    def listar_balance(self) :
        '''
        Metodo que realiza el balance del dia
        Devuelve listas enlazadas para las ventas, compras, alquileres y reparaciones realizados en la fecha actual
        Tambien devuelve el monto_caja de la bicicleteria y el monto total de cada tipo de operacion
        '''
        fecha = datetime.now().date()
        total_compras = 0
        total_ventas = 0
        total_alquileres = 0
        total_reparaciones = 0
        
        compras = ListaEnlazada()
        ventas = ListaEnlazada()
        
        for movimiento in self.movimientos :
            if not movimiento[0].isnumeric() :
                continue
            elif fecha == str_to_d(movimiento[2]) :
                match movimiento[1] :
                    case 'COMPRA' :
                        compras.add_to_start( movimiento )
                        total_compras += float(movimiento[3]) 
                    case 'VENTA' :
                        ventas.add_to_start( movimiento )
                        total_ventas += float(movimiento[3])
        
        alquileres = ListaEnlazada()       
        for alquiler in self.alquileres :
            
            if fecha == str_to_d(alquiler[3]) :
                alquileres.add_to_start( alquiler )
                total_alquileres += float( alquiler[5] )

        reparaciones = ListaEnlazada()
        
        for fecha_inicio, reparacion in self.taller.registro.items() :
        
            if fecha != str_to_dt(fecha_inicio).date() :
                continue
            
            reparaciones.add_to_start( (fecha_inicio,reparacion) )
            total_reparaciones += float( reparacion['monto'] )
                
        return compras, total_compras, ventas, total_ventas, alquileres, total_alquileres, reparaciones, total_reparaciones, self.monto_caja

    
    #MANEJO DE ARCHIVOS
    def crear_archivos(self) :
        '''
        Metodo utilizado al instanciar la bicicleteria, crea los archivos de stock, 
        historial de bicicletas, usuarios, movimientos y reparaciones_alquileres si es que no existen
        '''
        crear_archivo(  fname = self.arch_stock ,       
                        filas_predeterminadas = [['ID' , 'MARCA' , 'COLOR' , 'PRECIO_COMPRA($)' , 'CATEGORIA' , 'ESTADO','DIAS_DE_USO' , 'DISPONIBLE' , 'VENDIBLE' , 'ALQUILABLE']] )
        
        crear_archivo(  fname = self.arch_hist_bicicletas ,
                        filas_predeterminadas = [['ID','MARCA','COLOR','CATEGORIA','PRECIO_COMPRA($)','ESTADO']] )
        
        crear_archivo(  fname = self.arch_usuarios ,
                        filas_predeterminadas = [['ID' , 'NOMBRE' , 'CONTRASENA' , 'ROL' , 'FECHA_REGISTRO'], 
                                                ['admin2024','administrador','Admin123', 'Administrador' , d_to_str(datetime.now().date()) ] ] )
        
        crear_archivo(  fname = self.arch_movimientos ,
                        filas_predeterminadas = [['ID_BICICLETA' , 'MOVIMIENTO' , 'FECHA' , 'MONTO($)' ]])
        
        crear_archivo(  fname = self.arch_rep_alq , 
                        filas_predeterminadas = [[ 'ID_BICICLETA', 'ID_CLIENTE','DURACION_DIAS' , 'FECHA_INICIO', 'FECHA_FIN' , 'MONTO($)','OPERACION']] )

    def actualizar_archivos(self) :
        '''
        Metodo utlizado al cierre del programa que actualiza los archivos con la nueva informacion y cierra la interfaz
        '''
        #ARCHIVO STOCK
        if self._stock is not None :
            
            stock : ValuesView[Bicicleta] = self.stock.values()
            
            with open( self.arch_stock , 'w' , encoding='utf-8' , newline='' ) as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow( ['ID' , 'MARCA' , 'COLOR' , 'PRECIO_COMPRA($)' , 'CATEGORIA' , 'ESTADO' , 'DIAS_DE_USO' , 'DISPONIBLE' , 'VENDIBLE' , 'ALQUILABLE'] )
                
                for bicicleta in stock :
                    escritor.writerow( [    bicicleta.id , 
                                            bicicleta.marca , 
                                            bicicleta.color , 
                                            bicicleta.precioCompra , 
                                            type(bicicleta).__name__ ,
                                            bicicleta.estado , 
                                            bicicleta.diasDeUso , 
                                            int(bicicleta.disponible) ,
                                            int(bicicleta.vendible) ,
                                            int(bicicleta.alquilable) ] )
        
        # ARCHIVO HISTORIAL DE BICICLETAS
        if self._hist_bicicletas is not None :
            
            historial_bicicletas : np.ndarray = self.hist_bicicletas
            
            with open( self.arch_hist_bicicletas , 'w' , encoding='utf-8' , newline='' ) as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['ID','MARCA','COLOR','CATEGORIA','PRECIO_COMPRA($)','ESTADO'])
                for bicicleta in historial_bicicletas :
                    escritor.writerow(bicicleta)            
                
        # ARCHIVO USUARIOS
        if self._usuarios is not None :
            
            usuarios : dict[str,np.ndarray] = self.usuarios
            
            with open( self.arch_usuarios , 'w' , encoding='utf-8' , newline='') as archivo :
                escritor = csv.writer(archivo)
                escritor.writerow( ['ID' , 'NOMBRE' , 'CONTRASENA' , 'ROL' , 'FECHA_REGISTRO'] )
                
                for id,info_usuario in usuarios.items() :
                    usuario = np.append( np.array([id]), info_usuario )
                    escritor.writerow(usuario)
        
        # ARCHIVO MOVIMIENTOS
        if self._movimientos is not None :
                
            movimientos : np.ndarray = self.movimientos
            
            with open( self.arch_movimientos , 'w' , encoding='utf-8' , newline='' ) as archivo :
                escritor = csv.writer(archivo)
                
                if movimientos.shape[0] > 1 :
                    for fila in movimientos :
                        escritor.writerow(fila)
                else :
                    escritor.writerow(movimientos[0])   
                          
        # ARCHIVO REPARACIONES Y ALQUILERES
        if self.alquileres is not None or self.taller is not None :
            
            alquileres : np.ndarray = self.alquileres
            taller : Taller = self.taller
            
            with open( self.arch_rep_alq , 'w' , encoding='utf-8' , newline='' ) as archivo :
                escritor = csv.writer(archivo)
                escritor.writerow([ 'ID_BICICLETA', 'ID_CLIENTE','DURACION_DIAS' , 'FECHA_INICIO', 'FECHA_FIN' , 'MONTO($)','OPERACION'])
                
                for fila in alquileres :
                    escritor.writerow(fila)

                for fecha_inicio, reparacion in taller.registro.items() :
                    
                    bicicleta = reparacion['bicicleta']
                    id_cliente = reparacion['cliente']
                    
                    escritor.writerow( [bicicleta.id if isinstance(bicicleta, Bicicleta) else bicicleta,
                                        id_cliente if id_cliente is not None else '' ,
                                        reparacion['duracion'] ,
                                        fecha_inicio ,
                                        dt_to_str(reparacion['fecha_fin']) ,
                                        reparacion['monto'] ,
                                        'REP' ] )
            
        # ARCHIVO DATOS DE LA BICICLETERIA
        datos_bicicleteria = np.genfromtxt( 'datos_bicicleteria.csv' , delimiter=',' , dtype=str , encoding=None )
        
        datos_actualizados = np.array([ Carrera.precio_alq,
                                        Ciudad.precio_alq,
                                        Playera.precio_alq,
                                        self.monto_caja,
                                        self.descuento_semanal,
                                        self.descuento_mensual,
                                        self.cant_reparadores])
        
        with open( 'datos_bicicleteria.csv' , 'w' , encoding = 'utf-8' , newline='' ) as archivo :
            escritor = csv.writer(archivo)
            for fila in np.column_stack((datos_bicicleteria[:,0], datos_actualizados)) :
                escritor.writerow(fila)
        
    def registrar_bicicleta(self, bicicleta : Bicicleta) :
        '''
        Metodo que registra una bicicleta en el historial de bicicletas
        '''
        nueva_bicicleta = np.array([[  
            bicicleta.id , 
            bicicleta.marca , 
            bicicleta.color , 
            type(bicicleta).__name__ ,
            bicicleta.precioCompra,
            bicicleta.estado
        ]])
        
        self.hist_bicicletas = np.append(self.hist_bicicletas, nueva_bicicleta, axis=0)
     
       
    #OTROS METODOS UTILES
    def generar_id(self) :
        '''
        Metodo que genera automaticamente un id para la bicicleta que se esta comprando (nuevo id = mayor id existente + 1)
        '''
        id_bicicletas : np.ndarray = self.hist_bicicletas[:,0].astype(int)
        
        if len(id_bicicletas.flatten()) == 0 :
            return 1
        return np.max( id_bicicletas.flatten() ) + 1
    
    def primer_uso(self) :
        '''
        Metodo que devuelve True si no hay ningun administrador 
        registrado en el sistema que no sea el admin2024 que viene 
        con el sistema, de lo contrario devuelve False
        '''
        administradores = [ usuario for usuario in self.usuarios.values() if usuario[2]=='Administrador' ]
        
        return len( administradores ) < 2
            
    def muestreo_bicis( self , categoria : str , accion : Literal['vender','alquilar','reparar'] ) :
        '''
        Metodo que devuelve una lista enlazada con las bicicletas 
        de una categoria disponibles para alquiler, reparacion o venta, 
        dependiendo de los parametros que reciba
        '''
        muestreo = ListaEnlazada()
        
        categoria_class_map = {
            'Playera' : Playera ,
            'Carrera' : Carrera ,
            'Ciudad'  : Ciudad
        }
        
        categoria = categoria_class_map[categoria]
        
        stock : ValuesView[Bicicleta] = [bicicleta for bicicleta in self.stock.values() if isinstance(bicicleta, categoria)]
        
        for bicicleta in stock :
            
            if bicicleta.estado == 0 :  # esto significa que la bicicelta esta en reparacion, por lo que no puede ser alquilada, vendida ni reparada
                continue
            elif (accion == 'vender' or accion=='reparar') and bicicleta.alquilable and not bicicleta.disponible :  # si se busca vender o reparar una bicicleta, debemos asegurarnos de que no este en alquiler
                continue
            elif (accion == 'vender' and not bicicleta.vendible) or (accion == 'alquilar' and (not bicicleta.disponible or not bicicleta.alquilable)) :
                continue
            
            self.actualizar_precio_venta(bicicleta)
            muestreo.add_to_start( bicicleta )
                    
        if muestreo.is_empty() :
            return None     
        return muestreo

    def calcular_monto(self, bicicleta : Playera|Ciudad|Carrera, dias : int) :
        '''
        Metodo que devuelve el monto de un alquiler
        '''
        monto = dias * bicicleta.precio_alq
        
        if 7 <= dias <= 30 :
            monto *= (1-self.descuento_semanal)
        elif dias > 30 :
            monto *= (1-self.descuento_mensual)
            
        return monto
      
    def actualizar_precio_venta(self, bicicleta : Carrera | Ciudad | Playera) :
        '''
        Metodo que recibe una bicicleta y actualiza su precio de venta
        actual teniendo en cuenta el precio y estado en el que se compro
        y el estado actual.
        '''
        bicis_historicas : np.ndarray = self.hist_bicicletas
        
        mask = bicis_historicas[:,0] == str(bicicleta.id) # mascara para filtrar todas las bicicletas menos la que deseamos actualizar el precio de venta
        
        estado_original = bicis_historicas[ mask ].flatten()[5]
        
        bicicleta.precioVenta = round(bicicleta.precioCompra * (bicicleta.estado / int(estado_original)) , 2)
     
    def abrir_taller(self) :
        '''
        Metodo para abrir el taller, llama al getter de self.taller
        para crear el objeto y que empiece a procesar las reparaciones
        '''
        self.taller
