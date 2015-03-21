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
       
       if "EpidemicRouter" in line and "Scenario.name" not in line:
           new_line = line.split("EpidemicTTLAttackRouter")[0] #+ "EpidemicBlackHoleRouter\n"
       elif "ProphetRouter" in line and "Scenario.name" not in line:
           new_line = line.split("ProphetTTLAttackRouter")[0] #+ "ProphetBlakcHoleMRouter\n"
       if "SprayAndWaitRouter" in line and "Scenario.name" not in line:
           new_line = line.split("SprayAndWaitTTLAttackRouter")[0] #+ "SprayAndWaitBlackHoleRouter\n"

       if "EpidemicTTLAttackRouter" in line and "Scenario.name" not in line:
           new_line = line.split("EpidemicTTLAttackRouter")[0] + "EpidemicBlackHoleRouter\n"
       elif "ProphetTTLAttackRouter" in line and "Scenario.name" not in line:
           new_line = line.split("ProphetTTLAttackRouter")[0] + "ProphetBlakcHoleMRouter\n"
       if "SprayAndWaitTTLAttackRouter" in line and "Scenario.name" not in line:
           new_line = line.split("SprayAndWaitTTLAttackRouter")[0] + "SprayAndWaitBlackHoleRouter\n"

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
