from model import modelo

# Establecer función objetivo
#with open("resultados.txt", "w", encoding="utf8") as file:
    #file.write("|{0:10}|{1:10}|{2:10}|{3:5}|{4:7}|\n".format("Best Bound", "Valor Obj", "Time", "Sol Count", "Gap"))
print("|{0:10}|{1:10}|{2:5}|{3:5}|".format("Valor Obj", "Time", "Sol Count", "Gap", "BestBound"))
for i in [14]:
    m = modelo(14 - i)
    m.setParam("TimeLimit", 7200)
    m.optimize()
    print("-------------------------------- Partidos a optimizar " + str(i + 1) + "-------------------------------")
    #with open("resultados.txt", "a", encoding="utf8") as file:
        #file.write("|{0:10}|{1:10}|{2:10}|{3:9}|{4:7}|\n".format(m.objBound, m.objVal, round(m.Runtime, 2), m.solCount, round(m.MIPGap, 2)))
    print("----------------------------------------------------------------")
"""
m = modelo(0)
m.optimize()
print("--------------------------------Partidos a optimizar " + str(15) +"-------------------------------")
with open("resultados.txt", "w", encoding="utf8") as file:
    file.write("|{0:10}|{1:10}|{2:9|{3:5}|".format(m.objVal, round(m.Runtime, 2), m.solCount, m.MIPGap))
print("----------------------------------------------------------------")
"""
#m.computeIIS()
#m.write("model.ilp")
# m.printAttr("X")
"""
m.printQuality()
print()
"""
# Imprimir los valores de las variables para la solución óptima
variable_optima = []
for v in m.getVars():
    if "programacion" in v.varName:
        variable_optima.append(v)
utiles = []
for i in variable_optima:
    if i.X == 1:
        utiles.append(i)

variable_optima = []
for v in m.getVars():
    if "Atractivo Ascenso" in v.varName:
        variable_optima.append(v)


for i in variable_optima:
    print(i)

puntos = []
for v in m.getVars():
    if "puntos" in v.varName and v.X == 1:
        puntos.append(v)

for i in puntos:
    print(i)
puntos = []
for v in m.getVars():
    if "nueva" in v.varName and v.X == 1:
        puntos.append(v)

for i in puntos:
    print(i)

