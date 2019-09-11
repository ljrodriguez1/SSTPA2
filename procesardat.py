with open("Resultado1.txt") as result:
    list = []
    for i in result:
        a = i.find("[")
        b = i.find("]")
        list.append([int(x) for x in i[a + 1:b].rstrip("\n").split(",")])

ultima = []
for i in list:
    if i[1] == 30:
        ultima.append(i)
ultima.sort()
for i in ultima:
    print(i)

solo_fecha = [x[1] for x in list]

partidos = [solo_fecha.count(x + 16) for x in range(15)]
print(partidos)