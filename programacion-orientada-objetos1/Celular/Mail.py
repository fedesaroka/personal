import csv
from Aplicacion import Aplicacion
from funciones_auxiliares import createFile, ListaEnlazada
from datetime import datetime

class Mail(Aplicacion):
    
    def __init__(self, weight):
        super().__init__(weight)
        createFile('mails.csv',['ID','DE','PARA','FECHA','MENSAJE','LECTURA'])
        self.mails=self.extractFile('mails.csv')
     
    def extractFile(self, archivo_csv):
        mails = {0:['-','-',datetime(2024,1,1).strftime("%Y-%m-%d"),'Bienvenido a Mails','Leido']}
        try:
            with open(archivo_csv, mode='r', newline='', encoding= 'utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Saltar encabezados
                for mail in lector_csv:
                    mails[int(mail[0])] = (mail[1],mail[2],mail[3],mail[4],mail[5])
            print("Todos los mails han sido registrados desde el archivo CSV.")
            return mails
        except FileNotFoundError:
            print("El archivo CSV no fue encontrado.")
        except KeyError as e:
            print(f"Error en el archivo CSV. Faltan columnas: {e}")
        except Exception as e:
            print(f"Se produjo un error al leer el archivo CSV: {e}")
       
    def sortMailByUnread(self):
        sortedLinkedList = ListaEnlazada()
        
        # Primero agregamos los correos "No Leídos"
        for mail in self.mails:
            if self.mails[mail][4].strip().lower() == 'no leido':  # Comparación insensible a mayúsculas
                sortedLinkedList.add_to_end(self.mails[mail])
        
        # Luego agregamos los correos "Leídos"
        for mail in self.mails:
            if self.mails[mail][4].strip().lower() == 'leido':  # Comparación insensible a mayúsculas
                sortedLinkedList.add_to_end(self.mails[mail])
                
        for mail in sortedLinkedList:
            print(mail)
                
    def sortMailByDate(self): #value seria el mail
        
        
        descendingLinkedList = sorted(
        [value for value in self.mails.values()],
        key=lambda x: datetime.strptime(x[2],"%Y-%m-%d"),  
        reverse=True
    )
        for mail in descendingLinkedList:
            print(mail)
