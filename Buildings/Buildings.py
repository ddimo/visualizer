# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et



class Buildings(object):    # собираем класс с factory - фактически такой элемент только один
    def __init__(self):
        self._factory = []

    # Загружает из по пути path
    def load(self, path):
        tree = et.parse(path)
        root = tree.getroot()
        for factoryElem in root.iter("factory"):    # для каждого элемента factory, хотя он всего 1
            factory = Factory()                     # создаем класс Factory в переменную factory
            factory.load(factoryElem)               # загружаем инфу в переменную factory через метод load объекта Factory
            self._factory.append(factory)           # возвращаемый "массив" фактически содержит в себе обработанную ноду factory

    @property
    def factory(self):
        return self._factory



class Factory(object):  # собираем класс с item'ами
    def __init__(self):
        self._item = []

    def load(self, elem):
        for itemElem in elem.iter("item"):  
            item = Item()                   
            item.load(itemElem)
            self._item.append(item)    

    @property
    def item(self):
        return self._item




class Item(object):     # берем ноду production из item'а и аттрибуты item'а
    def __init__(self):
        # собираем аттрибуты item'ов и ноду production
        self._levelneed = ""          
        self._buildingId = "" 
        self._production = []

    def load(self, elem):
        # elem - каждый <item> внутри <factory>
        self._levelneed = elem.get("levelneed")
        self._buildingId = elem.get("buildingId")

        for productionElem in elem.iter("production"):
            production = Production()
            production.load(productionElem)
            self._production.append(production)

    @property
    def levelneed(self):
        return self._levelneed

    @property
    def buildingId(self):
        return self._buildingId

    @property
    def production(self):
        return self._production




class Production(object):   # собираем ноды product из production
    def __init__(self):       
        self._product = []

    def load(self, elem):
        # elem - каждый (один) <production> внутри <item>
        for productElem in elem.iter("product"):
            product = Product()
            product.load(productElem)
            self._product.append(product)

    @property
    def product(self):
        return self._product




class Product(object):  # собираем ноды resourse + аттрибуты из product
    def __init__(self):
        self._name = ""          
        self._resource = []

    def load(self, elem):
        # elem - каждый <product> внутри <production>
        self._name = elem.get("name")

        for resourceElem in elem.iter("resource"):
            resource = Resource()
            resource.load(resourceElem)
            self._resource.append(resource)

    @property
    def name(self):
        return self._name

    @property
    def resource(self):
        return self._resource




class Resource(object): # собираем аттрибуты resource
    def __init__(self):
        self._name = ""

    def load(self, elem):
        self._name = elem.get("name")

    @property
    def name(self):
        return self._name



