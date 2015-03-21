#! /usr/bin/python
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# julianofischer at gmail dot com
# 2014, Oct. 1

import sys

file_name = sys.argv[1]
#node_number = int(sys.argv[2])

my_file = open(file_name,"r")
lines = my_file.readlines()

connections = {}
con_dist = {}

for line in lines:
    splitted = line.split(" ")
    #print splitted
    now = int(splitted[0])
    from_node = int(splitted[2])
    to_node = int(splitted[3])
    #print splitted
    isUp = splitted[4].find('up') != -1
    
    if isUp:
        #to_node
        if to_node not in connections:
            connections[to_node] = 1
        else:
            connections[to_node] = connections[to_node] + 1
        
        if to_node not in con_dist:
            con_dist[to_node] = []
            
        if from_node not in con_dist[to_node]:
            con_dist[to_node].append(from_node)
        
        #from_node
        if from_node not in connections:
            connections[from_node] = 1
        else:
            connections[from_node] = connections[from_node] + 1
        
        if from_node not in con_dist:
            con_dist[from_node] = []
            
        if to_node not in con_dist[from_node]:
            con_dist[from_node].append(to_node)




connections_sum = 0
distinct_sum = 0

for key, value in connections.iteritems():
    distinct = -1
    for other_key, other_value in con_dist.iteritems():
        if other_key == key:
            distinct = len(other_value)
            distinct_sum = distinct_sum + distinct
            #print other_value
            break
            
    print "Node %s had %d connections with %d distinct other nodes" % (key,value,distinct)
    connections_sum = connections_sum + int(value)
    

#for key, value in con_dist.iteritems():
#    print "Node %s had connected with %d distinct other nodes" % (key,len(value))
    #print value


print "Average number of connections: %d" % (connections_sum/len(connections.keys()))
print "Average number of distinct %d" % (distinct_sum/len(con_dist.keys()))
print "Number of nodes: %d ad %d" % (len(connections.keys()),len(con_dist.keys()))
