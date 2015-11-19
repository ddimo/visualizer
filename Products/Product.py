# -*- coding: utf-8 -*-

"""
Продукт
"""
class Product(object):
    def __init__(self):
        self._build_time = ""   # Время производства
        self._exp = ""          # exp
        self._levelneed = ""    # levelneed
        self._name = ""         # name

    # elem - <quest>
    def load(self, elem):
        self._build_time = elem.get("build_time")
        self._exp = elem.get("exp")
        self._levelneed = elem.get("levelneed")
        self._name = elem.get("name")
        self._type = elem.get("type")

    @property
    def build_time(self):
        return self._build_time

    @property
    def exp(self):
        return self._exp

    @property
    def levelneed(self):
        return self._levelneed

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type