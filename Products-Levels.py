# -*- coding: utf-8 -*-
from Products.Products import Products
from Buildings.Buildings import Buildings
import Utils, re, os

"""
Скрипт строит визуальную схему продуктов
"""

""" Настройки """
# Путь к All_Products.xml
productsPath = "../../township/base/All_Products.xml"
buildingsPath = "../../township/base/buildings_v1.xml"

dotFileName = "Tmp/products.dot"
# Путь к graphViz
graphVizPath = "Bin\\"
# Путь, куда положить картинку с графом
outputFilePath = "products.png"

""" Парсим xml, создаем объекты """
# Продукты
products = Products()
products.load(productsPath)

buildings = Buildings()
buildings.load(buildingsPath)

# Разбор структуры квестов
# Финальный скрипт
script = []
script.append(u'digraph G { \nnode [fontname="Verdana"];')

script.append("subgraph structure { level_root; products_root; factories_root; }")
script.append("{ rank = same; level_root; products_root; factories_root; }")

script.append("{ rank = same; level_root; ")
for level in range(0,100):
	level_element = "LEVEL_"+str(level)
	script.append("{0}; ".format(level_element))
script.append("}")


script.append("{ rank = same; factories_root; ")
for factorynode in buildings.factorynode:
	for factory in factorynode.items:
		cur_factory_id = factory.buildingId
		script.append("{0}; ".format(cur_factory_id))
script.append("}")


script.append("subgraph levels {")
for level in range(1,100):
	prev_level = level-1
	#if prev_level>0:
	prev_level_element = "LEVEL_"+str(prev_level)
	level_element = "LEVEL_"+str(level)
	script.append("{0} -> {1};".format(prev_level_element, level_element))
script.append("}")


for level in range(0,100):
	level_element = "LEVEL_"+str(level)
	script.append("{0} [shape=box, style=filled, color=red]; ".format(level_element))

for product in products.products:
    cur_name = product.name
    cur_type = product.type
    cur_levelneed = "LEVEL_"+str(product.levelneed)
    script.append("{0} -> {1};".format(cur_levelneed, cur_name))
    if cur_type == "seed":
    	script.append("{0} [shape=invtriangle];".format(cur_name))



for factorynode in buildings.factorynode:
	for factory in factorynode.items:
		#print factory.buildingId
		cur_levelneed = "LEVEL_"+str(factory.levelneed)
		cur_factory_id = factory.buildingId
		script.append("{0} -> {1} [style=dotted];".format(cur_levelneed, cur_factory_id))
		script.append("{0} [shape=polygon,sides=4,distortion=.7];".format(cur_factory_id))




script.append(u"}")

#print script

# Команды для GraphViz записываем в файл
with open(dotFileName, 'w') as f:
    f.write('\n'.join(script).encode('utf-8').strip())

# Запускаем консольную утилиту
command = '"{0}dot.exe" -Tpng {1} -o {2}'.format(graphVizPath, os.path.abspath(dotFileName), os.path.abspath(outputFilePath))
os.system(command)
