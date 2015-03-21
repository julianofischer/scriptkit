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

       #if "ProphetBlakcHoleMRouter" in line and "Scenario.name" not in line:
       #    new_line = line.replace("ProphetBlakcHoleMRouter","ProphetBlackHoleRouter")
       
       if "SprayAndWaitRouter" in line and "Scenario.name" not in line and "Group1.router" in line:
           new_line = new_line.replace("SprayAndWaitRouter","SprayAndWaitBlackHoleCM")

       if "ProphetRouter" in line and "Scenario.name" not in line and "Group1.router" in line:
           new_line = new_line.replace("ProphetRouter","ProphetBlackHoleCM")

       if "EpidemicRouter" in line and "Scenario.name" not in line and "Group1.router" in line:
           new_line = new_line.replace("EpidemicRouter","EpidemicBlackHoleCM")
           
       if "semcontramedida" in line and "Scenario.name" not in line:
           new_line = new_line.replace("semcontramedida","comcontramedida")

       

       #if "Report.reportDir" in line:
       #    line = line.split('cenarioblackhole')
       #    new_line = line[0]+"cenarioblackhole/comcontramedida"+line[1]

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
