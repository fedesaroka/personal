from datetime import *
from bicicleta import *
import queue as q
import threading as th
from typing import Literal, Union
from auxiliares import dt_to_str, str_to_dt


class Taller :
    '''
    Procesa reparaciones de bicicletas. Debe instanciarse con un registro de reparaciones que puede estar vacio y una cantidad de reparadores con los que cuenta el taller.
    
    ATRIBUTOS:
        - registro: array de diccionarios con la informacion de todas las reparaciones (pendientes, en proceso o completadas)
        - en_proceso: diccionario con todas las reparaciones en proceso
        - max_reparaciones: maxima cantidad de reparaciones simultaneas permitidas que esta dada por la cantidad de reparadores que tiene la bicicleteria
        - _pendientes: cache de la propiedad "pendientes" utilizada para no tener que calcularla cuando no es necesario
        - nuevo_ingreso: Objeto del tipo Event unicamente utilizado cuando hay reparadores libres, 
            con el fin de obligar al programa a esperar hasta que ingrese una bicicleta al taller para seguir ejecutandose
        - fin_reparacion: Objeto del tipo Event utilizado cuando no hay reparadores libres,
            con el fin de obligar al programa a esperar hasta que termine de repararse alguna bicicleta para seguir ejecutandose
        - abrir_taller: Objeto del tipo Thread utilizado con el fin de procesar las reparaciones en segundo plano mientras la bicicleteria realiza otras tareas
    '''
    def __init__(   self , 
                    registro : dict[str, dict[Literal['bicicleta','cliente','duracion','fecha_fin','monto'], Union[Bicicleta,str,int,datetime,float] ] ] , 
                    cant_reparadores : int ) :
        
        self.registro : dict[str, dict] = registro
        self.max_reparaciones : int = cant_reparadores
        self._pendientes : q.Queue | None = None
        self.en_proceso : dict = {}
       
        self.nuevo_ingreso : th.Event = th.Event()
        self.fin_reparacion : th.Event = th.Event()
        
        self.abrir_taller = th.Thread( target = self.procesar , daemon = True )
        self.abrir_taller.start()
        
    @property
    def pendientes( self ) :
        '''
        Queue (FIFO) que contiene a todas 
        las reparaciones pendientes.
        '''
        if self._pendientes is None :   
            pendientes = q.Queue()
            
            fechas_inicio = [str_to_dt(fecha) for fecha in self.registro.keys()]
            
            for fecha_inicio in sorted(fechas_inicio) :
                reparacion = self.registro[dt_to_str(fecha_inicio)]
                
                fecha_fin = reparacion['fecha_fin']
                bicicleta = reparacion['bicicleta']
                
                if datetime.now() <= fecha_fin :
                    pendientes.put((fecha_fin, bicicleta))
                    
                elif isinstance(bicicleta, Bicicleta) and bicicleta.estado == 0 :
                    bicicleta.fin_reparacion()
             
            self._pendientes = pendientes
            
        return self._pendientes
    
    def __str__(self) :
        return f'El taller cuenta con {len(self.en_proceso)} reparaciones en proceso y {self.pendientes.qsize()-len(self.en_proceso)} reparaciones pendientes.'
     
    def procesar(self) :
        '''
        Metodo que, mediante un daemon thread para que siga corriendo en segundo plano, 
        se ejecuta desde el init hasta que el programa finaliza.
        Este metodo se encarga de continuamente leer el registro de 
        reparaciones en tiempo real y procesar todas las reparaciones 
        que puedan terminar durante la ejecucion del programa.
        '''   
        while True :
            pendientes = self.pendientes
            
            while not pendientes.empty() :
                
                reparacion = pendientes.get()
                self.en_proceso[dt_to_str(reparacion[0])] = reparacion[1]
                
                reparar = th.Thread(target=self.reparar, args=(reparacion,), daemon=True)   # este thread representa la reparacion en tiempo real de una bicicleta
                reparar.start()
                
                if len(self.en_proceso) == self.max_reparaciones :
                    self.fin_reparacion.clear()  
                    self.fin_reparacion.wait()
                    
            self.nuevo_ingreso.clear()
            self.nuevo_ingreso.wait()
            
            
    def reparar(self, reparacion : tuple[datetime, Bicicleta|int]) :
        '''
        Metodo que simula la reparacion de una bicicleta en tiempo real,
        esperando la cantidad de tiempo necesaria para que termine
        la reparacion para terminar de ejecutarse. Se ejecuta utilizando
        un daemon thread para que pueda correr en segundo plano.
        '''
        fecha_fin = reparacion[0]
        tiempo_espera : timedelta = fecha_fin - datetime.now()  
        th.Timer(tiempo_espera.total_seconds(), self.finalizar_reparacion, args=(reparacion,)).start()
        
    def finalizar_reparacion(self, reparacion : tuple[datetime, Bicicleta|int]) :
        '''
        Metodo que finaliza la reparacion de una bicicleta.
        '''
        fecha_fin, bicicleta = reparacion
        
        if isinstance(bicicleta, Bicicleta) :
            bicicleta.fin_reparacion()
            
        del self.en_proceso[dt_to_str(fecha_fin)]
        self.fin_reparacion.set()
           
    def ingresar( self , bicicleta : Playera | Ciudad | Carrera , en_stock : bool, id_cliente : str | None = None ) :
        '''
        Metodo que recibe una bicicleta y la registra en el taller de reparaciones.
        '''
        self._pendientes = None # desactivamos el cache del atributo "pendientes" para calcularlo devuelta y que incluya la nueva bicicleta que esta ingresando al taller
        
        fecha_inicio = self.prox_fecha_inicio()
        duracion = 9 - bicicleta.estado
        fecha_fin = fecha_inicio + timedelta(days=duracion)
        
        costo = bicicleta.precio_alq * duracion
        
        monto = costo * ( 0.25 if not en_stock else -1 ) # Cuando la bicicleta a reparar no esta en el stock de la bicicleteria, se debe cobrarle al dueño de la bicicleta lo suficiente para obtener una ganancia del 25%  del costo de la reparacion.
        
        self.registro[dt_to_str(fecha_inicio)] = {  
            'bicicleta' : bicicleta if en_stock else bicicleta.id ,
            'cliente' : id_cliente ,
            'duracion' : duracion ,
            'fecha_fin' : fecha_fin ,
            'monto' : monto
        }
        
        if en_stock :
            bicicleta.reparar()
        
        self.nuevo_ingreso.set()
        
        return costo
    
    def prox_fecha_inicio(self) :
        '''
        Metodo utilizado al ingresar una nueva bicicleta al taller,
        devuelve la fecha de inicio de la nueva reparacion
        '''
        ahora = datetime.now()
        
        if len(self.en_proceso) < self.max_reparaciones : # Si todavia hay reparadores libres al momento, la reparacion empieza inmediatamente.
            return ahora
    
        # Para determinar la fecha de inicio, nos fijamos en la fecha de fin de la primera 
        # reparacion que libere a un reparador y le permita empezar esta nueva reparacion.
        fechas_fin = []
        for reparacion in self.registro.values() :
            fecha_fin : datetime = reparacion['fecha_fin']
            
            if ahora > fecha_fin :   # aseguramos que solo se incluyen las reparaciones que no finalizaron
                continue
            
            if len(fechas_fin) == self.max_reparaciones :
                fechas_fin.remove(min(fechas_fin))
                
            fechas_fin.append(fecha_fin)
            
        return min(fechas_fin)
        