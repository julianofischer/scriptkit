#!/usr/bin/python
# encoding: utf-8
# Juliano Fischer Naves
# 23 de Outubro de 2013

import os,sys


def procura_no_arquivo(absolute_path):
    f = open(absolute_path,'r')
    lines = f.read().splitlines()
    lines.insert(line,value_to_add)
    
    f = open(absolute_path,'w')
    
    for l in lines:
        f.write(l)
        f.write('\n')
   
    f.flush()
    f.close()


value_to_add = sys.argv[1]
value_to_add = value_to_add + "\n"
line = int (sys.argv[2])

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for file in files:
            f = os.path.abspath(root) + "/" + file
            procura_no_arquivo(os.path.abspath(f))
