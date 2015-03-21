#!/usr/bin/python
# -*- coding: utf-8 -*-
# Juliano Fischer Naves
# ---------------------

import Gnuplot, Gnuplot.funcutils, sys, argparse


parser = argparse.ArgumentParser()
parser.add_argument("-x",help="Label for x axis")
parser.add_argument("-y", help="Label for y axis")
parser.add_argument("-f", help="The data file", required=True, nargs='*')
parser.add_argument("-c", help="A command list",nargs='*')
parser.add_argument("-o",help="The output file name")
parser.add_argument("-t",help="Title for datafiles", nargs='*')
parser.add_argument("-kb",help="key bottom",action='store_true')
parser.add_argument("-kr",help="key right",action='store_true')
parser.add_argument("-kl",help="key left",action='store_true')
parser.add_argument("-kt",help="key top",action='store_true')
parser.add_argument("-ki",help="key inside",action='store_true')
parser.add_argument("-ko",help="key outside",action='store_true')
parser.add_argument("-ls",help="line style",nargs='*')
parser.add_argument("-lc",help="line color",nargs='*',required=False)
parser.add_argument("-lw",help="line width",nargs='*',required=False)


print sys.argv

g = Gnuplot.Gnuplot(debug=1)
g("set encoding iso_8859_1")
#g("set terminal eps enhanced \"Times-Roman\" 30")
g("set terminal postscript eps size 4.0,3.0 enhanced color font 'Helvetica,24' linewidth 2")
g("set pointsize 2.5")
g("set style line 1 pt 4 lt 1 lw 1")
g("set style line 2 pt 6 lt 2 lw 1")
g("set style line 3 pt 8 lt 1 lw 1")
g("set style line 4 pt 10 lt 2 lw 1")
g("set style line 5 pt 12 lt 3 lw 1")
g("set style line 6 pt 5 lt -1 lw 1")
g("set style line 7 pt 7 lt 0 lw 1")
g("set style line 8 pt 8 lt 1 lw 1")
g("set style line 9 pt 11 lt 2 lw 1")
g("set style line 10 pt 13 lt 3 lw 1")


xlabel = "Tamanho do Buffer (MB)"
ylabel = "Taxa de Entrega (%)"
output = "saida.eps"
command_list = []
args = parser.parse_args(sys.argv[1:])
#print args

if args.y:
    ylabel = args.y
if args.x:
    xlabel = args.x
if args.o:
    output = args.o
if args.c:
    command_list = args.c

#xlabel = xlabel.encode("iso-8859-1")
#ylabel = ylabel.encode("iso-8859-1")
xlabel = xlabel.decode('utf-8')
xlabel = xlabel.encode('iso-8859-1')
ylabel = ylabel.decode('utf-8')
ylabel = ylabel.encode('iso-8859-1')

g("set output \""+output+"\"")
g("set xlabel \""+xlabel+"\"")
g("set ylabel \""+ylabel+"\"")

#comados passados por parâmetro
for command in command_list:
    g(command)


setkey = "set key"
if args.kb:
    setkey = setkey + " bottom"
elif args.kt:
    setkey = setkey + " top"

if args.kl:
    setkey = setkey + " left"
elif args.kr:
    setkey = setkey + " right"

g(setkey)

if args.ki:
    g("set key inside")
elif args.ko:
    g("set key outside")

aux = 0
plotlist = []
line_color = "black"
line_width = 1.0
lc = []

if args.lc:
    lc = args.lc

for f in args.f:
    tit = "Title"
    line_style = "0"
    if args.t[aux]:
        tit = args.t[aux]
        tit = tit.decode("utf-8")
        tit = tit.encode("iso-8859-1")
    if args.ls[aux]:
        line_style = args.ls[aux]
    
    #se for maior quer dizer que o indice chega a no
    #minimo aux       
    if len(lc) > aux:
        line_color = lc[aux]
    else:
        line_color = 'black'
    
    aux = aux + 1

    plotfile = "\"%s\" w errorlines t \"%s\" ls %s lc rgb '%s'" % (f,tit,line_style,line_color)
    plotlist.append(plotfile)

plot = ", ".join(plotlist)
plot = "plot "+plot

g(plot)

#print plot

