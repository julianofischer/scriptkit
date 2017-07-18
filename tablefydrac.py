#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# ---------------------
'''
  Transforma os resultados em linhas de uma tabela Latex
  Input: diretório com os resultados no formato utilizado (epidemicbrg, epidemicdrac, epidemicdracstop...)
'''
import sys

TABLEHEADER = '''\\begin{table}[]
\centering
\caption{My caption}
\label{my-label}
\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|l|l|}
\hline
                                                                                & \multicolumn{6}{l|}{\\textbf{Diferença Absoluta (\%)}}                   & \multicolumn{6}{l|}{\\textbf{Diferença Relativa (\%)}}                   \\\\ \hline
\\textbf{\\begin{tabular}[c]{@{}l@{}}Protocolo/\\\\ Nº Nós Maliciosos\end{tabular}} & \\textbf{0} & \\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} & \\textbf{5} & \\textbf{0} & \\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} & \\textbf{5} \\\\ \hline'''

TABLEFOOTER = '''\end{tabular}
\end{table}'''

TABLELINE_STR = "\\textbf{%s}                                                                       &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     &     %d     \\\\ \hline"

dictionary = {"epidemic" : "Epidêmico", "life" : "Life", "maxprop" : "MaxProp", "prophet":"Prophet","prophetv2":"ProphetV2","snw":"SnW","wave":"Wave"}
DRACSTOP_SUFFIX = "dracstop"
BRG_SUFFIX = "brg"
positive_counter = 0;
total_counter = 0;

def main():
    directory = sys.argv[1]

    print(TABLEHEADER)
    for key in sorted(dictionary.keys()):
        dracstopfile = directory + key + DRACSTOP_SUFFIX
        brgfile = directory + key + BRG_SUFFIX
        tablefy(dracstopfile, brgfile, key)
    print(TABLEFOOTER)

    print("Total: %d, Positive: %d, Percent %f" % (total_counter, positive_counter, (positive_counter*100.0)/total_counter))

def tablefy(filea, fileb, key):
    global positive_counter, total_counter;
    #print("Opening: %s, %s, %s" % (filea,fileb,key))
    t = (dictionary[key],)
    absolute_values = []
    relative_values = []

    with open(filea) as dracstopfile, open(fileb) as brgfile:
        for i in range(0,6):
            line_dracstop = dracstopfile.readline().split()
            line_brg = brgfile.readline().split()
            dracstop_value = float(line_dracstop[1])
            brg_value = float(line_brg[1])
    
            absolute_value = round((dracstop_value-brg_value) * 100.0)
            absolute_values.append(absolute_value)

            total_counter = total_counter + 1
            if absolute_value > 0:
                positive_counter = positive_counter + 1

            relative_value = round(((dracstop_value * 100.0)/brg_value) - 100.0)
            relative_values.append(relative_value)
    
        bigtuple = t + tuple(absolute_values) + tuple(relative_values)
        print(TABLELINE_STR % bigtuple)

if __name__=="__main__":
    main()
