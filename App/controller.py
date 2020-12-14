"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import os
from timeit import default_timer as dt
import csv
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from time import perf_counter
from DISClib.DataStructures import listiterator as it

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""


# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def incializar():
    return model.newAnalyzer()


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    i = 1
    for service in input_file:
        if i % 100000 == 0:
            print(i, 'servicios cargados')
        model.addStopConnection(analyzer, service)
        i += 1
    print('añadiendo ruta')
    model.addRoutes(analyzer)
    model.admpqs(analyzer["Map_Companies"],
                 analyzer['Maxpq-Afiliados-Compañias-services'],
                 analyzer['Maxpq-Afiliados-Compañias-taxis'])
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def partB_1(cont, date, n):
    date = model.toDatetimeD(date)
    return model.mstInDate(cont['Omap_Dates'], date, int(n))


def partB_2(cont, date1, date2, n):
    date1, date2 = model.toDatetimeD(date1), model.toDatetimeD(date2)
    return model.mstsInRangeDates(cont['Omap_Dates'], date1, date2, int(n))


def partC(cont, comunityA, comunityB, hour1, hour2):
    hour1 = model.toDatetimeH(hour1)
    hour2 = model.toDatetimeH(hour2)
    return model.bestTimeToGo(cont['Graph_Duration'], comunityA, comunityB, hour1, hour2)


def A(analyzer, n_top_taxis, n_top_services):
    n_top_services = int(n_top_services)
    n_top_taxis = int(n_top_taxis)
    size = m.size(analyzer['Map_Companies'])
    if n_top_services > size:
        n_top_services = size
    if n_top_taxis > size:
        n_top_taxis = size
    lista_final = lt.newList()
    lista_top_taxis_compani = model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-taxis'],
                                               n_top_taxis)
    lista_top_services_compani = model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-services'],
                                                  n_top_services)
    lt.addLast(lista_final, lista_top_services_compani)
    lt.addLast(lista_final, lista_top_taxis_compani)
    return lista_final


def search(analyzer, key, pos):
    compania_info = m.get(analyzer["Map_Companies"], key)["value"]
    if pos == 1:
        n_servicios = lt.getElement(compania_info, 2)
        n_servicios = m.size(n_servicios)
    elif pos == 0:
        n_servicios = lt.getElement(compania_info, 1)
    return n_servicios


def re(analyzer, lista):
    mapa = analyzer['Map_Companies']
    minpq1 = analyzer['Maxpq-Afiliados-Compañias-services']
    minpq2 = analyzer['Maxpq-Afiliados-Compañias-taxis']
    f = 0
    iterador2 = it.newIterator(lista)
    while it.hasNext(iterador2):
        next_list = it.next(iterador2)
        if f == 0:
            model.rehacer(next_list, mapa, minpq1, 1)
            f += 1
        else:
            model.rehacer(next_list, mapa, minpq2, 2)
