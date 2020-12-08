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
import csv
from DISClib.ADT import map as m
from DISClib.ADT import list as lt


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
def Init():
    return model.newAnalyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def load(analyzer,servicesfile):
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        taxi_id = service["taxi_id"]
        compania= service["company"]
        model.addtaxi(taxi_id, analyzer["taxis"])
        model.addcompania(compania,taxi_id,analyzer)
        model.admpqs(analyzer["compcont"], 
                     analyzer['Maxpq-Afiliados-Compañias-services'],
                     analyzer['Maxpq-Afiliados-Compañias-taxis'])
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def A(analyzer,n_top_taxis,n_top_services):
    lista_final=lt.newList()
    taxis_reportados=m.size(analyzer['taxis'])
    companies_taxi_ins=analyzer["companies"]
    lista_top_taxis_compani=model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-taxis'],
                                            n_top_taxis)
    lista_top_services_compani=model.rank_maxpq(analyzer['Maxpq-Afiliados-Compañias-services'],
                                                n_top_services)
    lt.addLast(lista_final, taxis_reportados)
    lt.addLast(lista_final, companies_taxi_ins)
    lt.addLast(lista_final, lista_top_services_compani)
    lt.addLast(lista_final, lista_top_taxis_compani)
    return lista_final
def search(analyzer, key,pos):
    num=lt.getElement(m.get(analyzer['compcont'],key), pos)
    return num 

    
    

