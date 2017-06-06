#!/usr/bin/python
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# ---------------------

import sys

first_line = None
with open(sys.argv[1]) as f:
    first_line = f.readline().split()

for i in range(6):
    print("%d    %s    %s" % (i, first_line[1], first_line[2]))



