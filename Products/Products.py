# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
from Product import Product

"""
Список всех продуктов
"""
class Products(object):
    def __init__(self):
        self._products = []         # Список продуктов

    # Загружает из по пути path
    def load(self, path):
        tree = et.parse(path)
        elem = tree.getroot()
        for productElem in elem.iter("product"):
            product = Product()
            product.load(productElem)
            self._products.append(product)

    @property
    def products(self):
        return self._products
