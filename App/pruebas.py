import config as cf
from DISClib.ADT import indexminpq as pq

def greater(key1, key2):
    key2=key2["key"]
    if key1 == key2:
        return 0
    elif key1 > key2:
        return -1
    else:
        return 1
minpq = pq.newIndexMinPQ(greater)

pq.insert(minpq, "5",5)
pq.insert(minpq, "23",23)
pq.insert(minpq, "31",31)
pq.insert(minpq, "15",15)

print(pq.delMin(minpq))
print(pq.delMin(minpq))
print(pq.delMin(minpq))