# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
# from Factory import Factory


class Buildings(object):
    def __init__(self):
        self._factorynode = []

    # Загружает из по пути path
    def load(self, path):
        tree = et.parse(path)
        root = tree.getroot()
        for factoryElem in root.iter("factory"):    # для каждого элемента factory, хотя он всего 1
            factory = Factories()                   # создаем класс Factories в переменную factory
            factory.load(factoryElem)               # загружаем инфу в переменную factory через метод load объекта Factory
            self._factorynode.append(factory)           # возвращаемый "массив" фактически содержит в себе обработанную ноду factory

    @property
    def factorynode(self):
        return self._factorynode





class Factories(object):
    def __init__(self):
        self._items = []

    def load(self, elem):
        for itemElem in elem.iter("item"):  # обрабатываем элементы item только внутри ноды factory
            item = Item()                   # создаем класс Item
            item.load(itemElem)
            self._items.append(item)    # возвращаемый массив будет содержать в себе все item'ы ноды factory

    @property
    def items(self):
        return self._items




class Item(object):
    def __init__(self):
        self._levelneed = ""          
        self._buildingId = ""    

    def load(self, elem):
        # elem - каждый <item> внутри <factory>
        self._levelneed = elem.get("levelneed")
        self._buildingId = elem.get("buildingId")

    @property
    def levelneed(self):
        return self._levelneed

    @property
    def buildingId(self):
        return self._buildingId
