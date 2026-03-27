import datetime
from Aplicacion import Aplicacion
from Paquete import PaqueteLlamada, Intentions
from Stack import Stack

## Modelo de paquete a enviar: ['LLAMADA', Emisor , Receptor, datetime , pedido]. R = REQUEST ; B = BUSY ; N = NOT FOUND ; K = OK ; S = STOP ; F = RECHAZADO
class Llamadas(Aplicacion):
    def __init__(self, weight) -> None:
        super().__init__(weight)
        self.callHistory = Stack()
        
    def sendCallRequest (self, tel1 : str):
        
        if not self.callHistory.empty():
            if self.callHistory.topValue.value[1] == 'En curso':
                print('Ya tiene una llamada en curso')
                return None
        
        tel2 = input('Ingrese el numero de telefono a llamar: ')
        
        packet = PaqueteLlamada(tel1, tel2, datetime.datetime.now().replace(microsecond = 0).strftime("%d/%m/%Y, %H:%M:%S"), Intentions.REQUEST )
        
        return packet
    
    def receivePacket(self, packet : PaqueteLlamada):
        
        if not isinstance(packet, PaqueteLlamada):  
            print('Error en paquete, no se puede procesar')
            return False
        
        if not self.callHistory.empty():
            if self.callHistory.topValue.value[1] == 'En curso':
                print('Ya tiene una llamada en curso')
                return None
        
        if packet.intention == Intentions.BUSY:
            header = packet.receiver + '-' + packet.datetime
            self.callHistory.push(( header , 'Ocupado'))
            
        elif packet.intention == Intentions.NOT_FOUND:
            print ('El telefono no se encuentra en linea')
            
        elif packet.intention == Intentions.OK:
            header = packet.receiver + '-' + packet.datetime
            self.callHistory.push(( header , 'En curso'))
            
        elif packet.intention == Intentions.STOP: ##Esto asume que tu propio numero de telefono esta en packet.sender
            header = packet.sender + '-' + packet.datetime
            time1 = datetime.datetime.strptime(packet.datetime,"%d/%m/%Y, %H:%M:%S") ##Inicio de comunicacion
            time2 = datetime.datetime.now().replace(microsecond = 0) #Fin de comunicacion
            delta = time2 - time1
            self.callHistory.pop()
            self.callHistory.push((header , 'Duracion: ' + str(delta)))
            
        elif packet.intention == Intentions.REQUEST:
            choice = None
            choice = input(f'Llamada entrante de {packet.sender} \n Aceptar? (Y/N)')
            choice.upper()
            while not choice in ['Y', 'N']:
                choice = input('Error, ingrese una opcion valida (Y/N)')
                choice.upper()
                    
            if choice == 'N':
                packet.intention = Intentions.REJECTED
                return packet
            else:
                header = packet.sender + '-' + packet.datetime
                self.callHistory.push((header , 'En curso'))
                packet.intention = Intentions.OK
                return packet
        elif packet.intention == Intentions.REJECTED:
            header = packet.sender + '-' + packet.datetime
            self.callHistory.push((header , 'Rechazada'))
           
    def endCallRequest (self, tel1 : str):
        
        if 'En curso' not in self.callHistory.topValue.value[1]:
            print('No hay llamada en curso')
            return False
        
        target = self.callHistory.pop()[0]
                
        target = target.split('-')
        
        #packet = ['LLAMADA', tel1 , target[0] , target[1] , 'S' ]
        packet = PaqueteLlamada(tel1, target[0], target[1], Intentions.STOP)
        
        time1 = datetime.datetime.strptime(target[1],"%d/%m/%Y, %H:%M:%S") ##Inicio de comunicacion
        time2 = datetime.datetime.now().replace(microsecond = 0) #Fin de comunicacion
        delta = time2 - time1
        
        self.callHistory.push((target[0] + '-' + target[1] , 'Duracion: ' + str(delta)))
        
        return packet
       
    def getCallHistory(self):
        print(self.callHistory)
        return None
    
    @staticmethod
    def getDatetimeFromHeader (header : str):
        
        header.split(',')
        date = datetime.datetime.strptime(header[1] , "%d/%m/%Y, %H:%M:%S")
        
        return date