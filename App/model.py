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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as omp
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import indexheap as ih
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
from datetime import datetime, time
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""


# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
   Num: Almacena El numero de viajes
   vertex: Mapa de los vertices segun lat y long
    """
    try:
        Service = {'Graph_Duration': gr.newGraph(datastructure='ADJ_LIST',
                                                 directed=True,
                                                 size=200,
                                                 comparefunction=compareStopIds),
                   "Map_Routes": mp.newMap(numelements=200,
                                           maptype="CHAINING",
                                           comparefunction=compareStopIds, loadfactor=0.9),
                   "Omap_Dates": omp.newMap(omaptype='RBT', comparefunction=compareOmpLst),

                   "num": 0
                   }
        return Service
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo

def tryConvert(text):
    try:
        return float(text)
    except:
        return False


def addStopConnection(Services, viaje):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """

    try:

        taxi_id, trip_total, trip_miles = viaje['taxi_id'], tryConvert(viaje['trip_total']), tryConvert(
            viaje['trip_miles'])
        origin, destination = viaje["pickup_community_area"], viaje["dropoff_community_area"]
        Ocurredt1, Ocurredt2 = viaje['trip_start_timestamp'], viaje['trip_end_timestamp']
        duration = tryConvert(viaje["trip_seconds"])

        if Ocurredt1:
            Ocurredt1 = toDatetimeC(Ocurredt1)
            if taxi_id and trip_miles and trip_total:
                addDate(Services['Omap_Dates'], Ocurredt1.date(), taxi_id, trip_total, trip_miles)
            if origin and destination and duration and Ocurredt2:
                Ocurredt2 = toDatetimeC(Ocurredt2)
                orgin_f, destination_f = (origin, Ocurredt1.time()), (destination, Ocurredt2.time())
                addVertexAndMapDuration(Services['Graph_Duration'], Services['Map_Routes'], orgin_f, destination_f,
                                        duration)
        return Services
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addDate(DateOmap, date, taxi_id, trip_total, trip_miles):
    """
    Args:
        DateOmap: omap de time
        date: datetime con el dia en que sucedio
        taxi_id:
        trip_total:
        trip_miles:
    """
    timeRoot = omp.get(DateOmap, date)
    if timeRoot is None:
        timeValue = {'map_taxis': mp.newMap(100, maptype='CHAINING', comparefunction=compareStopIds, loadfactor=0.9),
                     'count': 1}
        omp.put(DateOmap, date, timeValue)
    else:
        timeValue = timeRoot['value']
        timeValue['count'] += 1

    addTaxi(timeValue['map_taxis'], taxi_id, trip_total, trip_miles)

    return DateOmap


def addTaxi(map_taxis, taxi_id, trip_total, trip_miles):
    taxi = mp.get(map_taxis, taxi_id)
    if taxi is None:
        points_info = {'miles': trip_miles, 'payments': trip_total, 'services': 1}
        mp.put(map_taxis, taxi_id, points_info)
    else:
        points_info = taxi['value']
        points_info['miles'] += trip_miles
        points_info['payments'] += trip_total
        points_info['services'] += 1
    return map_taxis


def addVertexAndMapDuration(graph, map_routes, origin_f, destination_f, duration):
    gr.insertVertex(graph, origin_f)
    gr.insertVertex(graph, destination_f)
    if origin_f[0] == '76.0' and origin_f[1] == time(12, 00) and destination_f[0] == '8.0' and destination_f[1] == time(12, 00):
        print(duration)
    route_k = (origin_f, destination_f)
    route = mp.get(map_routes, route_k)
    if route is None:
        route_info = {'total_duration': duration, 'services': 1}
        mp.put(map_routes, route_k, route_info)
    else:
        route_info = route['value']
        route_info['total_duration'] += duration
        route_info['services'] += 1
    return map_routes


def addRoutes(Services):
    map_routes = Services['Map_Routes']
    graph_routes = Services['Graph_Duration']
    list_k = mp.keySet(map_routes)
    iter_k = it.newIterator(list_k)
    for _ in range(lt.size(list_k)):
        route_k = it.next(iter_k)
        route = mp.get(map_routes, route_k)
        route_info = route['value']
        prom = route_info['total_duration'] / route_info['services']
        vertexa, vertexb = route_k
        gr.addEdge(graph_routes, vertexa, vertexb, prom)


# ==============================
# Funciones de consulta
# ==============================

def mstInDate(DateOmap, date, n):
    dateEntry = omp.get(DateOmap, date)
    if dateEntry is None:
        return None
    dateValue = dateEntry['value']
    mapTaxis = dateValue['map_taxis']
    return mstsFreqTaxiInMap(mapTaxis, n)


def mstsInRangeDates(DateOmap, date1, date2, n):
    dates_range = omp.keys(DateOmap, date1, date2)
    iter_days = it.newIterator(dates_range)
    frequency_taxi = mp.newMap(loadfactor=0.9, comparefunction=compareStopIds)
    for _ in range(lt.size(dates_range)):
        date_k = it.next(iter_days)
        dateValue = omp.get(DateOmap, date_k)['value']
        mapTaxis = dateValue['map_taxis']
        taxis_ids = mp.keySet(mapTaxis)
        iter_taxis = it.newIterator(taxis_ids)
        for _ in range(lt.size(taxis_ids)):
            taxi_id = it.next(iter_taxis)
            taxi_info = mp.get(mapTaxis, taxi_id)['value']
            addTaxi(frequency_taxi, taxi_id, taxi_info['payments'], taxi_info['miles'])
    return mstsFreqTaxiInMap(frequency_taxi, n)


def bestTimeToGo(graph, origin, destination, hour1, hour2):
    ac_hour = hour1
    min_duration, search_r, recomend_go, end_go = None, None, None, None
    while ac_hour < hour2:
        origin_s = (origin, ac_hour)
        arr_hour = ac_hour
        search = djk.Dijkstra(graph, origin_s)
        while arr_hour < hour2:
            destination_s = (destination, arr_hour)
            if djk.hasPathTo(search, destination_s):
                duration = djk.distTo(search, destination_s)
                if min_duration is None or duration < min_duration:
                    min_duration = duration
                    recomend_go = ac_hour
                    end_go = arr_hour
                    search_r = search
                break
            arr_hour = nextTime(arr_hour)
        ac_hour = nextTime(ac_hour)
    camino = djk.pathTo(search_r, (destination, end_go))
    return {'hour': recomend_go, 'path': camino, 'time': min_duration}


# ==============================
# Funciones Helper
# ==============================
def mstsFreqTaxiInMap(mapTaxis, n):
    taxis_ids = mp.keySet(mapTaxis)
    iter_taxis = it.newIterator(taxis_ids)
    mstsfrq = lt.newList('ARRAY_LIST', compareOmpLst)
    for _ in range(lt.size(taxis_ids)):
        taxi_id = it.next(iter_taxis)
        taxi = mp.get(mapTaxis, taxi_id)
        taxi_info = taxi['value']
        points = taxi_info['miles'] / taxi_info['payments'] * taxi_info['services']
        insertInRank(mstsfrq, {'taxi_id': taxi_id, 'points': points}, order_aux_max, n)
    return mstsfrq


def insertInRank(rank, el, order, n):
    def iterIN(large):
        pos = large
        for i in range(1, large):
            if order(lt.getElement(rank, pos), lt.getElement(rank, pos - 1)):
                lt.exchange(rank, pos, pos - 1)
                pos = pos - 1
            else:
                break

    cen = False
    size = lt.size(rank)
    if size < n:
        size += 1
        lt.addLast(rank, el)
        cen = True
    else:
        if order(el, lt.getElement(rank, size)):
            lt.changeInfo(rank, size, el)
            cen = True
    if cen:
        iterIN(size)
    return rank


def nextTime(o_time):
    hour = o_time.hour
    minute = o_time.minute
    if minute < 45:
        minute = (minute + 15)
    elif hour != 23:
        minute = 0
        hour += 1
    new_time = time(hour, minute)
    return new_time


def toDatetimeD(text: str):
    return datetime.strptime(text, '%Y-%m-%d').date()


def toDatetimeC(text: str):
    return datetime.strptime(text, '%Y-%m-%dT%H:%M:%S.000')


def toDatetimeH(time_string):
    return time.fromisoformat(time_string)

# ==============================
# Funciones de Comparacion
# ==============================
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if stop == stopcode:
        return 0
    elif stop > stopcode:
        return 1
    else:
        return -1


def compareOmpLst(date1, date2):
    """
    Compara dos elementos
    """
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1


def order_aux_max(el1, el2):
    if el1['points'] < el2['points']:
        return 0
    else:
        return 1
