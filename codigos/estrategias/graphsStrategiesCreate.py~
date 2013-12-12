#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa gera e grava em arquivo GML os grafos com 50
# arestas adicionais usando todas as estrategias com e sem auxílio 
# do mincut.
# -------
# Dependencias:
# strategiesHVN50edgesMincut.py
# strategiesHVN50edgesNormal.py

import pp, sys, time, os
import networkx as nx
import copy as cp
import pickle
import strategiesHVN50edgesMincut as mincut
import strategiesHVN50edgesNormal as normal

os.system("clear")

G = nx.read_gml("../altatensao.gml")

#pega somente o maior subgrafo
if(not(nx.is_connected(G))):
	G = nx.connected_component_subgraphs(G)[0]

path = "grafos/"

res = open("dados/edges.pickle", 'r')
bestEdges = pickle.load(res)

#criacao dos grafos
GBest = cp.deepcopy(G)
GBest.add_edges_from(bestEdges)

GCMdN, edges = normal.add50edges(cp.deepcopy(G), normal.findCMdEdge)
GVVzN, edges = normal.add50edges(cp.deepcopy(G), normal.findVVGEdge)
GMGrN, edges = normal.add50edges(cp.deepcopy(G), normal.findVMGEdge)
GMCaN, edges = normal.add50edges(cp.deepcopy(G), normal.findVMBEdge)

GCMdM, edges = mincut.add50edges(cp.deepcopy(G), mincut.findCMdEdge)
GVVzM, edges = mincut.add50edges(cp.deepcopy(G), mincut.findVVGEdge)
GMGrM, edges = mincut.add50edges(cp.deepcopy(G), mincut.findVMGEdge)
GMCaM, edges = mincut.add50edges(cp.deepcopy(G), mincut.findVMBEdge)

#gravacao dos grafos
nx.write_gml(GBest, path+"AAI.gml")
nx.write_gml(GCMdN, path+"CMdNormal.gml")
nx.write_gml(GVVzN, path+"VVzNormal.gml")
nx.write_gml(GMGrN, path+"MGrNormal.gml")
nx.write_gml(GMCaN, path+"MCaNormal.gml")
nx.write_gml(GCMdM, path+"CMdMincut.gml")
nx.write_gml(GVVzM, path+"VVzMincut.gml")
nx.write_gml(GMGrM, path+"MGrMincut.gml")
nx.write_gml(GMCaM, path+"MCaMincut.gml")
