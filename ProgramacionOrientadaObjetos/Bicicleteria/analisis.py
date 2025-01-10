import numpy as np

#FUNCIONES GENERALES PARA INTERPRETAR LA INFORMACION DEL ARCHIVO "bicicletas.csv"
def leer(nombre_archivo) :
    '''
    Funcion que recibe el nombre de un archivo y devuelve su contenido como un array
    '''
    try :
        datos = np.genfromtxt(nombre_archivo, delimiter=',',skip_header=1, dtype=str, encoding=None )
        return datos
    except :
        return None

def analisis_por_comuna():
    '''
    Analisis 1: Evalua la cantidad de usos por comuna del archivo y determina las tres comunas con mayor demanda en las que conviene invertir abriendo otra bicicletería
    '''
    datos = leer('bicicletas.csv')
    if datos is not None :    
        comunas = np.array( list( map( int , datos[:, 5] ) ) )
        mejores_comunas = []
        
        counts = np.bincount(comunas)
        for i in range(3) :   
            mejor_comuna = np.argmax(counts)
            mejores_comunas.append([mejor_comuna , counts[mejor_comuna] ])
            counts[mejor_comuna] = 0
    
        dict_comunas = {i: counts[i] for i in range(1, 16)}
        
        return dict_comunas , mejores_comunas
    
    return None, None

def generos() :
    '''
    Análisis 2: Evalua la cantidad de usos por genero y determina cual es las utiliza en menor cantidad para proponer descuentos
    '''
    datos = leer('bicicletas.csv')
    if datos is not None :
        datos = np.array( list ( map( lambda genero : int(genero=='FEMENINO') , datos[:, 2 ]) ) )
        generos = np.bincount(datos)
        dicc = {'Masculino': generos[0] , 'Femenino': generos[1]}
        menos_uso = [ 'Femenino' if np.argmin(generos) == 1 else 'Masculino' ][0]

        return dicc , menos_uso
    
    return None, None
 
def usos_por_edad() :
    '''
    Analisis 3: Evalua la cantidad de usos por edad y determina las tres edades con mayor demanda para proponer descuentos
    '''
    datos = leer('bicicletas.csv')
    if datos is not None :
            
        edades = np.array(list( map( int , datos[:, 1] )))
        
        usos_por_edad = np.bincount( edades )
        mejores_edades=[]
        for i in range(3) :   
            mejor_edad = np.argmax(usos_por_edad)
            mejores_edades.append([ mejor_edad , usos_por_edad[mejor_edad] ])
            usos_por_edad[mejor_edad] = 0

        dicc = {i: usos_por_edad[i] for i in range(len(usos_por_edad))}
        
        return dicc , mejores_edades
    
    return None, None
    
def usos_por_hora() :
    '''
    Analisis 4: Evalua la cantidad de usos por hora del dia para establecer las tres horas pico y recomendar un aumento de las tarifas en esas horas
    '''
    datos = leer( 'bicicletas.csv' )    
    if datos is not None : 
        datos = np.array( list(map( int , datos[ : , 9] )) )
        
        cantidades =  np.bincount( datos )
        
        mejores_horas = []
        for i in range(3) :   
            mejor_hora = np.argmax(cantidades)
            mejores_horas.append(mejor_hora )
            cantidades[mejor_hora] = 0

        dicc = { x : cantidades[x] for x in range(len(cantidades)) if cantidades[x] > 0 }
        
        return dicc , mejores_horas
    
    return None, None

            