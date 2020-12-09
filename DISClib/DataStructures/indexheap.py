"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 """

from DISClib.ADT import map as map
from DISClib.DataStructures import liststructure as lt
from DISClib.Utils import error as error

"""
Estructura que contiene la información de una cola de prioridad indexada,
orientada a menor
"""


def newIndexHeap(cmpfunction, gide='Min'):
    """
    Crea un cola de prioridad indexada orientada a menor

    Args:
        cmpfunction:
        gide:
    Returns:
       Una nueva cola de prioridad indexada
    Raises:
        Exception
    """
    try:
        indexheap = {'elements': lt.newList(datastructure='ARRAY_LIST',
                                            cmpfunction=cmpfunction),
                     'qpMap': map.newMap(maptype='PROBING', comparefunction=cmpfunction),
                     'size': 0, 'gide': None}
        gide = smaller if gide == 'Max' else greater
        indexheap['gide'] = gide
        return indexheap
    except Exception as exp:
        error.reraise(exp, 'indexheap:newindexheap')


def insert(iheap, key, index):
    """
    Inserta la llave key con prioridad index

    Args:
        iheap: El heap indexado
    Returns:
       El iheap con la nueva paraja indexada
    Raises:
        Exception
    """
    try:
        if not map.contains(iheap['qpMap'], key):
            iheap['size'] += 1
            lt.insertElement(iheap['elements'], {'key': key, 'index': index},
                             iheap['size'])
            map.put(iheap['qpMap'], key, iheap['size'])
            swim(iheap, iheap['size'])
        return iheap
    except Exception as exp:
        error.reraise(exp, 'indexheap:newindexheap')


def isEmpty(iheap):
    """
    Informa si una cola de prioridad indexada es vacia

    Args:
        iheap: El heap indexado a revisar
    Returns:
       True si esta vacia
    Raises:
        Exception
    """
    try:
        return iheap['size'] == 0
    except Exception as exp:
        error.reraise(exp, 'indexheap:isEmpty')


def size(iheap):
    """
    Retorna el número de elementos en el heap

    Args:
        iheap: El heap a revisar
    Returns:
       El numero de elementos
    Raises:
        Exception
    """
    try:
        return iheap['size']
    except Exception as exp:
        error.reraise(exp, 'indexheap:size')


def contains(iheap, key):
    """
    Indica si la llave key se encuentra en el heap

    Args:
        iheap: El heap a revisar
    Returns:
       El numero de elementos
    Raises:
        Exception
    """
    try:
        return map.contains(iheap['qpMap'], key)
    except Exception as exp:
        error.reraise(exp, 'indexheap:contains')


def first(iheap):
    """
    Retorna el primer elemento del heap, es decir el menor elemento

    Args:
        iheap: El heap a revisar
    Returns:
       El numero de elementos
    Raises:
        Exception
    """
    try:
        if (iheap['size'] > 0):
            firstIdx = lt.getElement(iheap['elements'], 1)
            return firstIdx['key']
        return None
    except Exception as exp:
        error.reraise(exp, 'indexheap:first')


def delFirst(iheap):
    """
    Retorna el menor elemento del heap y lo elimina.
    Se reemplaza con el último elemento y se hace sink.

    Args:
        iheap: El heap a revisar
    Returns:
       La llave asociada al mayor indice
    Raises:
        Exception
    """
    try:
        if (iheap['size'] > 0):
            firstIdx = lt.getElement(iheap['elements'], 1)
            exchange(iheap, 1, iheap['size'])
            iheap['size'] -= 1
            sink(iheap, 1)
            map.remove(iheap['qpMap'], firstIdx['key'])
            return firstIdx['key']
        return None
    except Exception as exp:
        error.reraise(exp, 'indexheap:delFirst')


def decreaseKey(iheap, key, newindex):
    """
    Decrementa el indice de un llave

    Args:
        iheap: El heap a revisar
        key: la llave a decrementar
        newindex: El nuevo indice de la llave
    Returns:
       El numero de elementos
    Raises:
        Exception
    """
    try:
        val = map.get(iheap['qpMap'], key)
        elem = lt.getElement(iheap['elements'], val['value'])
        elem['index'] = newindex
        lt.changeInfo(iheap['elements'], val['value'], elem)
        swim(iheap, val['value'])
        return iheap
    except Exception as exp:
        error.reraise(exp, 'indexheap:decreaseKey')


def increaseKey(iheap, key, newindex):
    """
    Incrementa el indice de un llave

    Args:
        iheap: El heap a revisar
        key: la llave a incrementar
        newindex: El nuevo indice de la llave
    Returns:
       El numero de elementos
    Raises:
        Exception
    """
    try:
        val = map.get(iheap['qpMap'], key)
        elem = lt.getElement(iheap['elements'], val['value'])
        elem['index'] = newindex
        lt.changeInfo(iheap['elements'], val['value'], elem)
        sink(iheap, val['value'])
        return iheap
    except Exception as exp:
        error.reraise(exp, 'indexheap:increaseKey')


#  ---------------------------------------------------------
#   Funciones Helper
#  ---------------------------------------------------------


def exchange(iheap, i, j):
    """
    Intercambia los elementos en las posiciones i y j del heap
    """
    try:
        element_i = lt.getElement(iheap['elements'], i)
        element_j = lt.getElement(iheap['elements'], j)
        lt.changeInfo(iheap['elements'], i, element_j)
        map.put(iheap['qpMap'], element_i['key'], j)
        lt.changeInfo(iheap['elements'], j, element_i)
        map.put(iheap['qpMap'], element_j['key'], i)
    except Exception as exp:
        error.reraise(exp, 'indexheap:exchange')


def greater(parent, element):
    """
    Indica si el index de parent es mayor
    que index de element
    """
    try:
        return parent['index'] > element['index']
    except Exception as exp:
        error.reraise(exp, 'indexheap:greater')


def smaller(parent, element):
    """
       Indica si el index de parent es mayor
       que index de element
       """
    try:
        return parent['index'] < element['index']
    except Exception as exp:
        error.reraise(exp, 'indexheap:greater')


def swim(iheap, pos):
    """
    Deja en el lugar indicado un elemento adicionado
    en la última posición

    Args:
        heap: El arreglo con la informacion
        pos: posicion en el arreglo a revisar

    Returns:
        El arreglo en forma de heap
    Raises:
        Exception
    """
    try:
        gide = iheap['gide']
        while pos > 1:
            posparent = int((pos / 2))
            poselement = int(pos)
            parent = lt.getElement(iheap['elements'], posparent)
            element = lt.getElement(iheap['elements'], poselement)
            if gide(iheap, parent, element):
                exchange(iheap, posparent, poselement)
            pos = (pos // 2)
    except Exception as exp:
        error.reraise(exp, 'indexheap:swim')


def sink(iheap, pos):
    """
    Deja en la posición correcta un elemento ubicado en la raíz del heap

    Args:
        heap: El arreglo con la informacion
        pos: posicion en el arreglo a revisar

    Returns:
        El arreglo en forma de heap
    Raises:
        Exception
    """
    try:
        size = iheap['size']
        gide = iheap['gide']
        while ((2 * pos <= size)):
            j = 2 * pos
            if (j < size):
                if gide(iheap, lt.getElement(iheap['elements'], j),
                        lt.getElement(iheap['elements'], (j + 1))):
                    j += 1
            if (not gide(iheap, lt.getElement(iheap['elements'], pos),
                         lt.getElement(iheap['elements'], j))):
                break
            exchange(iheap, pos, j)
            pos = j
    except Exception as exp:
        error.reraise(exp, 'indexheap:sink')
