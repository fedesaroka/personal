import csv
import customtkinter as ctk
from datetime import datetime, date
from typing import Literal
from matplotlib.figure import Figure

# MANEJO DE ARCHIVOS
def crear_archivo( fname : str , filas_predeterminadas : list[list[str]] ):
    '''
    Recibe el nombre de un archivo y sus filas iniciales y lo crea.
    Si ya existe no se crea
    '''
    try :
        with open( fname , 'x' , encoding='utf-8' , newline='' ) as arch :
            escritor = csv.writer(arch)
            for fila in filas_predeterminadas :
                escritor.writerow(fila)
            return 
    except FileExistsError :
        return


# FORMATEO DE FECHAS
def dt_to_str(fecha : datetime) :
    '''
    Convierte un objeto datetime 
    en fecha de formato '%d/%m/%Y %H:%M:%S'
    '''
    return fecha.strftime('%d/%m/%Y %H:%M:%S')

def d_to_str(fecha : date) :
    '''
    Convierte un objeto date 
    en fecha de formato '%d-%m-%Y'
    '''
    return fecha.strftime("%d-%m-%Y")

def str_to_dt(fecha : str) :
    '''
    Convierte una fecha en formato '%d/%m/%Y %H:%M:%S'
    a objeto datetime
    '''
    return datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S')

def str_to_d(fecha : str) :
    '''
    Convierte una fecha en formato '%d/%m/%Y %H:%M:%S'
    a objeto del tipo date
    '''
    return datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S').date()


# GRAFICOS
def graficos(tipo : Literal['pie','plot','bars'], datos : dict, titulo : str, xlabel : str = None, ylabel : str = None) :
    '''
    Funcion que genera distintos tipos de graficos dependiendo de los parametros que recibe
    '''
    fig = Figure(figsize=(12, 6), dpi=100)
    match tipo :
        case 'pie':
            grafico = fig.add_subplot(111)
            grafico.pie(datos.values(), labels=[ f'{categoria} ({cantidad})' for categoria,cantidad in datos.items()],autopct='%1.2f%%')
        case 'plot':
            grafico = fig.add_subplot(111)
            grafico.set_xlabel(xlabel)
            grafico.set_ylabel(ylabel)
            grafico.plot(datos.keys(), datos.values(), color='blue', linewidth=1)
        case 'bars':
            grafico = fig.add_subplot(111)
            grafico.set_xlabel(xlabel)
            grafico.set_ylabel(ylabel)
            grafico.bar(datos.keys(), datos.values(), color='blue', linewidth=1)

    grafico.set_title(titulo, loc='center', fontdict={'fontsize':10,'color':'black'})
    
    return fig

    
# INTERFAZ
def pack( *args , **kwargs ) :
    '''
    Funcion para ejecutar el metodo "pack" con multiples widgets de customtkinter
    '''
    pady = kwargs.get('pady')
    padx = kwargs.get('padx')
    
    for arg in args :
        arg : ctk.CTkBaseClass
        arg.pack(   pady = (20,0) if pady is None else pady , 
                    padx = 10 if padx is None else padx )
  
def pack_forget( *args ) :
    '''
    Funcion para ejecutar el metodo "pack_forget" con multiples widgets de customtkinter
    '''
    for arg in args :
        if isinstance( arg , list ) :
            
            for widget in arg :
                
                widget : ctk.CTkBaseClass
                widget.pack_forget()
                widget.place_forget()
                
        else :       
            
            arg : ctk.CTkBaseClass
            arg.pack_forget()
