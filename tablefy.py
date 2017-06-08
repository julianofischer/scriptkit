#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# ---------------------

import sys
TABLE_STR = "\\textbf{%s}                                                                  & %.2f        & %.2f      & %.2f      & %.2f      & %.2f      & %.2f       & %.2f      & %.2f      & %.2f      & %.2f      \\\\ \\hline"

def main():
    for f in sys.argv[1:]:
        tablefy(f)

def tablefy(thefile):
    first_line = None
    with open(thefile) as f:
        first_line = f.readline().split()
        without_malicious = float(first_line[1])
        filename = thefile
        filename = (filename,) #converting into a tuple

        absolute_values = []
        relative_values = []

        for i in range(1,6):
            with_malicious = float(f.readline().split()[1])

            absolute_value = (with_malicious-without_malicious) * 100.0
            absolute_values.append(absolute_value)

            relative_value = ((with_malicious * 100.0)/without_malicious) - 100.0
            relative_values.append(relative_value)

        bigtuple = filename + tuple(absolute_values) + tuple(relative_values)
        print(TABLE_STR % bigtuple)

if __name__=="__main__":
    main()
