from Aplicacion import Aplicacion

class Contactos(Aplicacion):
    def __init__(self, weight):
        super().__init__(weight)
        self.contactList = dict()
        
    
    def addContact(self, name : str, number : str):
        
        if name in self.contactList.keys():
            print("Ya existe un contacto con ese nombre")
        
        if isinstance(name, str) and number.isnumeric():
            self.contactList.update({name : number}) 
        else:
            if not isinstance (name, str):
                raise ValueError("Error al ingresar el nombre, por favor ingrese")
            else:
                raise ValueError("Error al ingresar el numero, ingrese un numero valido")
    
    def deleteContact (self, name):
        try:
            self.contactList.pop(name)
        except KeyError:
            print ("Error, se encuentra un contacto con ese nombre")
            return 0
    
    def updateContact (self, name, value):
        
        if not name in self.contactList.keys():
            print ("El contacto no existe")
        else:
            self.contactList.update({name : value})
