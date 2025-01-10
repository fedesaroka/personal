class Bicicleta :
    '''
    Representacion de bicicletas en python.
    
    ATRIBUTOS DE INSTANCIA:
    - id: identificador unico que diferencia a todas las bicicletas (int positivo)
    - marca: marca de la bicicleta (str)
    - color: color de la bicicleta (str)
    - precioCompra: precio al que se compro la bicicleta (float)
    - precioVenta: precio actual al que se vende la bicicleta (float)
    - diasDeUso: Cantidad estimada de dias de uso que tiene la bicicleta (int positivo)
    - estado: Numero entero del 0 al 10 que representa la condicion en la que se encuentra la bicicleta.
    - vendible: booleano que indica si la bicicleta es vendible o no
    - alquilable: booleano que indica si la bicicleta es alquilable o no
    - disponible: booleano que indica si la bicicleta esta actualmente disponible para alquiler 
    '''
    def __init__(   self , 
                    id : int , 
                    marca : str , 
                    color : str , 
                    precioCompra : float , 
                    diasDeUso : int = None , 
                    estado : int = None ,
                    disponible : bool = None , 
                    vendible : bool = None , 
                    alquilable : bool = None ) :
        
        self.id = id
        self.marca = marca
        self.color = color.lower()
        self.precioCompra = precioCompra
        self.precioVenta = precioCompra
        self._diasDeUso = diasDeUso # cache de la propiedad "diasDeUso"
        self._estado = estado # cache del la propiedad "estado" para solamente tener que calcularla cuando cambia el atributo "_diasDeUso"
        self._vendible = vendible # cache de la propiedad "vendible"
        self._alquilable = alquilable # cache de la propiedad "alquilable"
        self._disponible = disponible # # cache de la propiedad "disponible"
    
    @property
    def diasDeUso( self ) :
        '''
        Si no se define una cantidad de dias de uso al crear la bicicleta,
        debe aproximarse utilizando el estado en el que se encuentra y su vida util.
        Si tampoco se define el estado al crearse, se establece un valor predeterminado de
        cero dias de uso.
        '''
        if self._diasDeUso is None :
            
            if self._estado is not None and self._estado < 9 :
                self._diasDeUso = round((9 - self._estado) * (type(self).vida_util / 8))
            elif self._estado is None or self._estado == 10 :
                self._diasDeUso = 0
            else :
                self._diasDeUso = 1
                
        return self._diasDeUso
    
    @diasDeUso.setter
    def diasDeUso( self , valor : int ) :
        self._diasDeUso = valor
        self._estado = None # dado que cambio el valor del atributo "diasDeUso", desactivamos el cache de la propiedad "estado" para volver a calcularla la proxima vez que lo llame
    
    @property
    def estado( self ) :
        ''' 
        - Si la bicicleta es nueva, el numero es 10 y puede venderse pero no alquilarse (excepto que el atributo "alquilable" o "vendible" se cambie mediante su setter). 
        - Si la bicicleta no es nueva, el numero se calcula con los dias de uso que tiene la bicicleta (atributo de instancia "diasDeUso") y su vida util (atributo de clase "vida_util").
        - Si el numero calculado esta entre 5 y 9 inclusive se considera usada, siendo 9 el mejor estado en el que puede estar una bicicleta usada y 4 el peor, y puede venderse y alquilarse (excepto que el atributo "alquilable" o "vendible" se cambie mediante su setter).
        - Si el numero calculado esta entre 1 y 4 inclusive se considera dañada, por lo que no puede ser alquilada a menos que se repare.
        - Mientras mas bajo sea el numero, mas bajo sera el precio de venta y mas larga y costosa sera la reparacion de la bicicleta.
        - Si el numero es 0, significa que la bicicleta esta siendo reparada en este momento.
        - Cuando una bicicleta se termina de reparar su estado pasa a ser 9, dado que no es nueva pero se deja en muy buenas condiciones
        '''
        # Si el cache esta disponible lo uso
        if self._estado is not None :
            return round(self._estado)
        # Si el cache no esta disponible, significa que cambio el valor del atributo "diasDeUso", por lo que debe calcularse devuelta
        elif self.diasDeUso == 0 :
            self._estado = 10
        else :
            self._estado = 9 - ( self.diasDeUso * ( 8 / type(self).vida_util ) ) 
            if self._estado < 1 : # salvamos el caso aunque lo mas probable es que no suceda dado que las bicicletas no pueden alquilarse una vez que el estado es 4 o menos
                self._estado = 1
        
        return round(self._estado)
        
    @estado.setter
    def estado( self , valor : int ) :
        self._estado = valor
    
    @property
    def vendible( self ) :
        '''
        Si no se define al crear la bicicleta,
        se establece True como predeterminado.
        '''
        if self._vendible is None :
            self._vendible = True
        return self._vendible
    
    @vendible.setter
    def vendible( self , valor : bool ) :
        self._vendible = valor
    
    @property
    def alquilable( self ) :
        '''
        Si no se define al crear la bicicleta,
        se establece el True como predeterimnado si
        el estado es menor o igual a 9. De lo contrario,
        se establece False.
        '''
        if self._alquilable is None :
            self._alquilable = self.estado <= 9 
        return self._alquilable
    
    @alquilable.setter
    def alquilable( self , valor : bool ) :
        self._alquilable = valor
         
    @property
    def disponible( self ) :
        '''
        Si no se define al crear la bicicleta, 
        se establece como True si el estado es menor o igual a 9 
        o si la bicicleta es alquilable.
        '''
        if self._disponible is not None :
            return self._disponible
        return ( self.estado <= 9 ) or ( self._alquilable if self._alquilable is not None else False ) 
    
    @disponible.setter
    def disponible( self , valor : bool ) :
        self._disponible = valor
    
    
    def __str__(self):
        return f"ID: {self.id}\nMarca: {self.marca}\nColor: {self.color}\nPrecio venta: ${self.precioVenta}\nCategoria: {type(self).__name__}\nEstado: {self.estado}"
    
    def __eq__(self , other ) :
        return self.id == other.id
    
    def alquilar(self) :    
        '''
        Metodo que modifica la disponibilidad de la bicicleta al alquilarla
        '''
        self.disponible = False
     
    def devolver( self , duracion_alquiler : int ) :
        '''
        Metodo que modifica la disponibilidad de la bicicleta y actualiza la cantidad de dias de uso que tiene al devolverla
        '''
        self.diasDeUso += duracion_alquiler
        self.disponible = True

    def reparar( self ) :
        '''
        Metodo que se ejecuta cuando ingresa la bicicleta al taller de reparaciones
        '''
        self.estado = 0
    
    def fin_reparacion( self ) :
        '''
        Metodo que se ejecuta cuando la bicicleta se termina de reparar, dejandola en estado 9
        '''
        self.diasDeUso = 1  # si toma el valor 0 se convierte en nueva y no tendria sentido dado que la bicicleta si fue usada


class Playera(Bicicleta) :
    '''
    Representacion de bicicletas del tipo Playera en python.
    
    ATRIBUTOS Y PROPIEDADES DE INSTANCIA:
    - id: identificador unico que diferencia a todas las bicicletas (int positivo)
    - marca: marca de la bicicleta (str)
    - color: color de la bicicleta (str)
    - precioCompra: precio al que se compro la bicicleta (float)
    - precioVenta: precio actual al que se vende la bicicleta (float)
    - diasDeUso: Cantidad estimada de dias de uso que tiene la bicicleta (int positivo)
    - estado: Numero entero del 0 al 10 que representa la condicion en la que se encuentra la bicicleta.
    - vendible: booleano que indica si la bicicleta es vendible o no
    - alquilable: booleano que indica si la bicicleta es alquilable o no
    - disponible: booleano que indica si la bicicleta esta actualmente disponible para alquiler 
    ATRIBUTOS DE CLASE:
    - precio_alq: Precio de alquiler por dia. Este atributo se define como None, pero para ser usado debe definirse como un float
    - vida_util: Vida util en dias de las bicicletas del tipo Playera
    '''
    def __init__(   self, 
                    id: int, 
                    marca: str, 
                    color: str, 
                    precioCompra : float, 
                    diasDeUso : int = None,
                    estado : int = None ,
                    disponible : bool = None, 
                    vendible : bool = None, 
                    alquilable : bool = None):
        super().__init__(id, marca, color, precioCompra, diasDeUso, estado, disponible, vendible, alquilable)
    
    precio_alq = None   
    vida_util = 2190 


class Ciudad(Bicicleta) :
    '''
    Representacion de bicicletas del tipo Ciudad en python.
    
    ATRIBUTOS Y PROPIEDADES DE INSTANCIA:
    - id: identificador unico que diferencia a todas las bicicletas (int positivo)
    - marca: marca de la bicicleta (str)
    - color: color de la bicicleta (str)
    - precioCompra: precio al que se compro la bicicleta (float)
    - precioVenta: precio actual al que se vende la bicicleta (float)
    - diasDeUso: Cantidad estimada de dias de uso que tiene la bicicleta (int positivo)
    - estado: Numero entero del 0 al 10 que representa la condicion en la que se encuentra la bicicleta.
    - vendible: booleano que indica si la bicicleta es vendible o no
    - alquilable: booleano que indica si la bicicleta es alquilable o no
    - disponible: booleano que indica si la bicicleta esta actualmente disponible para alquiler 
    ATRIBUTOS DE CLASE:
    - precio_alq: Precio de alquiler por dia. Este atributo se define como None, pero para ser usado debe definirse como un float
    - vida_util: Vida util en dias de las bicicletas del tipo Ciudad
    '''
    def __init__(   self, 
                    id: int, 
                    marca: str, 
                    color: str, 
                    precioCompra : float, 
                    diasDeUso: int = None, 
                    estado : int = None ,
                    disponible : bool = None, 
                    vendible : bool = None, 
                    alquilable : bool = None):
        super().__init__(id, marca, color, precioCompra, diasDeUso, estado, disponible, vendible, alquilable)
       
    precio_alq = None
    vida_util = 2920    
      
         
class Carrera(Bicicleta) :
    '''
    Representacion de bicicletas del tipo Carrera en python.
    
    ATRIBUTOS Y PROPIEDADES DE INSTANCIA:
    - id: identificador unico que diferencia a todas las bicicletas (int positivo)
    - marca: marca de la bicicleta (str)
    - color: color de la bicicleta (str)
    - precioCompra: precio al que se compro la bicicleta (float)
    - precioVenta: precio actual al que se vende la bicicleta (float)
    - diasDeUso: Cantidad estimada de dias de uso que tiene la bicicleta (int positivo)
    - estado: Numero entero del 0 al 10 que representa la condicion en la que se encuentra la bicicleta.
    - vendible: booleano que indica si la bicicleta es vendible o no
    - alquilable: booleano que indica si la bicicleta es alquilable o no
    - disponible: booleano que indica si la bicicleta esta actualmente disponible para alquiler 
    ATRIBUTOS DE CLASE:
    - precio_alq: Precio de alquiler por dia. Este atributo se define como None, pero para ser usado debe definirse como un float
    - vida_util: Vida util en dias de las bicicletas del tipo Carrera
    '''
    def __init__(   self, 
                    id: int, 
                    marca: str, 
                    color: str, 
                    precioCompra : float, 
                    diasDeUso: int = None, 
                    estado : int = None ,
                    disponible : bool = None, 
                    vendible : bool = None, 
                    alquilable : bool = None):
        super().__init__(id, marca, color, precioCompra, diasDeUso, estado, disponible, vendible, alquilable)
        
    precio_alq = None
    vida_util = 1460 
