import csv
#from TP_EDP import Telefono

#cambiar algunas cosas de los archivos auxiliares
def createFile(archivo, filas_iniciales): # funcion que crea UN archivo EN CASO DE QUE NO EXISTA
    try:
        with open(archivo, 'x', encoding='utf-8', newline='') as arch:
            escritor = csv.writer(arch)
            escritor.writerow(filas_iniciales)  # Escribir encabezados
            return 
    except FileExistsError:
        return


def extractFile(archivo_csv):
    telefonos = dict()
    try:
        with open(archivo_csv, mode='r', newline='') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Saltar encabezados
            for telefono in lector_csv:
                telefonos[telefono[0]] = Telefono(telefono[0], telefono[1], telefono[2], telefono[3],
                                                    telefono[4], telefono[5], int(telefono[6]), telefono[7])
                
        print("Todos los teléfonos han sido registrados desde el archivo CSV.")
        return telefonos
    except FileNotFoundError:
        print("El archivo CSV no fue encontrado.")
    except KeyError as e:
        print(f"Error en el archivo CSV. Faltan columnas: {e}")
    except Exception as e:
        print(f"Se produjo un error al leer el archivo CSV: {e}")

def updateFiles(self):
    with open('telefonos.csv', 'w', encoding='utf-8', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['ID', 'NOMBRE', 'MODELO', 'OS', 'VERSION', 'RAM', 'ALMACENAMIENTO', 'NUMERO'])  # Escribir encabezados
        for telefono in self.telefonos.values():
            escritor.writerow([telefono.id, telefono.configParameters.nombre, telefono.model, telefono.os,
                                telefono.version, telefono.ram, telefono.almacenamiento, telefono.numero])

class Nodo:
    def __init__(self, value):
        self.valor = value
        self.prox = None
    def __eq__(self , other) :
        return self.valor == other.valor

    def __str__(self) :
        return str(self.valor)
    
class ListaEnlazada:
    def __init__(self):
        self.head = None
        self.listSize = 0
    def is_empty(self):
        return self.head is None

    def size(self) :
        return self.listSize

    def __getitem__(self , i : int) :
        if self.size() > i :
            current = self.head
            for n in range(i) :
                current = current.prox
            return current.valor
        
    def __iter__(self) :
        list = []
        current = self.head
        for i in range(self.size()) :
            list.append(current)
            current = current.prox
        return iter(list)
    
    def __contains__(self , value) :
        for i in self :
            if i.valor == value :
                return True
        return False
    
    def add_to_start(self, value): # Forma 1: Pasamos el valor del nodo y lo instanciamos
        new_node = Nodo(value)
        new_node.prox = self.head
        self.head = new_node
        self.listSize += 1

    def add_to_end(self, value): # Forma 2: Pasamos el nodo a linkear
        new_node = Nodo(value)
        self.listSize += 1
        if self.is_empty():
            self.head = new_node
            return
        current = self.head
        while current.prox:
            current = current.prox
        current.prox = new_node

    def pop(self):
        '''
        Este método pop devuelve el valor del nodo head y lo desenlaza de la lista.
        Ojo! En general el método pop devuelve el último nodo de la lista. Siempre revisar la
        implementación y/o la documentación de los métodos.
    
        '''
        if self.is_empty():
            return None
        popped_value = self.head.valor
        self.head = self.head.prox
        self.listSize -= 1
        return popped_value

    def delete(self, value):
        '''
        Este método busca el primer nodo cuyo valor se corresponde al argumento y lo desenlaza. 
        Tendría sentido hacer referencia al nodo directamente en lugar de su valor?
        '''
        if self.is_empty():
            return
        if self.head.valor == value:
            self.head = self.head.prox
            self.listSize -= 1
            return

        current = self.head
        while current.prox:
            if current.prox.valor == value:
                current.prox = current.prox.prox
                self.listSize -= 1
                return
            current = current.prox

    def __str__(self):
        text = ""
        current = self.head
        while current:
            text += str(current.valor) + " -> "
            current = current.prox
        text += "None" # De qué otra manera podríamos agregarlo ?
        return text

    def replace( self , oldValue , newValue ) :
        if oldValue in self :
            newnod = Nodo(newValue)
            if self.head.valor == oldValue :
                newnod.prox = self.head.prox
                self.head = newnod
                return
            current = self.head
            if self.head.valor != oldValue :
                while current.prox.valor != oldValue :
                    current = current.prox
            newnod.prox = current.prox.prox
            current.prox = newnod