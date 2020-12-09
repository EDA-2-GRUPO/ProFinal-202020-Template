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

import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.DataStructures import listiterator as it
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""


# ___________________________________________________
#  Variables
# ___________________________________________________

def printB(lista):
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        next=it.next(iterador)
        print(next)
def printC(lista):
    print("hora: ",lista["hour"])
    iterador=it.newIterator(lista["path"])
    while it.hasNext(iterador):
       next=it.next(iterador)
       print("VertexA: ",next["vertexA"][0]+" "+str(next["vertexA"][1]),"VertexB: ",next["vertexB"][0]+" "+str(next["vertexB"][1]))
    print("time: ", lista["time"])
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("q- Inicializar Analizador")
    print("w- Cargar información")
    print("1- Parte A")
    print("2- Parte B")
    print("5- Parte c")


"""
Menu principal
"""
dict_files = {'1': 'taxi-trips-wrvz-psew-subset-small.csv', '2': 'taxi-trips-wrvz-psew-subset-medium.csv',
              '3': "taxi-trips-wrvz-psew-subset-large.csv"}


def inicializar():
    print("\nInicializando....")
    return controller.incializar()


def cargar(cont):
    print('cargando')
    print('seleccion el volumen de datos')
    c = input('1: small, 2: medium, 3: large')
    controller.loadServices(cont, dict_files[c])
    print('se han cargado los datos')
    return cont


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "w":
        cont = inicializar()

    elif inputs[0] == "q":
        cargar(cont)

    elif int(inputs[0]) == 1:
        pass


    elif int(inputs[0]) == 2:
        inputs = input('1: en una fecha, 2: en un rango de fechas\n>')
        if inputs[0] == '1':
            d = input('ingrese date')
            n = input('ingrese n')
            lista_final=controller.partB_1(cont, d, n)
            printB(lista_final)
        else:
            d1 = input('ingrese date1')
            d2 = input('ingrese date2')
            n = input('ingrese n')
            lista_final=controller.partB_2(cont, d1, d2, n)
            printB(lista_final)
    elif int(inputs[0]) == 3:
        h1 = input('hora1')
        h2 = input('hora2')
        o = input('pick')
        d = input('drofft')
        lista_final=controller.partC(cont, o, d, h1, h2)
        printC(lista_final)
    else:
        break
