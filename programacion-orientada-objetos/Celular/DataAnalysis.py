import csv
import numpy as np
import matplotlib.pyplot as pyplot
from enum import Enum


class Columnas(Enum):
    APP = 0
    CATEGORY = 1
    RATING = 2
    REVIEWS = 3
    SIZE = 4
    INSTALLS = 5
    TYPE = 6
    PRICE = 7
    CONTENT_RATING = 8
    GENRES = 9
    LAST_UPDATED = 10
    CURRENT_VER = 11
    ANDROID_VER = 12
    
class DataAnalysis:
    def __init__(self) -> None:
        self.rawData = self.getData('Play Store Data.csv')
        self.mendData()

    def getData (self, csvname : str):
        
        data = [[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ]
        
        ## [2], [3], [5] hacer arrays de int/float
        
        with open(csvname, 'r' , encoding = 'utf-8') as archivo:
            reader = csv.reader(archivo)
            next(reader,None) ##Saca los encabezados
            for line in reader:
                data[Columnas.APP.value].append(line[Columnas.APP.value])
                data[Columnas.CATEGORY.value].append(line[Columnas.CATEGORY.value])
                data[Columnas.RATING.value].append(line[Columnas.RATING.value])
                data[Columnas.REVIEWS.value].append(line[Columnas.REVIEWS.value])
                data[Columnas.SIZE.value].append(line[Columnas.SIZE.value])
                data[Columnas.INSTALLS.value].append(line[Columnas.INSTALLS.value][:-1:])
                data[Columnas.TYPE.value].append(line[Columnas.TYPE.value])
                data[Columnas.PRICE.value].append(line[Columnas.PRICE.value][1:]) ##Quizas quiera dejar los precios como estan, no esta claro
                data[Columnas.CONTENT_RATING.value].append(line[Columnas.CONTENT_RATING.value])
                data[Columnas.GENRES.value].append(line[Columnas.GENRES.value])
                data[Columnas.LAST_UPDATED.value].append(line[Columnas.LAST_UPDATED.value])
                data[Columnas.CURRENT_VER.value].append(line[Columnas.CURRENT_VER.value])
                data[Columnas.ANDROID_VER.value].append(line[Columnas.ANDROID_VER.value])
            return data
    
    def mendData(self):
        self.rawData[Columnas.RATING.value] = self.mendRating(self.rawData[Columnas.RATING.value])
        self.rawData[Columnas.REVIEWS.value] = self.mendReviews(self.rawData[Columnas.REVIEWS.value])
        self.rawData[Columnas.INSTALLS.value] = self.mendInstalls(self.rawData[Columnas.INSTALLS.value])
    
    def mendReviews (self, reviewsList):
        return np.array(reviewsList)
     
    def mendRating(self, ratingList):
        
        changedList = []
        
        for number in ratingList:
            
            if number in ['NaN', ''] :
                changedList.append(float(0))
            else:
                changedList.append(float(number))
                
        array = np.array(changedList)
        return array
        
    def mendInstalls (self, installList):
        
        changedList = []
        
        for number in installList:
            
            if number in ['']:
                changedList.append(0)
            else:
                number = number.split(',')
                realnumber = ''
                for part in number:
                    realnumber += part
                
            realnumber = int(realnumber)
            changedList.append(realnumber)
        
        array = np.array(changedList)
        return array

    def paidPieChart(self):
        
        categories = []
        for cat in self.rawData[Columnas.CATEGORY.value]:
            if cat not in categories:
                categories.append(cat)
                
        appCount = np.array([0] * len(categories))
        
        for row in range(len(self.rawData[Columnas.APP.value])):
            if self.rawData[Columnas.TYPE.value][row] == 'Paid':
                index = categories.index(self.rawData[Columnas.CATEGORY.value][row])
                appCount[index] += 1
        
        appCount = appCount.astype('float64')
        totalPaidAppCount = appCount.sum()
        
        filteredPercentage = []
        filteredCategories = []
        for cell in range(appCount.size):
            appCount[cell] = (appCount[cell] * 100) / totalPaidAppCount
            if appCount[cell] >= float(1):
                filteredPercentage.append(appCount[cell])
                filteredCategories.append(categories[cell])
        
        filteredArray = np.array(filteredPercentage)
        
        ##Cantidad de apps pagas por categoria, con proporcion mayores uqe 1%
        
        pyplot.pie(filteredArray, labels= filteredCategories)
        pyplot.legend( title = 'Categorias:')
        pyplot.show()
        
    def paidMedian(self):
        
        appPrices = []
        
        for i in range(len(self.rawData[Columnas.APP.value])):
            if self.rawData[Columnas.TYPE.value][i] == 'Paid':
                appPrices.append(float(self.rawData[Columnas.PRICE.value][i]))
                
        pricesArray = np.array(appPrices)
        median = np.median(pricesArray)
        
        print(f'El precio mas visto es ${median}')
        
        return True
    
    def installsPerCategory(self):
        
        categories = []
        for cat in self.rawData[Columnas.CATEGORY.value]:
            if cat not in categories:
                categories.append(cat)
                
        appInstals = np.array([0] * len(categories))
                
        for row in range(len(self.rawData[Columnas.APP.value])):
            index = categories.index(self.rawData[Columnas.CATEGORY.value][row])
            appInstals[index] += self.rawData[Columnas.INSTALLS.value][row]
            
        x, y = list(zip(*sorted(zip(appInstals,categories))))    
        
        print("TOP 5 CATEGORIAS MCON MAS DESCARGAS:")
        for i in range(1,6):
            print(f'{i}. {y[-i]}, {x[-i]} Descargas')
        
        pyplot.ylabel('Categorias')
        pyplot.xlabel('Descargas')
        pyplot.barh(y, x)
        pyplot.show()