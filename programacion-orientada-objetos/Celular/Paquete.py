from enum import Enum

class Intentions(Enum):
    REQUEST = 0
    BUSY = 1
    NOT_FOUND = 2
    OK = 3
    STOP = 4
    REJECTED = 5

class Paquete:
    def __init__(self, sender, receiver, datetime) -> None:
        self.sender = sender
        self.receiver = receiver
        self.datetime = datetime
        
class PaqueteSMS(Paquete):
    def __init__(self, sender, receiver, datetime, message) -> None:
        super().__init__(sender, receiver, datetime)
        self.message = message
        
class PaqueteLlamada(Paquete):
    
    def __init__(self, sender, receiver, datetime, intention) -> None:
        super().__init__(sender, receiver, datetime)
        self.intention = intention
        