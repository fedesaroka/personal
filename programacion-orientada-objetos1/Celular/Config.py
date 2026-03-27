from Aplicacion import Aplicacion
from Parametros import ConfigParameters

#Estoy importando Telefono a cada metodo para evitar un import circular

class Config(Aplicacion):
    """Subclase de Aplicacion con los metodos para congifurar el telefono

    Args:
        Aplicacion (_Clase_ _padre_)
    """    
    def __init__(self, weight):
        super().__init__(weight)
    
    def changePassword(self, tel : ConfigParameters): ##Hay que pasarle el telefono sobre el que esta actuando
        
        if not isinstance(tel, ConfigParameters):
            raise TypeError ("Clase incorrecta")
        
        password = input ("Ingrese contraseña actual: ")
        
        if tel.pin != password:
            print ("Contraseña incorrecta")
            return False
        
        newpassword = input("Ingrese contraseña nueva: ")
        
        if input("Ingrese nuevamente: ") != newpassword:
            print("Contraseña incorrecta")
            return False
        
        tel.pin = newpassword
        return True
        
        
    def setName (self, tel : ConfigParameters):
        
        if not isinstance(tel, ConfigParameters):
            raise TypeError ("Clase incorrecta")
        
        password = input("ingrese contraseña actual: ")
        
        if tel.pin == password:
            newname = input ("Ingrese nombre nuevo: ")
            tel.name = newname
            return True
        else:
            print("Contraseña incorrecta")
            return False
        
    def red(self, tel : ConfigParameters):
        
        if isinstance(tel, ConfigParameters):
            tel.red = not tel.red
        else:
            raise TypeError ("Clase incorrecta")

    def datos(self, tel : ConfigParameters):
        
        if isinstance(tel, ConfigParameters):
            tel.datos = not tel.datos
        else:
            raise TypeError ("Clase incorrecta")

