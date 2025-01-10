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
        
    def __str__(self):
        text = ""
        current = self.head
        while current:
            text += str(current.valor) + " -> "
            current = current.prox
        text += "None" 
        return text
        
    def is_empty(self):
        return self.head is None

    def size(self) :
        return self.listSize

    def add_to_start(self, value):
        new_node = Nodo(value)
        new_node.prox = self.head
        self.head = new_node
        self.listSize += 1

    def add_to_end(self, value):
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
        Devuelve el valor del nodo head y lo desenlaza de la lista.
        '''
        if self.is_empty():
            return None
        popped_value = self.head.valor
        self.head = self.head.prox
        self.listSize -= 1
        return popped_value


