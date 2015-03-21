#!/usr/bin/python
# encoding: utf-8
# Juliano Fischer Naves
# 23 de Outubro de 2013

import os,sys


def procura_no_arquivo(absolute_path):
    list = []
    f = open(absolute_path,'r')
    lines = f.read().splitlines()

    for line in lines:
       new_line = line
       
       if "TTLAttack.factor" in line and "Scenario.name" not in line:
           new_line = "TTLAttack.factor = %s\n" % nome #recebido por parametro
       if "Report.reportDir" in line:
           line = line.split('/')
           line[4] = "fator_%s" % nome
           new_line = '/'.join(line)

       list.append(new_line)
    
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
