#coding: utf-8

#as conexões são abertas quando o primeiro vê e fechadas quando o primeiro deixa de ver

open_connections = []

def is_open(tu):
    for t in open_connections:
        equality_1 = t[0] == tu[0] and tu[1] == t[1]
        equality_2 = t[0] == tu[1] and tu[0] == t[1]
        if equality_1 or equality_2:
            return True
    return False

#no ONE começa em 0 os ids, como no datast começa em 1, temos que decrementar todos os ids.
def decrement(item):
    from_node = str(int(item[2]) - 1)
    to_node = str(int(item[3]) - 1)
    return (item[0],item[1],from_node,to_node,item[4])


def close_connection(tu):

    tuple_to_remove = None

    for t in open_connections:
        equality_1 = t[0] == tu[0] and tu[1] == t[1]
        equality_2 = t[0] == tu[1] and tu[0] == t[1]
        if equality_1 or equality_2:
            tuple_to_remove = t
            break

    if tuple_to_remove:
        open_connections.remove(tuple_to_remove)
    else:
        raise Exception("Solicitando fechamento de conexão que não está aberta...")


'''
   (from,to)
'''

lines_to_save = []

lines = [line.split() for line in open('sigcomm_filtered','r')]
lines = list(map(decrement, lines))

for line in lines:

    if 'up' in line:
        tu = (line[2],line[3])

        if not is_open(tu):
            open_connections.append(tu)
            lines_to_save.append(line)
        else:
            #ignora a linha pois a conexão já está aberta
            print ("ignoring %s" % str(line))
            pass

    elif 'down' in line:
        if is_open(tu):
            close_connection(tu)
            lines_to_save.append(line)
        else:
            #ignora a linha pois a conexão já está fechada
            print ("ignoring %s" % str(line))

    else:
        raise Exception('linha não tem down nem up')

with open("sigcomm_refiltered",'w') as f:
    for line in lines_to_save:
        f.write(" ".join(line)+"\n")