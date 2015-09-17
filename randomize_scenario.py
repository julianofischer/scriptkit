#!/usr/bin/python    
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# Sep. 17, 2015
# ---------------------

import sys, argparse, random

def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("A negative value was provided as argument")
    return ivalue
'''
def check_lastnode_argument(value):
    check_negative(value)
    ivalue = int(value)
    if ivalue < first_node:
        raise argparse.ArgumentTypeError("Last node should be greater than the first node")
    return ivalue
'''

parser = argparse.ArgumentParser()

'''
parser.add_argument("--first",help="The first node",type=check_negative,default=0)
args = parser.parse_known_args()
first_node = args[0].first'''

#parser.add_argument("--last",help="The last node",type=check_lastnode_argument,required=True)
parser.add_argument("numberOfNodes",help="The total of nodes",type=check_negative)
parser.add_argument("filename",help="The target file")
parser.add_argument("numberOfRuns",help="Number of runs (and outputs)",type=check_negative, default=1)
args = parser.parse_args()

number_of_nodes = args.numberOfNodes
file_name = args.filename
#last_node = args.last
number_of_runs = args.numberOfRuns

def generate(lines,turn):
    #mapping the old id with the new id
    ids = range (0, number_of_nodes)
    random.shuffle(ids)
    
    dic = {}
    aux = 0
    
    for id in ids:
        dic[aux] = str(id)
        aux = aux + 1
    
    new_lines = []
    
    ###TEST CASE###
    #used to test if all ids are appearing in the trace
    ids_assert = []
    for l in lines:
        fromnode = int(l[2])
        tonode = int(l[3])
        
        if ids_assert.count(fromnode) == 0:
            ids_assert.append(fromnode)
            
        if ids_assert.count(tonode) == 0:
            ids_assert.append(tonode)
    
    for x in range (0,number_of_nodes):
        assert ids_assert.count(x) > 0, "The id %d does not appear in the trace" % (x)    
    
    ### end of test case ###
    
    #substituting old ids by new ones
    for l in lines:
        assert len(l) == 5, "The list size should be 5"
        
        fromnode = int(l[2])
        assert fromnode >= 0 and fromnode <= number_of_nodes, "Node out of range"
        
        tonode = int(l[3])
        assert tonode >= 0 and tonode <= number_of_nodes, "Node out of range"
        
        new_line = [l[0],l[1],dic[fromnode],dic[tonode],l[4]]
        new_lines.append(new_line)
        #print "old line: %s" % (','.join(l))
        #print "new line: %s" % (','.join(new_line))
    
    new_filename = file_name + "_" + str(turn)
    
    assert len(lines) == len(new_lines), "New file has different size [ %d != %d ]" % (len(lines),len(new_lines)) 
    
    #write the new file
    with open(new_filename,'w') as f:
        for l in new_lines:
            l = [str(x) for x in l]
            l = " ".join(l)
            f.write(l+"\n")
                
def main():
        
    lines = []
    with open(file_name) as f:
        lines = [x.split() for x in f.readlines()]
    
    for i in range (0,number_of_runs):
        generate(lines,i)

if __name__ == "__main__":
    main()
