# -*- coding: utf-8 -*-
from Products.Products import Products
from Buildings.Buildings import Buildings
import Utils, re, os

"""
Скрипт строит визуальную схему продуктов
"""

""" Настройки """
# Путь к All_Products.xml
productsPath = "../township/base/All_Products.xml"
buildingsPath = "../township/base/buildings_v1.xml"

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
seeds = []
script = []
script.append(u'digraph G { \nnode [fontname="Verdana"];')
script.append("seeds_root -> level_root -> products_root -> factories_root -> bottom_root;")

script.append("{ rank = same;")
script.append(" level_root;")
for level in range(0,100):
	level_element = "LEVEL_"+str(level)
	script.append(" {0};".format(level_element))
script.append("}")


script.append("{ rank = same;")
script.append(" factories_root;")
for factory in buildings.factory:
	for factory in factory.item:
		cur_factory_id = factory.buildingId
		script.append(" {0};".format(cur_factory_id))
script.append("}")


# создаем элементы-левелапы красными прямоугольниками
for level in range(0,100):
	level_element = "LEVEL_"+str(level)
	script.append("{0} [shape=box, style=filled, color=red]; ".format(level_element))

# рисуем строку левелапов
for level in range(1,100):
	prev_level = level-1
	prev_level_element = "LEVEL_"+str(prev_level)
	level_element = "LEVEL_"+str(level)
	script.append("{0} -> {1} [style=dotted];".format(prev_level_element, level_element))

# рисуем связи продуктов с левелапами
for product in products.products:
    cur_name = product.name
    cur_type = product.type
    cur_levelneed = "LEVEL_"+str(product.levelneed)
    script.append("{0} -> {1};".format(cur_levelneed, cur_name))

    if cur_type == "seed":
    	seeds.append(cur_name)
    	script.append("{0} [shape=invtriangle];".format(cur_name))

    if isinstance(product.event,str):
    	script.append("{0} [color=lightgoldenrod,style=filled];".format(cur_name))
    else:
		script.append("{0} [color=lightblue,style=filled];".format(cur_name))

script.append("{ rank = same;")
script.append(" seeds_root;")
for seed_id in seeds:
	script.append(" {0};".format(seed_id))
script.append("}")



used_products = []

for factory in buildings.factory:
	for item in factory.item:
		cur_levelneed = "LEVEL_"+str(item.levelneed)
		cur_factory_id = item.buildingId
		script.append("{0} -> {1} [style=dashed];".format(cur_levelneed, cur_factory_id))
		script.append("{0} [shape=polygon,sides=4,distortion=.7,color=orange,style=filled];".format(cur_factory_id))

		for production in item.production:
			for product in production.product:
				# print product.name
				cur_product = "f_"+product.name
				used_products.append(cur_product)
				script.append("{0} -> {1} [style=dotted,arrowhead=invdot];".format(cur_factory_id, cur_product))
				#for resource in product.resource:
					# print resource.name
					# script.append("{0} -> {1} [style=dotted];".format(cur_resource, cur_product))


# script.append("{ rank = same;")
# script.append(" bottom_root;")
# for used_product in used_products:
# 	script.append(" {0};".format(used_product))
# script.append("}")





script.append(u"}")

#print script

# Команды для GraphViz записываем в файл
with open(dotFileName, 'w') as f:
    f.write('\n'.join(script).encode('utf-8').strip())

# Запускаем консольную утилиту
command = '"{0}dot.exe" -Tpng {1} -o {2}'.format(graphVizPath, os.path.abspath(dotFileName), os.path.abspath(outputFilePath))
os.system(command)
