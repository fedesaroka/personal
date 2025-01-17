#Clase aplicacion y derivados

class Aplicacion:
    def __init__(self, weight : int) -> None: # weight en bytes 
        self.isOpen = False
        self.weight = self.tamanio_a_bytes(weight)

    def onOff (self):
        self.isOpen = not self.isOpen
        
    @staticmethod
    def tamanio_a_bytes(tamanio_formateado):
        
        """Convierte una cadena de tamaño formateado (ej. "117.74 MB") a su valor en bytes.
        Args:
            tamanio_formateado (str): Tamaño en formato de cadena con sufijo (ej. "1.5 GB").
        Returns:
            int: El tamaño convertido a bytes.
        Raises:
            ValueError: Si el formato de entrada no es válido.
        """        
        # Arreglo temporal, posiblemente se altere el csv
        if tamanio_formateado == 'Varies with device':
            tamanio_formateado = '0 K'
            
        if isinstance(tamanio_formateado, int):
            return int(float(tamanio_formateado))
        
        # Quitar espacios, convertir a mayúsculas, y eliminar la letra "B" si existe
        tamanio_formateado = tamanio_formateado.replace(" ", "").upper().replace("B", "")

        # Diccionario de sufijos y su potencia de 1024 correspondiente
        sufijos = {"K": 1, "M": 2, "G": 3, "T": 4, "P": 5}

        # Recorrer el diccionario para encontrar el sufijo que coincida al final de la cadena
        for sufijo, potencia in sufijos.items():
            if tamanio_formateado.endswith(sufijo):
                # Extraer la parte numérica y convertirla a float
                valor = float(tamanio_formateado[:-len(sufijo)])
                # Calcular el tamaño en bytes usando la potencia de 1024
                return int(valor * (1024 ** potencia))

        # Si no hay sufijo (es decir, el valor está en bytes), convertir directamente
        return int(float(tamanio_formateado))