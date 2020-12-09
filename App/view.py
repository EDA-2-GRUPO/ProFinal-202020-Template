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
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as m
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""
# ___________________________________________________
#  printeo funciones
# ___________________________________________________
def printA(lista,cont):
    print(m.size(cont["taxis"]))
    print(cont["companies"])
    print_=-1
    iterador2=it.newIterator(lista)
    while it.hasNext(iterador2):
     next_comp=it.next(iterador2)
     if print_==0:
         print("_____________")
         print("Top taxis")
         print("_____________\n")
         print_+=1
     else:
         print("_________")
         print("Top servicios")
         print("_________\n")
         print_+=1
     iterador=it.newIterator(next_comp)
     while it.hasNext(iterador):
           next=it.next(iterador)
           print(next)
           print(controller.search(cont,next,print_))

# ___________________________________________________
#  Variables
# ___________________________________________________
def printMenu():
    print("hello")

# ___________________________________________________
#  Menu principal
# ___________________________________________________
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if inputs[0] == "q":
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        print(cont.keys())
    elif inputs[0] == "w":
        controller.loadall(cont)
    elif int(inputs[0]) == 1:
         n_top_taxis=input("ingrese el numero de compañias top que desea")
         n_top_services=input("ingrese el numero de compañias top que desea")
         lista_final=controller.A(cont,n_top_taxis,n_top_services)
         printA(lista_final,cont)
    else:
        print("Opcion invalida")
        continue

sys.exit(0)
"""
Menu principal
"""