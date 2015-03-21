#!/usr/bin/python
# encoding: utf-8
# Juliano Fischer Naves
# 20 de Janeiro de 2013
#
# Deve ser chamado dentro do diretório onde serão agregados os resultados
# Um exemplo: /infocom/maxprop/
# Dentro de maxprop podem variar os valores de buffer

import os
from math import sqrt


ic_95 = {1:12.706, 2:4.303, 3:3.182, 4:2.776, 5:2.571, 
         6:2.447, 7:2.365, 8:2.306, 9:2.262, 10:2.228,
         11:2.201, 12:2.179, 13:2.160, 14:2.145, 15:2.131,
         16:2.120, 17:2.110, 18:2.101, 19:2.093, 20:2.086,
         21:2.080, 22:2.074, 23:2.069, 24:2.064, 25:2.060, 
         26:2.056, 27:2.052, 28:2.048, 29:2.045, 30:2.042,
         31:2.040, 32:2.037, 33:2.035, 34:2.032, 35:2.030,
}

#Calcula a média
def media(lista):
    return float(sum(lista))/len(lista)

#Calcula o desvio padrão
def desvPad(lista):
    med = media(lista)
    soma = 0
    for i in lista:
         soma = (i - med)**2 + soma
    return float(soma)/(len(lista) - 1)


#calcula a variância
def variancia(lista):
    desvio = desvPad(lista)
    return sqrt(desvio)
    
#calcula o intervalo de confiança utilizando a distribuição
#t-student e nível de 95% de confiança
#toDo: disponibilizar opção de escolher o nível de conf.
def confidence(lista):
    graus_de_liberdade = len(lista) - 1
    try:
        value = ic_95[graus_de_liberdade]
        confidenceValue = value * (variancia(lista)/sqrt(len(lista)))
        return confidenceValue
    except:
        print("Impossível calcular para este número de amostras...")

import os

CONST_DELIVERY = "delivery_prob"
CONST_OVERHEAD = "overhead_ratio"
CONST_LATENCY = "latency_avg"
CONST_HOPCOUNT_AVG = "hopcount_avg"
CONST_BUFFERTIME_AVG = "buffertime_avg"
CONST_DROPPED = "dropped"
SIMULATION_TIME = "sim_time"

CONST_CREATED = "created"
CONST_RELAYED = "relayed"
CONST_ABORTED = "aborted"
CONST_REMOVED = "removed"
CONST_LATENCY_MED = "latency_med"
CONST_HOPCOUNT_MED = "hopcount_med"
CONST_BUFFERTIME_MED = "buffertime_med"

delivery_rate = []
overhead = []
latency_avg = []
hopcount_avg = []
buffertime_avg = []
dropped = []
sim_time = []

created = []
relayed = []
aborted = []
removed = []
latency_med = []
hopcount_med = []
buffertime_med = []

def grava_arquivo(nome,lista):
    with open(nome,'w') as f:
        for linha in lista:
            f.write(linha)

def procura_valor(term,linha,number,lista,offset):
   if linha.find(term) != -1:
       value = str(number)+" "+linha[offset:]
       lista.append(value)

#pega os arquivos da pasta atual
pastas = os.listdir('.')
#ordena os arquivos
pastas.sort(key=int)
#buffer_size = 0
buffer_size = ""
for pasta in pastas:
	if os.path.isdir(pasta):
	    #o tamanho do buffer é o número da pasta
	    #também pode ser a quantidade de nós maliciosos
	    #é o valo que muda a cada 10 rodadas de simulação
	    buffer_size = pasta
        print "Buffer :" + buffer_size + ", "+str(pasta)
        arquivos = os.listdir(pasta)
        
        ### List comprehension: lista somente os arquivos MessageStatsReport
        arquivos = [a for a in arquivos if a.find("MessageStatsReport") != -1]
        
        for arquivo in arquivos:
            
            arq = open(pasta+"/"+arquivo,'r')
            for linha in arq.readlines():
                procura_valor(CONST_DELIVERY,linha,buffer_size,delivery_rate,15)
                procura_valor(CONST_LATENCY,linha,buffer_size,latency_avg,13)
                procura_valor(CONST_HOPCOUNT_AVG,linha,buffer_size,hopcount_avg,13)
                procura_valor(CONST_BUFFERTIME_AVG,linha,buffer_size,buffertime_avg,15)
                procura_valor(CONST_OVERHEAD,linha,buffer_size,overhead,16)
                procura_valor(CONST_DROPPED,linha,buffer_size,dropped,8)
                procura_valor(SIMULATION_TIME,linha,buffer_size,sim_time,9)
                procura_valor(CONST_CREATED,linha,buffer_size,created,8)
                procura_valor(CONST_RELAYED,linha,buffer_size,relayed,8)
                procura_valor(CONST_ABORTED,linha,buffer_size,aborted,8)
                procura_valor(CONST_REMOVED,linha,buffer_size,removed,8)
                procura_valor(CONST_LATENCY_MED,linha,buffer_size,latency_med,13)
                procura_valor(CONST_HOPCOUNT_MED,linha,buffer_size,hopcount_med,13)
                procura_valor(CONST_BUFFERTIME_MED,linha,buffer_size,buffertime_med,15)
                
            arq.close()

		#buffer_size = buffer_size + 1

grava_arquivo("delivery_rate.agregado",delivery_rate)
grava_arquivo("overhead.agregado",overhead)
grava_arquivo("latency.agregado",latency_avg)
grava_arquivo("buffertimeavg.agregado",buffertime_avg)
grava_arquivo("hopcount_avg.agregado",hopcount_avg)
grava_arquivo("dropped.agregado",dropped)
grava_arquivo("sim_time.agregado",sim_time)
grava_arquivo("created.agregado",created)
grava_arquivo("relayed.agregado",relayed)
grava_arquivo("aborted.agregado",aborted)
grava_arquivo("latency_med.agregado",latency_med)
grava_arquivo("hopcount_med.agregado",hopcount_med)
grava_arquivo("buffertime_med.agregado",buffertime_med)
grava_arquivo("removed.agregado",removed)

os.system ('agrega_gnuplot')
