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
       
       if "Report.reportDir" in line:
           #splitline = line.split("infocom05/")
           #new_line = splitline[0]+"infocom05/"+"bufferinfinito/"+splitline[1]
           splitline = line.split("rollernet/")
           new_line = splitline[0]+"rollernet/"+"bufferinfinito/"+splitline[1]

       list.append(new_line)
    
    f = open(absolute_path,'w')
    
    for l in list:
        f.write(l)
        f.write('\n')
   
    f.flush()
    f.close()


if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for file in files:
            f = os.path.abspath(root) + "/" + file
            procura_no_arquivo(os.path.abspath(f))
