#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Desc: Este programa adiciona 50 arestas na rede usando todas as
# estrategias COM auxilio do mincut. Em seguida, gera os gráficos
# de comparacao das estrategias.

import pp, sys, time, os
import networkx as nx
import copy as cp
import pickle
import strategiesHVN50edgesMincut as mincut
import strategiesHVN50edgesMincut as normal

os.system("clear")

G = nx.read_gml("../nets/altatensao.gml")

res0 = open("results/edges0.pickle", 'r')
res1 = open("results/edges1.pickle", 'r')
bestEdges0 = pickle.load(res0)
bestEdges1 = pickle.load(res1)

bestEdges = bestEdges0 + bestEdges1

#pega somente o maior subgrafo
if(not(nx.is_connected(G))):
	G = nx.connected_component_subgraphs(G)[0]

print "Mincut starting"
mincut.Compare(cp.deepcopy(G))
print "Normal starting"
normal.Compare(cp.deepcopy(G))
