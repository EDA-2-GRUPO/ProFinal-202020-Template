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
    for service in input_file:
        analyzer["num"] += 1
        model.addStopConnection(analyzer, service)
        taxi_id = service["taxi_id"]
        compania= service["company"]
        model.addtaxi(taxi_id, analyzer["taxis"])
        model.addcompania(compania,taxi_id,analyzer)
    model.addRoutes(analyzer)
    model.admpqs(analyzer["compcont"], 
    analyzer['Maxpq-Afiliados-Compañias-services'],
    analyzer['Maxpq-Afiliados-Compañias-taxis']) 
    return analyzer

        
       
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
def A(analyzer,n_top_taxis,n_top_services):
    n_top_services=int(n_top_services)
    n_top_taxis=int(n_top_taxis)
    lista_final=lt.newList()
    lista_top_taxis_compani=model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-taxis'],
                                            n_top_taxis)
    lista_top_services_compani=model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-services'],
                                                n_top_services)
    lt.addLast(lista_final, lista_top_services_compani)
    lt.addLast(lista_final, lista_top_taxis_compani)
    return lista_final
def search(analyzer, key,pos):
    compania_info=m.get(analyzer["compcont"], key)["value"]
    if pos ==1:
       n_servicios=lt.getElement(compania_info,2)
       n_servicios=m.size(n_servicios)
    elif pos ==0:
       n_servicios=lt.getElement(compania_info,1)
    return n_servicios

    
    

