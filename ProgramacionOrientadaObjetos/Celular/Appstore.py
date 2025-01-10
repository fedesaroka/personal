import csv
from Aplicacion import Aplicacion
from Parametros import ConfigParameters
# from TP_EDP import Telefono

class AppStore (Aplicacion):
    def __init__(self, weight):
        super().__init__(weight)
        self.availableAppsList = self.getApps()
    
    
    def getApps(self):
        """
        Lee el archivo csv para obtener las aplicaciones de la app store
        
        Returns:
            [Nombre, peso en bytes, version minima]
        
        """
        try:
            with open('Play Store Data.csv', 'r', encoding = 'utf-8') as archivo:
                reader = csv.reader(archivo)

                usefulData = [[],[],[]]
                for row in reader:
                    usefulData[0].append(row[0])
                    usefulData[1].append(row[4])
                    if len(row) < 13:
                        usefulData[2].append('')
                    else:
                        usefulData[2].append(row[12])
                
                usefulData[0] = usefulData[0][1:]
                usefulData[1] = usefulData[1][1:]
                usefulData[2] = usefulData[2][1:]
                usefulData[2] = self.filterVersionList(usefulData[2])
                
                for i in range(len(usefulData[1])): ##Ver que hacer con los pesos que "varian segun device"
                    usefulData[1][i] = self.tamanio_a_bytes(usefulData[1][i])
                
                return usefulData
        except FileNotFoundError:
            print ('El archivo no existe')
  
    def installApp (self, tel : ConfigParameters, telAppList : dict, name):
        """
        Instala la aplicacion dado el nombre
        Args:
            tel: Instancia de ConfigParameters del telefono
            name : Nombre de la aplicación
            telAppList: Diccionario del telefono donde instalar la app
        Notes:
            Cuidado con las instancias que se pasan, asi se evita
            instalar en un telefono incorrecto
         """
        if not isinstance(tel, ConfigParameters):       #Busca si se paso una clase incorrecta
            raise TypeError("Clase Incorrecta")
        
        if not tel.datos:                       #Se fija que este conectado a internet
            print("No hay conexion a internet")
            return None
        
        if name in telAppList.keys():      #Evita que se instale una aplicacion ya instalada
            print("Aplicacion ya instalada")
            return None
            
        elif name in self.availableAppsList[0]:
            
            i = 0
            while self.availableAppsList[0][i] != name:
                i += 1
            weight = self.availableAppsList[1][i]
            version = self.availableAppsList[2][i]
            if tel.almacenamiento < weight:
                print('Espacio insuficiente')
                return None          
            if not self.compareVersions(tel.version, version):
                print ('Posee un OS mas antiguo que el minimo')
                return None
            telAppList.update({name : Aplicacion(weight)})
            tel.almacenamiento -= weight 
        else:
            print("No existe esa aplicacion en la tienda")

        
    def uninstallApp (self, tel : ConfigParameters,telAppList : dict ,name):
        
        if isinstance(tel, ConfigParameters):
            if name in telAppList.keys():
                app : Aplicacion = telAppList.get(name)
                tel.almacenamiento += app.weight
                telAppList.pop(name)
            else:
                print("Aplicacion no instalada")
        else:
            raise TypeError ("Clase Incorrecta")

    @staticmethod
    def filterVersionList (versionList : list):
        
        for i in range (len(versionList)):
            versionList[i] = versionList[i].split(' ')
        
        filteredList = []
        for i in range(len(versionList)):
            if len(versionList[i]) == 0 :
                filteredList.append('')
            elif versionList[i][0] == 'Varies' or versionList[i][0] == 'NaN' or versionList[i][0] == '':
                filteredList.append('')
            elif versionList[i][1] == '-':
                filteredList.append(versionList[i][0])
            else:
                filteredList.append(versionList[i][0])
        
        return filteredList
    
    @staticmethod
    def compareVersions (ver1 : str, ver2 : str):
        """Compara que ver1 >= ver2
        Args:
            ver1 (str): Version del telefono
            ver2 (str): Version minima de la app
        """        
        if ver2 == '':
            return True
        
        ver1 = ver1.split('.')
        ver2 = ver2.split('.')
        
        if len(ver2) > len(ver1):
            ver1.append('0')
        elif len(ver2) < len(ver1):
            ver2.append('0')
        
        if ver1[0] < ver2[0]:
            return False
        elif (ver1[0] == ver2[0]):
            if (ver1[1] < ver2[1]):
                return False
            elif (ver1[1] == ver2[1]):
                if ver1[2] < ver2[2]:
                    return False
        
        return True