import csv
import datetime
from TP_EDP import Telefono
import Paquete as pkt

class Central():
    
    def __init__(self):
        
        self.phones = self.extractFile('telefonos.csv')
        self.callLog = dict()
        self.SMSLog = dict()
        
    #Verificar si van todos los atributos del l
    
    def extractFile(self, archivo_csv):
        phones = dict()
        try:
            with open(archivo_csv, mode='r', newline='', encoding = 'utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)
                for telefono in lector_csv:
                    phones[int(telefono[0])]=Telefono(int(telefono[0]),telefono[1],telefono[2],telefono[3],
                                                    telefono[4],telefono[5],telefono[6],telefono[7])      
            print("Todos los teléfonos han sido registrados desde el archivo CSV.")
            return phones
        except FileNotFoundError:
            print("El archivo CSV no fue encontrado.")
        except KeyError as e:
            print(f"Error en el archivo CSV. Faltan columnas: {e}")
        except Exception as e:
            print(f"Se produjo un error al leer el archivo CSV: {e}")

    def eraseDevice(self,telefono:Telefono):
        if telefono.id in self.phones:
            self.phones.pop(telefono.id)
            print (f"Se elimino el telefono con el id {telefono.id}")
        else:
            print (f"No se encuentra registrado el telefono con el id {telefono.id}")
        
    def registerDevice(self, telefono:Telefono):
        if telefono.id not in self.phones: 
            self.phones.update({telefono.id : telefono})
            print (f"Se registro el telefono con el id {telefono.id}")
        else:
            print (f"Ya se encuentra registrado el telefono con el id {telefono.id}")
    
    
    def verifyWeb(self, numero):
        
        if numero not in self.phones:
            print(f"El telefono con numero {numero} no esta registrado.")
            return False

        dispositivo = self.phones[numero]
        
        if dispositivo.encendido and dispositivo.configParameters.red:
            print(f"El telefono con numero {numero} esta disponible.")
            return True
        else:
            print(f"El telefono con numero {numero} no esta disponible.")
            return False
        
    
    def verifyInternet(self, numero):
        
        if numero not in self.phones:
            print(f"El telefono con numero {numero} no tiene acceso a internet.")
            return False
        
        dispositivo = self.phones[numero]
        if dispositivo.encendido and dispositivo.datos:
            print(f"El telefono con numero {numero} tiene acceso a internet.")
            return True
        else:
            print(f"El telefono con numero {numero} no tiene acceso a internet.")
            return False
    
    def receivePakcet(self, packet : pkt.Paquete):
        
        if not isinstance(packet, pkt.Paquete):
            print ('CENTRAL: Error al procesar paquete, tipo erroneo')
            return False
        
        if isinstance(packet, pkt.PaqueteLlamada):
            newPacket = self.handleCall(packet)
            return newPacket
        else:
            newPacket = self.handleSMS(packet)
            return newPacket
    
    def handleSMS (self, packet : pkt.PaqueteSMS):
        receptor = packet.receiver
        isReceiver = False
        for phone in self.phones.values():
            if phone.numero == receptor:
                isReceiver = True
        if not isReceiver:
            packet.message = None ##Distinto de un caracter vacio '' asi que nunca puede entrar por error
        return packet
    
## Modelo de paquete a enviar: ['LLAMADA', Emisor , Receptor, datetime , pedido]. R = REQUEST ; B = BUSY ; N = NOT FOUND ; K = OK ; S = STOP ; F = RECHAZADO
    
    def handleCall(self, packet : pkt.PaqueteLlamada):
        """Inicia la llamada verificando la disponibilidad de ambos teléfonos."""
        
        originNumber = packet.sender
        destinyNumber = packet.receiver
        
        senderRegistered = False
        receiverRegistered = False
        
        senderId = None
        receiverId = None
        
        for registeredPhone in self.phones.values():
            if originNumber == registeredPhone.numero:
                senderRegistered = True
                senderId = registeredPhone.id
            if destinyNumber == registeredPhone.numero:
                receiverRegistered = True
                receiverId = registeredPhone.id
        
        if not (senderRegistered and receiverRegistered):
            print(f"El teléfono con número {destinyNumber} no está registrado en la central.")
            packet.intention = pkt.Intentions.NOT_FOUND
            return packet
        
        #Ambos estan registrados en la central
        originPhone = self.phones[senderId]
        destinyPhone = self.phones[receiverId]
        
        if packet.intention == pkt.Intentions.REQUEST:
            # Verificar si ambos teléfonos están disponibles para la llamada
            if not (self.verifyWeb(senderId) and self.verifyWeb(receiverId)):
                print("Uno o ambos teléfonos no están disponibles para la llamada.")
                return False

            if destinyPhone.ocupado:
                print(f"No se puede realizar la llamada. El número {destinyNumber} está ocupado.")
                packet.intention = pkt.Intentions.BUSY
                return packet
            else:
                #['LLAMADA', Emisor , Receptor, datetime , 'R']
                return packet
        elif packet.intention == pkt.Intentions.OK:
            return packet
        elif packet.intention == pkt.Intentions.REJECTED:
            #['LLAMADA', Emisor , Receptor, datetime , 'F']
            header = packet.sender + ' - ' + packet.receiver +' , ' + packet.datetime
            self.callLog.update({header : 'Rechazada'})    
            return packet
        elif packet.intention == pkt.Intentions.STOP:
            header = packet.sender + ' - ' + packet.receiver +' , ' + packet.datetime
            time1 = datetime.datetime.strptime(packet.datetime,"%d/%m/%Y, %H:%M:%S") ##Inicio de comunicacion
            time2 = datetime.datetime.now().replace(microsecond = 0) #Fin de comunicacion
            delta = time2 - time1
            self.callLog.update({header : 'Duracion: ' + str(delta)})
            return packet

'''#      PRUEBA DE LLAMADA, RECEPCION Y CORTE   
test = Central()

santi = Telefono(2,'Santi', 'S22', 'Android', '3.0.0', '16 G', '256 G', '1122857835')
gonza = Telefono(3,'Gonza', 'S22', 'Android', '3.0.0', '16 G', '256 G', '1159369841')

##El numero como clave porque no se va a repetir / no se deberia repetir para la central
test.phones.update({santi.id : santi,
                       gonza.id : gonza})


gonza.encendido = True
santi.encendido = True

gonza.bloqueado = False
santi.bloqueado = False

gonza.configParameters.red = True
gonza.configParameters.datos = True

santi.configParameters.red = True
santi.configParameters.datos = True

gonza.openApp()
santi.openApp()


##ENVIAR LLAMADA
paquete = gonza.currentApp.sendCallRequest(gonza.numero) 
paquete2 = test.receivePakcet(paquete)

##RESPONDER LLAMADA
paquete3 = santi.currentApp.receivePacket(paquete2)
paquete4 = test.receivePakcet(paquete3)
paquete5 = gonza.currentApp.receivePacket(paquete4)

##CORTAR LLAMADA
respuesta = santi.currentApp.endCallRequest(santi.numero)
respuesta2 = test.receivePakcet(respuesta)
respuesta3 = gonza.currentApp.receivePacket(respuesta2)

gonza.currentApp.getCallHistory()
santi.currentApp.getCallHistory()
print('fin')'''