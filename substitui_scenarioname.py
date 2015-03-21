#!/usr/bin/python
# encoding: utf-8
# Juliano Fischer Naves
# 23 de Outubro de 2013

import os,sys


def procura_no_arquivo(absolute_path):
    list = []
    f = open(absolute_path,'r')
    lines = f.read().splitlines()
    
    has_scenario_name = False

    for line in lines:
       new_line = line
       
       if "Scenario.name" in line:
           new_line = "Scenario.name = %s\n" % nome #recebido por parametro
           has_scenario_name = True

       list.append(new_line)
    
    scenario_name = "Scenario.name %s\n" % nome
    if not has_scenario_name:
        list.insert(0,scenario_name)
        
    f = open(absolute_path,'w')
    
    for l in list:
        f.write(l)
        f.write('\n')
   
    f.flush()
    f.close()


nome = sys.argv[1]
if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for file in files:
            f = os.path.abspath(root) + "/" + file
            procura_no_arquivo(os.path.abspath(f))
