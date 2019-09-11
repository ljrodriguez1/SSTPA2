import pandas as pd


def open_excel(name, page):
    """
    :param name: nombre del archivo a abrir
    :param page: nombre de la pagina de interes
    :return: lista por filas de pagina de excel
    """
    file = pd.ExcelFile(name)
    file = file.parse(page)
    column = []
    for key in file.keys():
        lista = []
        for i in range(len(file[key])):
            lista.append(str(file[key][i]).rstrip().replace("\xa0", " "))
        column.append(lista)
    lista = list(zip(*column))
    return lista


equiposDB = open_excel("datos/Datos.xlsx", 0)
partidosDB = open_excel("datos/Datos.xlsx", 1)

"""Creando diccionario Partidos para facilidad de manejo"""
pos = 0
listPos = []
for i in partidosDB:
    if i[0] != "nan":
        listPos.append(pos)
    pos += 1
dif = []
partidosJ = {partidosDB[i][0]: partidosDB[i + 1: i + 9] for i in listPos}
indice = 0
newDict = {}
superList = []
for key in partidosJ.keys():
    newList = []
    for fecha in partidosJ[key]:
        resultado = fecha[4].split(" : ")
        if int(resultado[0]) < int(resultado[1]):
            puntos = [0, 3]
        elif int(resultado[0]) > int(resultado[1]):
            puntos = [3, 0]
        else:
            puntos = [1, 1]
        newList.extend([[119 - indice, fecha[2], "Local", puntos[0], key, fecha[3]],
                        [119 - indice, fecha[3], "Visita", puntos[1], key, fecha[2]]])
        indice += 1
    superList.extend(newList)
    newDict[key] = newList
equipos = [x[2] for x in equiposDB]

"""
Definiendo variable Eit, toma 1 si equipo "i" tiene "t" puntos.
 para esto tMax es maximo puntaje
"""
tMax = max([int(x[3]) for x in equiposDB])
# for x in equiposDB:
#    print(x)
Eit = {x[2]: {i: 1 if i == int(x[3]) else 0 for i in range(83 + 1)} for x in equiposDB}
"""
variable Rina 1 si cantida de puntos que gana equipo "i" 
jugando partido "n" es igual a "a"
"""
Rina = {}
for i in equipos:
    Rina[i] = {}

for x in superList:
    #print(x) #[numero partido, equipo, local, puntos, fecha, equipo]
    Rina[x[1]].update({x[0]: {}})

for x in superList:
    for puntos in [0, 1, 3]:
        Rina[x[1]][x[0]].update({puntos: 1 if x[3] == puntos else 0})

"Ñ 1 si equipo i juega contra equipo j partido n"
Nijn = {x: {} for x in equipos}
for equipo in equipos:
    Nijn[equipo] = {x: {i: 0 for i in range(120)} for x in equipos if x != equipo}

contador = 0
for data in superList:
    Nijn[data[1]][data[5]][data[0]] = 1
    if contador == 239:
        break
    contador += 1

"""
ELin EVin 1 su equipo i es "L" o "V" en partido n
"""
ELin = {x: {} for x in equipos}
EVin = {x: {} for x in equipos}
for i in equipos:
    for z in range(120):
        EVin[i].update({z: 0})
        ELin[i].update({z: 0})

contador = 0
for i in superList:
    # print(i)
    ELin[i[1]].update({i[0]: 1 if i[2] == "Local" else 0})
    EVin[i[1]].update({i[0]: 1 if i[2] == "Visita" else 0})
    if contador == 239:
        break
    contador += 1

"""
Wis
"""
data = open_excel("datos/Generador de Patrones.xlsm", "W")
Wis = {x: {} for x in equipos}
for i in data:
    Wis[i[1]].update({int(i[3]): int(i[5])})

"Vf funcion de valor por fecha"
Vf = {x + 1: x * 2 for x in range(30)}

"""
Lfs Toma 1 si patron s indica que partido esde local en fecha s
"""
data = open_excel("datos/Generador de Patrones.xlsm", "Patrones")
Lsf = {x + 1: {} for x in range(1440)}
for i in range(1440):
    Lsf[i + 1].update({x + 16: int(data[i][x]) for x in range(15)})

"""
Bift
"""
data = open_excel("datos/Datos.xlsx", "Equipos")
Bift = {x: {} for x in equipos}
for x in equipos:
    for i in range(15):
        Bift[x].update({i + 16: {}})
for x in data:
    for fecha in range(15):
        for puntos in range(84):
            Bift[x[2]][fecha + 16].update({puntos: 1 if int(x[3]) + (fecha + 1) * 3 >= puntos else 0})


puntosInicio = {x[2]: int(x[3]) for x in data}
puntosMax = {}
puntosMin = {}
resultadoPartidos = {}
for equipo in equipos:
    ucwin = 0
    ucdraw = 0
    for partidos in list(Rina[equipo].keys())[0:15]:
        if Rina[equipo][partidos][3] == 1:
            ucwin += 1
        elif Rina[equipo][partidos][1] == 1:
            ucdraw += 1
    uclost = 15 - ucwin - ucdraw
    uct = {(x + 16): puntosInicio[equipo] + ((x + 1) * 3) if x < ucwin else puntosInicio[equipo] + (ucwin * 3) + (
            x + 1 - ucwin) if x < ucwin + ucdraw else puntosInicio[equipo] + ucwin * 3 + ucdraw for x in range(15)}
    ucl = {(x + 16): puntosInicio[equipo] if x < uclost else puntosInicio[equipo] + + (
            x + 1 - uclost) if x < uclost + ucdraw else puntosInicio[equipo] + (x + 1 - uclost - ucdraw) * 3 + ucdraw
           for x in range(15)}
    puntosMax[equipo] = uct
    puntosMin[equipo] = ucl
    resultados = {"win": ucwin, "draw": ucdraw, "loss": uclost}
    resultadoPartidos.update({equipo: resultados})

puntos = {equipo: {fecha + 16: [x for x in range(puntosMin[equipo][fecha + 16], puntosMax[equipo][fecha + 16] + 1)] for fecha in range(15)} for equipo in equipos}
# Rina = {line[0]: {puntos: 1 if puntos == puntos else 0} for puntos in [0, 1, 3] for line in equiposDB}

puntosvalidos = []
for i in equipos:
    for j in range(15):
        j = j + 16
        for k in range(90):
            if k in puntos[i][j]:
                puntosvalidos.append((i, k, j))



Aif = {x: {i + 16: 1 if puntosInicio[x] + 3 * (15 - i) > 34 + (i * 3) else 0 for i in range(15)} for x in equipos}


Dif = {x: {i + 16: 1 if puntosInicio[x] + (3 * i) < 9 + (15 - i) * 3 else 0 for i in range(15)} for x in equipos}
