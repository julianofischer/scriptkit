#!/usr/bin/python
# encoding: utf-8
# Juliano Fischer Naves
# 23 de Outubro de 2013

import os,sys


def procura_no_arquivo(absolute_path):
    list = []
    with open(absolute_path,'r') as f:
        uniquelines = set(f.readlines())
    
    with open(absolute_path,'w') as f:
        for l in uniquelines:
            f.write(l)
            #f.write('\n')
            f.flush()   

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for file in files:
            f = os.path.abspath(root) + "/" + file
            procura_no_arquivo(os.path.abspath(f))
