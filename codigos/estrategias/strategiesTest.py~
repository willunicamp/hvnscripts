#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa le dois arquivos contendo as arestas encontradas
# pelo procedimento AAI (adicao de arestas ideais) e calcula o aumento de eficiencia
# para 50 arestas por todas as estrategias, gerando os graficos comparativos.
# -------
# Dependencias:
# strategiesHVN50edgesMincut.py
# strategiesHVN50edgesNormal.py

import pp, sys, time, os
import networkx as nx
import copy as cp
import pickle
import strategiesHVN50edgesMincut as mincut
import strategiesHVN50edgesMincut as normal

os.system("clear")

G = nx.read_gml("../altatensao.gml")

#carrega os arquivos contendo as arestas escolhidas pelo AAI
res = open("dados/edges.pickle", 'r')

#variavel global contendo as arestas de AAI
bestEdges = pickle.load(res)

#pega somente o maior subgrafo
if(not(nx.is_connected(G))):
	G = nx.connected_component_subgraphs(G)[0]

#Inicia as comparacoes de estrategias com mincut
print "Mincut starting"
mincut.Compare(cp.deepcopy(G))
#inicia as comparacoes de estrategias sem mincut
print "Normal starting"
normal.Compare(cp.deepcopy(G))
