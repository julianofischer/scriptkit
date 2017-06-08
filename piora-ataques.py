#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# ---------------------

import sys

first_line = None
with open(sys.argv[1]) as f:
    first_line = f.readline().split()
    without_malicious = float(first_line[1])

    relative_values = []

    print("########## ABSOLUTA ##########")
    for i in range(1,6):
        with_malicious = float(f.readline().split()[1])
        print("%d    %f" % (i, (with_malicious-without_malicious)*100.0))
        relative_value = ((with_malicious * 100.0)/without_malicious) - 100.0
        relative_values.append(relative_value)

    print("########## RELATIVA ##########")
    for i,j in enumerate(relative_values):
        print("%d    %f" % (i,j))
