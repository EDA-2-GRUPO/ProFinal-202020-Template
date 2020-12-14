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
from DISClib.ADT import map as m
from DISClib.ADT import indexminpq as pq
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import indexheap as ih
from DISClib.Algorithms.Sorting.insertionsort import insertionSort
from datetime import datetime, time
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from time import perf_counter

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
        Services = {'Graph_Duration': gr.newGraph(datastructure='ADJ_LIST',
                                                  directed=True,
                                                  size=200,
                                                  comparefunction=compareStopIds),
                    "Map_Routes": mp.newMap(numelements=200,
                                            comparefunction=compareStopIds, loadfactor=0.5),
                    "Omap_Dates": omp.newMap(omaptype='RBT', comparefunction=compareOmpLst),
                    'taxis': m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareMp),
                    'Map_Companies': m.newMap(numelements=200,
                                              comparefunction=compareMp),
                    'Maxpq-Afiliados-Compañias-services': pq.newIndexMinPQ(compareMp),
                    'Maxpq-Afiliados-Compañias-taxis': pq.newIndexMinPQ(compareMp),
                    "Num Services": 0}
        return Services
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo


def addStopConnection(Services, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """

    try:

        taxi_id, trip_total, trip_miles = service['taxi_id'], tryConvert(service['trip_total']), tryConvert(
            service['trip_miles'])
        origin, destination = service["pickup_community_area"], service["dropoff_community_area"]
        Ocurredt1, Ocurredt2 = service['trip_start_timestamp'], service['trip_end_timestamp']
        duration = tryConvert(service["trip_seconds"])
        compania = service["company"]

        if taxi_id:
            addTaxi(taxi_id, Services['taxis'])
            if not compania:
                compania = 'Independent Owner'
            addCompany(compania, taxi_id, Services["Map_Companies"])
        if Ocurredt1:
            Ocurredt1 = toDatetimeC(Ocurredt1)
            if taxi_id and trip_miles and trip_total:
                # addDate(Services['Omap_Dates'], Ocurredt1.date(), taxi_id, trip_total, trip_miles)
                pass
            if origin and destination and duration and Ocurredt2:
                Ocurredt2 = toDatetimeC(Ocurredt2)
                orgin_f, destination_f = (origin, Ocurredt1.time()), (destination, Ocurredt2.time())
                if orgin_f == ('52.0', time(0, 30)):
                    print(orgin_f, destination_f )
                addVertexAndMapDuration(Services['Graph_Duration'], Services['Map_Routes'], orgin_f, destination_f,
                                        duration)
        return Services
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def format_station(station, hour: time):
    return station + '-' + str(hour.hour) + ':' + str(hour.minute)


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
        timeValue = {'map_taxis': mp.newMap(100, maptype='PROBING', comparefunction=compareStopIds, loadfactor=0.9),
                     'count': 1}
        omp.put(DateOmap, date, timeValue)
    else:
        timeValue = timeRoot['value']
        timeValue['count'] += 1

    addTaxiPoints(timeValue['map_taxis'], taxi_id, trip_total, trip_miles)

    return DateOmap


def addTaxiPoints(map_taxis, taxi_id, trip_total, trip_miles):
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
        if vertexa == ('52.0', time(0, 30)):
            print(vertexb)
        gr.addEdge(graph_routes, vertexa, vertexb, prom)


def addTaxi(taxi_id, analizer):
    if not m.contains(analizer, taxi_id):
        m.put(analizer, taxi_id, 0)
        return analizer


def addCompany(compania, taxi_id, map_compania):
    if m.contains(map_compania, compania):
        compania_info = m.get(map_compania, compania)["value"]
        n_servicios = lt.getElement(compania_info, 1)
        n_servicios += 1
        lt.changeInfo(compania_info, 1, n_servicios)
        map_taxis = lt.getElement(compania_info, 2)
        if not m.contains(map_taxis, taxi_id):
            m.put(map_taxis, taxi_id, 0)
            return map_compania
        return map_compania
    else:
        compania_info = lt.newList()
        map_taxis = m.newMap(numelements=40,
                             maptype='PROBING',
                             comparefunction=compareMp)
        addTaxi(taxi_id, map_taxis)
        # añade todo a Map_Companies
        lt.addLast(compania_info, 1)
        lt.addLast(compania_info, map_taxis)
        m.put(map_taxis, taxi_id, 0)
        m.put(map_compania, compania, compania_info)


def admpqs(map_companies, maxpq_ntaxis, maxpq_nservices):
    lista_companias = m.keySet(map_companies)
    iterador = it.newIterator(lista_companias)
    while it.hasNext(iterador):
        next_compani = it.next(iterador)
        compani_info = m.get(map_companies, next_compani)["value"]
        map_taxis = lt.getElement(compani_info, 2)
        numero_servicios_compani = lt.getElement(compani_info, 1)
        numero_taxis_compani = m.size(map_taxis)
        # add_to_maxpqs
        pq.insert(maxpq_ntaxis, next_compani, 1000000 / numero_taxis_compani)
        pq.insert(maxpq_nservices, next_compani, 1000000 / numero_servicios_compani)


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
            addTaxiPoints(frequency_taxi, taxi_id, taxi_info['payments'], taxi_info['miles'])
    return mstsFreqTaxiInMap(frequency_taxi, n)


def bestTimeToGo(graph, origin, destination, hour1, hour2):
    ac_hour = hour1
    min_duration, search_r, recomend_go, end_go = None, None, None, None
    while ac_hour < hour2:
        origin_s = (origin, ac_hour)
        arr_hour = ac_hour
        t1 = perf_counter()
        search = djk.Dijkstra(graph, origin_s)
        t2 = perf_counter()
        print(t2 - t1)
        max_p_d, min_p_d = 900, 0
        while arr_hour != nextTime(arr_hour) and (min_duration is None or min_p_d < min_duration):
            destination_s = (destination, arr_hour)
            if djk.hasPathTo(search, destination_s):
                duration = djk.distTo(search, destination_s)
                if viableTime(ac_hour, arr_hour, duration / 60, max_p_d / 60):
                    if min_duration is None or duration < min_duration:
                        min_duration = duration
                        recomend_go, end_go = ac_hour, arr_hour
                        search_r = search
                    if duration <= max_p_d:
                        break
            min_p_d, max_p_d = max_p_d, max_p_d + 900
            arr_hour = nextTime(arr_hour)
        ac_hour = nextTime(ac_hour)

    if min_duration is None:
        return None
    camino = djk.pathTo(search_r, (destination, end_go))
    return {'hour': recomend_go, 'path': camino, 'time': min_duration}


def rank_maxpq(maxpq, numero):
    lista_companies = lt.newList()
    for a in range(0, numero):
        llave = pq.min(maxpq)
        pq.delMin(maxpq)
        lt.addLast(lista_companies, llave)
    return lista_companies


# ==============================
# Funciones Helper
# ==============================
def rehacer(lista, mapa_companies, pq, pos):
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        nextc = it.next()
        if pos == 0:
            numero = lt.get(m.get(mapa_companies, nextc), pos)
        else:
            mapa = lt.get(m.get(mapa_companies, nextc), pos)
            numero = m.size(mapa)
        pq.insert(pq, nextc, numero)


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
    size = lt.size(rank)
    pos = size + 1
    while pos > 1:
        if order(el, lt.getElement(rank, pos - 1)):
            pos -= 1
        else:
            break
    if pos <= n:
        lt.insertElement(rank, el, pos)
        if size >= n:
            lt.removeLast(rank)
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


def tryConvert(text):
    try:
        return float(text)
    except ValueError:
        return False


def viableTime(t1, t2, d, p):
    return t1.hour * 60 + t1.minute + d < (t2.hour * 60 + t2.minute) + p + 15


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


def compareMp(key1, el2):
    """
    Comparacion para Map
    """
    key2 = el2['key']
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1
