from gurobipy import *
from Database import equipos, Wis, Rina, Bift, Eit, Vf, ELin, EVin, Lsf, puntosvalidos, Nijn, Aif, Dif, puntos as puntos1
from constant import fechaini, fechafin


# Modelo
def modelo(partidosPre):
    m = Model("")
    # m.setParam("threads", 8)
    partidos = [x for x in range(120)]
    fechas = [x + fechaini for x in range(15)]
    patrones = [x + 1 for x in range(1440)]
    puntos = [x + 9 for x in range(61)]
    A = [0, 1, 3]
    # numero de fechas (por definir)
    # Variables
    # print(equipos)
    x_nf = m.addVars(partidos, fechas, vtype=GRB.BINARY, name="programacion")
    y_is = m.addVars(equipos, patrones, vtype=GRB.BINARY, name="patron")
    p_itf = m.addVars(puntosvalidos, vtype=GRB.BINARY, name="puntos")
    a_if = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="Atractivo Ascenso")
    d_if = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="Atractivo Descenso")
    s_ft = m.addVars(fechas, puntos, vtype=GRB.BINARY, name="Maximo Puntaje")
    z_ft = m.addVars(fechas, puntos, vtype=GRB.BINARY, name="Puntaje Atractivo")
    b_nf = m.addVars(partidos, fechas, vtype=GRB.BINARY, name="Atractivo Partido Ascenso")
    l_ft = m.addVars(fechas, puntos, vtype=GRB.BINARY, name="Minimo Puntaje")
    f_ft = m.addVars(fechas, puntos, vtype=GRB.BINARY, name="Atractivo Partido Descenso")
    u_isf = m.addVars(equipos, patrones, fechas, vtype=GRB.BINARY, name="Ultimo Atractivo")



    ##m.addConstrs((p_itf[equipo, punto, fecha] == 0 for equipo in equipos for fecha in fechas for punto in puntos if punto
      ##            not in puntos1[equipo][fecha]))


    m.addConstrs((a_if[equipo, fecha] == 1 for equipo in equipos for fecha in fechas if Aif[equipo][fecha]), name="r342")

    m.addConstrs((d_if[equipo, fecha] == 1 for equipo in equipos for fecha in fechas if Dif[equipo][fecha]), name="r342")

    # cantidad de partidos preprogramados
    m.addConstrs((x_nf[(partido) + 8 * (fecha), fecha + 16] == 1 for partido in range(8) for fecha in range(partidosPre)), name="test")

    # R2
    m.addConstrs((quicksum(x_nf[partido, fecha] for fecha in fechas) == 1 for partido in partidos), name="R2")

    # R3
    m.addConstrs((quicksum(x_nf[partido, fecha] for partido in partidos if (ELin[equipo][partido] + EVin[equipo][partido])
                           == 1) == 1 for equipo in equipos for fecha in fechas), name="R3")

    # R4
    m.addConstrs((quicksum(y_is[equipo, patron] for patron in patrones if Wis[equipo][patron]) == 1 for equipo in equipos),
                 name="R4")

    # R5
    m.addConstrs((y_is[equipo, patron] == 0 for equipo in equipos for patron in patrones if Wis[equipo][patron] == 0),
                 name="R5")

    # R6
    m.addConstrs((quicksum(x_nf[partido, fecha] for partido in partidos if ELin[equipo][partido] == 1) ==
                  quicksum(y_is[equipo, patron] for patron in patrones if Lsf[patron][fecha] == 1)
                  for equipo in equipos for fecha in fechas), name="R6")
    # R7
    m.addConstrs((quicksum(x_nf[partido, fecha] for partido in partidos if EVin[equipo][partido] == 1) ==
                  quicksum(y_is[equipo, patron] for patron in patrones if Lsf[patron][fecha] == 0)
                  for equipo in equipos for fecha in fechas), name="R7")
    # R8

    m.addConstrs((quicksum(p_itf[equipo, punto, fecha] for punto in puntos1[equipo][fecha]) == 1 for equipo in equipos for fecha in fechas),
                 name="R8")

    # R9
    m.addConstrs((p_itf[equipo, punto, fecha - 1] <= quicksum(Rina[equipo][partido][a] * p_itf[equipo, punto + a, fecha] +
                  (1 - x_nf[partido, fecha]) for a in A if punto + a in puntos1[equipo][fecha]) for equipo in equipos for partido in partidos for fecha in fechas[1:]
                  for punto in puntos1[equipo][fecha - 1]
                  if Bift[equipo][fecha][punto] == 1 and partido in Rina[equipo].keys()), name="R9")

    # R10
    m.addConstrs((Eit[equipo][punto] <= quicksum(Rina[equipo][partido][a] * p_itf[equipo, punto + a, fecha] +
                                                              (1 - x_nf[partido, fecha]) for a in A if punto + a in puntos1[equipo][fecha]) for equipo in equipos
                  for partido in partidos for punto in puntos for fecha in fechas if (fecha == 16 and
                                                            Bift[equipo][fecha][punto] == 1 and partido in Rina[equipo].keys())), name="R10")

    # R11
    m.addConstrs((p_itf[equipo, punto, fecha] == 0 for equipo in equipos for fecha in fechas for punto in puntos1[equipo][fecha] if Bift[equipo][fecha][punto] == 0), name="R11")

    """
    Restricciones para definir alfa, con nombre s en programa
    """

    m.addConstrs((quicksum(s_ft[fecha, punto] for punto in puntos) == 1 for fecha in fechas), name="R133")

    m.addConstrs((s_ft[fecha, punto] <= 1 - p_itf[equipo, punto2, fecha] for punto in puntos
                  for equipo in equipos for fecha in fechas for punto2 in puntos1[equipo][fecha] if punto < punto2), name="R134")

    m.addConstrs((s_ft[fecha, punto] <= quicksum(p_itf[equipo, punto, fecha] for equipo in equipos if punto in puntos1[equipo][fecha])
                  for punto in puntos for fecha in fechas), name="R134")


    m.addConstrs((quicksum(s_ft[fecha, punto2]
                           for punto2 in puntos if punto2 <= punto1 + 3 * (fechafin - fecha + 1)) == z_ft[fecha, punto1]
                  for punto1 in puntos for fecha in fechas if fecha >= 17))

    """
    # R12 Sin nueva variable s_tf
    m.addConstrs((a_if[equipo1, fecha] <= (1 - p_itf[equipo1, punto1, fecha - 1]) + quicksum(s_tf[fecha - 1, punto2]
                  for punto2 in puntos if punto2 <= punto1 + 3 * (fechafin - fecha + 1))
                  for equipo1 in equipos for punto1 in puntos
                  for fecha in fechas if (fecha >= 17)), name="R12")
    """
    # R12 Con nueva variable
    m.addConstrs((a_if[equipo, fecha] <= (1 - p_itf[equipo, punto, fecha - 1]) + z_ft[fecha, punto]
                  for equipo in equipos for fecha in fechas[1:] for punto in puntos1[equipo][fecha - 1]), name="R12")

    """
    # R12 Con nueva variable
    m.addConstrs((a_if[equipo1, fecha] == z_ft[fecha - 1, punto1]
                  for equipo1 in equipos for punto1 in puntos
                  for fecha in fechas if (fecha >= 17 and p_itf[equipo1, punto1, fecha - 1])), name="R12")
    """
    # R13
    m.addConstrs((a_if[equipo1, fecha] <= (1 - Eit[equipo1][punto1]) + quicksum(Eit[equipo2][punto2] for punto2 in puntos if punto2 <= punto1 + 3 * (fechafin - fecha + 1))
                  for equipo1 in equipos for equipo2 in equipos for punto1 in puntos for fecha in fechas
                  if (fecha == 16 and equipo1 != equipo2)),
                 name="R13")

    # R14
    # m.addConstrs((a_if[equipo, fecha] <= 1 for equipo in equipos for fecha in fechas), name="R14")


    # R15
    m.addConstrs((a_if[equipo, fecha] <= a_if[equipo, fecha - 1] for equipo in equipos for fecha in fechas if fecha >= 17), name="R15")


    #Restricciones para definir cuando  un partido es interesante Si se quieren usar estar restricciones ocupár funcion
    #objetivo llamada obj2

    m.addConstrs((b_nf[partido, fecha] <= (a_if[equipo1, fecha] + a_if[equipo2, fecha])/2 for equipo1 in equipos for equipo2 in equipos
                  for fecha in fechas for partido in partidos if equipo1 != equipo2 and Nijn[equipo1][equipo2][partido]), name="test1")
    m.addConstrs((b_nf[partido, fecha] <= x_nf[partido, fecha] for fecha in fechas for partido in partidos), name="test2")


    #Definiendo Peor Puntaje l
    m.addConstrs((quicksum(l_ft[fecha, punto] for punto in puntos) == 1 for fecha in fechas), name="R133")

    m.addConstrs((l_ft[fecha, punto] <= 1 - p_itf[equipo, punto2, fecha] for punto in puntos
                  for equipo in equipos for fecha in fechas for punto2 in puntos1[equipo][fecha] if punto2 < punto), name="R134")

    m.addConstrs((l_ft[fecha, punto] <= quicksum(p_itf[equipo, punto, fecha] for equipo in equipos if punto in puntos1[equipo][fecha])
                  for punto in puntos for fecha in fechas), name="R134")


    m.addConstrs((quicksum(l_ft[fecha, punto2]
                           for punto2 in puntos if punto2 >= punto1 - 3 * (fechafin - fecha + 1)) == f_ft[fecha, punto1]
                  for punto1 in puntos for fecha in fechas if fecha >= 17))

    # R 16.2

    m.addConstrs((d_if[equipo, fecha] <= (1 - p_itf[equipo, punto, fecha - 1]) + f_ft[fecha, punto]
                  for equipo in equipos for fecha in fechas[1:] for punto in puntos1[equipo][fecha - 1]
                  if (fecha >= 17)), name="R12")
    """
    # R16
    # Funciones Para definir el d_if comentadas para testear modelo mas sencillo
    
    m.addConstrs((d_if[equipo1, fecha] <= (1 - p_itf[equipo1, punto1, fecha - 1]) + quicksum(p_itf[equipo2, punto2, fecha-1]
                  for punto2 in puntos if punto2 >= punto1 - 3 * (fechafin - fecha + 1))
                  for equipo1 in equipos for equipo2 in equipos for punto1 in puntos
                  for fecha in fechas if (fecha >= 17 and equipo1 != equipo2)), name="R16")
    # R17
    """
    m.addConstrs((d_if[equipo1, fecha] <= (1 - Eit[equipo1][punto1]) + quicksum(Eit[equipo2][punto2] for punto2 in puntos if punto2 >= punto1 - 3 * (fechafin - fecha + 1))
                  for equipo1 in equipos for equipo2 in equipos for punto1 in puntos for fecha in fechas
                  if (fecha == 16 and equipo1 != equipo2)),
                 name="R17")

    # R18
    # m.addConstrs((d_if[equipo, fecha] <= 1 for equipo in equipos for fecha in fechas), name="R18")

    # R19
    m.addConstrs((d_if[equipo, fecha] <= d_if[equipo, fecha - 1] for equipo in equipos for fecha in fechas if fecha >= 17), name="R19")

    # R20 Restriccion agregada al modelo para decir que solo se pueden jugar 8 partidos por fecha

    m.addConstrs((quicksum(x_nf[partido, fecha] for partido in partidos) == 8 for fecha in fechas), name="R20")
    """
    m.addConstrs((y_is[equipo, patron] == quicksum(u_isf[equipo, patron, fecha] for fecha in fechas) for equipo in equipos for patron in patrones), name="R50")
    
    m.addConstrs((a_if[equipo, fecha + 1] == a_if[equipo, fecha] - quicksum(u_isf[equipo, patron, fecha] for patron in patrones)
                  for equipo in equipos for fecha in fechas if fecha != 30))
    """

    obj = quicksum(Vf[fecha] * (a_if[equipo, fecha] + d_if[equipo, fecha]) for fecha in fechas for equipo in equipos)
    obj1 = quicksum(Vf[fecha] * (a_if[equipo, fecha]) for fecha in fechas for equipo in equipos)
    obj2 = quicksum(
        Vf[fecha] * (b_nf[partido, fecha] + a_if[equipo, fecha]) for fecha in fechas for partido in partidos for equipo
        in equipos)
    obj3 = quicksum(Vf[fecha] * (b_nf[partido, fecha]) for fecha in fechas for partido in partidos)

    m.setObjective(obj3, GRB.MAXIMIZE)
    return m
