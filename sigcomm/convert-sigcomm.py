#!/usr/bin/python3
# coding: utf-8


#pré-processamento
lines = [line.rstrip().split(';')[0:3] for line in open('proximity.csv','r')][1:]

current_list = []
final_list = []
previous = None
current = lines.pop(0)

while len(lines) > 0:
    previous = current
    current = lines.pop(0)
    current_list.append(previous[2])

    if current[0] != previous[0] or current[1] != previous[1]:
        final_list.append([previous[0],previous[1]] + current_list)
        current_list = []

#arquivo acabou mas ainda tem um current para ser processado
current_list.append(current[2])
final_list.append([current[0],current[1]] + current_list)


#with open("final_list",'w') as myfile:
#    for line in final_list:
#        myfile.write(str(line)+"\n")

#for l in final_list:
#    print l

'''
Daqui em diante é o calculo dos contatos.
Funciona da seguinte maneira: se foi visto duas vezes consecutivas, uma conexão foi criada.
'''


#cria um dicionário onde a chave é o id do nó
d = {}
for l in final_list:

    if l[1] not in d:
        d[l[1]] = []

    d[l[1]].append([l[0]] + l[2:])

#conexões são abertas quando aparecem em duas linhas consecutivas
#conexões são fechadas quando estão abertas e não aparecem em uma linha

connections = []

for node in sorted(d.keys(),key=int):
    open_connections = {}
    lista = d[node]

    current = lista.pop(0)
    previous = None
    while len(lista) > 0:
        previous = current
        current = lista.pop(0)

        #a conexão está aberta mas o nó não foi visto
        remove = []
        for anode in open_connections.keys():
            if anode not in current[1:]:
                connections.append( (current[0], "CONN", node, anode, "down") )
                #log for remove
                remove.append(anode)

        for anode in remove:
            #remove de open_connections
            del open_connections[anode]

        #ignora o tempo
        for n in current[1:]:
            if n in previous[1:]:
                if n not in open_connections:
                    open_connections[n] = previous[0]
                    connections.append((previous[0], "CONN", node, n, "up"))

    #fecha as demais conexões
    for anode in open_connections.keys():
        connections.append( (current[0], "CONN", node, anode, "down") )

connections = sorted(connections, key=lambda tup: int(tup[0]))
final_list = [' '.join(coluna) for coluna in connections]

with open("sigcomm_full",'w') as myfile:
    for line in final_list:
        myfile.write(str(line)+"\n")

final_list = [' '.join(coluna) for coluna in connections if int(coluna[2]) < 100 and int(coluna[3]) < 100]

with open("sigcomm_filtered",'w') as myfile:
    for line in final_list:
