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
from DISClib.ADT import map as m
from DISClib.ADT import indexminpq as minq
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import minpq as pq
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
        citibike = {'taxis': m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds),
                    "companies":0,
                    'compcont': m.newMap(numelements=14000,
                                      maptype='PROBING',
                                      comparefunction=compareStopIds), 
                    'Maxpq-Afiliados-Compañias-services': pq.newMinPQ(compareStopIds),
                    'Maxpq-Afiliados-Compañias-taxis': pq.newMinPQ(compareStopIds)}
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
# Funciones para agregar informacion al grafo
def addtaxi(taxi_id, analizer):
    if not m.contains(analizer, taxi_id):
        m.put(analizer, taxi_id,0)
def addcompania(compania, taxi_id, analyzer):
    map_compania=analyzer[analyzer["compcont"]]
    if m.contains(map_compania, compania):
        compania_info=m.get[map_compania, str(compania)]
        n_servicios=lt.getElement(compania_info,0)
        n_servicios+=1
        map_taxis=lt.getElement(compania_info,1)
        if not m.contains(map_taxis,taxi_id):
            m.put(map_taxis,taxi_id,0)
    else:
        analyzer["companies"]+=1
        lista_compañia=lt.newList()
        mapa_taxis= m.newMap(numelements=14000,
                             maptype='PROBING',
                             comparefunction=compareStopIds)
        addtaxi(mapa_taxis, taxi_id)
        #añade todo a compcont
        lt.addLast(lista_compañia, 1)
        lt.addLast(lista_compañia, mapa_taxis)
        m.put(map_compania,compania,lista_compañia)
def admpqs(map_companies,maxpq_ntaxis,maxpq_nservices):
    lista_companias=m.keySet(map_companies)
    iterador= it.newIterator(lista_companias)
    while it.hasNext(map_companies)
       next_compani=it.next(iterador)
       compani_info=m.get(map_companies,next_compani)
       map_taxis=lt.getElement(compani_info, 1)
       numero_servicios_compani=lt.getElement(compani_info, 0)
       numero_taxis_compani=m.size(map_taxis)
       #add_to_maxpqs
       minq.insert(maxpq_ntaxis, next_compani,numero_taxis_compani)
       minq.insert(maxpq_nserives, next_compani, numero_servicios_compani)
def rank_maxpq(maxpq, numero):
    lista_companies= lt.newList()
    for a in rank(0,numero):
       llave=minq.min(maxpq)
       minq.delMin(maxpq)
       lt.addLast(lista_companies, llave)
    return lista_companies
def rehacer(lista, mapa_companies,pq,pos):
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        nextc=it.next()
        if pos == 0:
           numero=lt.get(m.get(mapa_companies,nextc),pos)
        else:
           mapa=lt.get(m.get(mapa_companies,nextc),pos)
           numero=m.size(mapa) 
        minq.insert(pq,nextc,numero)

    





    



# ==============================
# Funciones de consulta
# ==============================

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================