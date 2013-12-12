#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa adiciona 50 arestas na rede usando todas as
# estrategias SEM auxilio do mincut. Em seguida, gera os gráficos
# de comparacao das estrategias.

import networkx as nx
import pp, sys, time, os
import copy as cp
import pickle
import itertools as it
from numpy import linalg as la
import numpy as np
import matplotlib.pyplot as plt

from networkx.utils import powerlaw_sequence

def DrawGraph(G, edges, img):
	fig = plt.figure(1,figsize=(8,8))
	fig.clf()
	pos=nx.graphviz_layout(G,prog="neato")

	#desenha o grafo
	nx.draw(G,pos,node_color='#000000',node_size=10,with_labels=False, edge_color='#AAAAAA',linewidths=0.0)
	#nx.draw_networkx_nodes(G,pos,nodelist=nodesleft,node_size=20,node_color='r')
	nx.draw_networkx_edges(G,pos, edgelist=edges, width=2,edge_color='#333333')
	plt.savefig("results/normal/images/"+img, dpi=300, transparent=False, format="eps")
	#plt.show()

def Compare(G):
	realEff = GlobalEfficiency(G)
	f = open("results/normal/strategies/real.data", 'w')
	pickle.dump(realEff, f)
	print "OKOK"

	edgeCentral = mostCentralEdge(G)

	maxG = cp.deepcopy(G)
	edgeMax = (180,359) #valor encontrado por outro algoritmo
	maxG.add_edge(*edgeMax)
	finalMaxEff = GlobalEfficiency(maxG)
	print nx.info(maxG)

	DrawGraph(maxG, [edgeMax], "MaxEdge.eps")

	#Adiciona melhores arestas encontradas
	#pelo cluster
	GBestEdges, edges = add50edges(cp.deepcopy(G), findBestEdge)
	bestEdgesEff = GlobalEfficiency(GBestEdges)
	DrawGraph(GBestEdges, edges, "BestEdges.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de betweenness medianos
	GMedBet, edges = add50edges(cp.deepcopy(G), findMedBetEdge)
	finalVmbetfEff = GlobalEfficiency(GMedBet)
	DrawGraph(GMedBet, edges, "MedBet.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de coeficiente de cluster medianos
	GMedCl, edges = add50edges(cp.deepcopy(G), findMedClEdge)
	finalVmclfEff = GlobalEfficiency(GMedCl)
	DrawGraph(GMedCl, edges, "MedCl.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau vizinhos dos de maior betweenness
	GVvg, edges = add50edges(cp.deepcopy(G), findVVGEdge)
	finalVvgEff = GlobalEfficiency(GVvg)
	DrawGraph(GVvg, edges, "VVG.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau
	GVmg, edges = add50edges(cp.deepcopy(G), findVMGEdge)
	finalVmgEff = GlobalEfficiency(GVmg)
	DrawGraph(GVmg, edges, "VMG.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor betweenness, com betweenness
	#maior que zero
	GVmb, edges = add50edges(cp.deepcopy(G), findVMBEdge)
	finalVmbEff = GlobalEfficiency(GVmb)
	DrawGraph(GVmb, edges, "VMB.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor coeficiente de cluster, com os
	#coeficientes maiores que zero
	GVcf, edges = add50edges(cp.deepcopy(G)	, findVCCEdge)
	finalVcfEff = GlobalEfficiency(GVcf)
	DrawGraph(GVcf, edges, "VCC.eps")

	print "Default efficiency: \t\t" + str(realEff) + " - 100%"
	print "Most central edge: \t\t" + str(edgeCentral)
	print "Maximum efficiency: \t\t" + str(finalMaxEff) + " - " + str(100.0*finalMaxEff/realEff) + "\t " + str(edgeMax)
	print "Best efficiency (min-cut): \t\t" + str(bestEdgesEff) + " - " + str(100.0*bestEdgesEff/realEff) 
	print "VVG efficiency (min-cut): \t\t" + str(finalVvgEff) + " - " + str(100.0*finalVvgEff/realEff) 
	print "VMG efficiency (min-cut): \t\t" + str(finalVmgEff) + " - " + str(100.0*finalVmgEff/realEff)
	print "VMB efficiency (min-cut): \t\t" + str(finalVmbEff) + " - " + str(100.0*finalVmbEff/realEff)
	print "VCF efficiency (min-cut): \t\t" + str(finalVcfEff) + " - " + str(100.0*finalVcfEff/realEff)
	print "VMedCl efficiency (min-cut): \t\t" + str(finalVmclfEff) + " - " + str(100.0*finalVmclfEff/realEff)
	print "VMedBet efficiency (min-cut): \t\t" + str(finalVmbetfEff) + " - " + str(100.0*finalVmbetfEff/realEff)

def CompareOneEdge(G, edgeMax,name):
	realEff = GlobalEfficiency(G)
	#f = open("results/normal/strategies/real.data", 'w')
	#pickle.dump(realEff, f)
	#print "OKOK"

	edgeCentral = mostCentralEdge(G)

	maxG = cp.deepcopy(G)
	maxG.add_edge(*edgeMax)
	finalMaxEff = GlobalEfficiency(maxG)
	print nx.info(maxG)

	DrawGraph(maxG, [edgeMax], name+"MaxEdge.eps")

	#Adiciona melhores arestas encontradas
	#pelo cluster
	GBestEdges, edges = addOneEdge(cp.deepcopy(G), emax(edgeMax))
	bestEdgesEff = GlobalEfficiency(GBestEdges)
	DrawGraph(GBestEdges, edges, name+"BestEdge.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de betweenness medianos
	GMedBet, edges = addOneEdge(cp.deepcopy(G), findMedBetEdge)
	finalVmbetfEff = GlobalEfficiency(GMedBet)
	DrawGraph(GMedBet, edges, name+"MedBet.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau vizinhos dos de maior betweenness
	GVvg, edges = addOneEdge(cp.deepcopy(G), findVVGEdge)
	finalVvgEff = GlobalEfficiency(GVvg)
	DrawGraph(GVvg, edges, name+"VVG.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau
	GVmg, edges = addOneEdge(cp.deepcopy(G), findVMGEdge)
	finalVmgEff = GlobalEfficiency(GVmg)
	DrawGraph(GVmg, edges, name+"VMG.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor betweenness, com betweenness
	#maior que zero
	GVmb, edges = addOneEdge(cp.deepcopy(G), findVMBEdge)
	finalVmbEff = GlobalEfficiency(GVmb)
	DrawGraph(GVmb, edges, name+"VMB.eps")

	print "Default efficiency: \t\t" + str(realEff) + " - 100%"
	print "Most central edge: \t\t" + str(edgeCentral)
	print "Maximum efficiency: \t\t" + str(finalMaxEff) + " - " + str(100.0*finalMaxEff/realEff) + "\t " + str(edgeMax)
	print "Best efficiency (min-cut): \t\t" + str(bestEdgesEff) + " - " + str(100.0*bestEdgesEff/realEff) 
	print "VVG efficiency (min-cut): \t\t" + str(finalVvgEff) + " - " + str(100.0*finalVvgEff/realEff) 
	print "VMG efficiency (min-cut): \t\t" + str(finalVmgEff) + " - " + str(100.0*finalVmgEff/realEff)
	print "VMB efficiency (min-cut): \t\t" + str(finalVmbEff) + " - " + str(100.0*finalVmbEff/realEff)
	print "VMedBet efficiency (min-cut): \t\t" + str(finalVmbetfEff) + " - " + str(100.0*finalVmbetfEff/realEff)


#Funcao de Min-cut balanceado
def emax(p):
	return p

def MinCut(G):

	#Calcula a matriz laplaciana do grafo G
	#Opcionalmente, pode-se usar a laplaciana normalizada
	#lap = nx.normalized_laplacian(G)
	lap = nx.laplacian_matrix(G)
	eigenValues, eigenVectors = la.eigh(lap)

	orthoVector = []
	
	#pega-se entao os componentes orthonormais dos
	#autovetores e cria-se um novo vetor
	for vectors in eigenVectors:
		orthoVector.append(vectors[1])

	#para o Ratio-cut, usa-se a mediana para dividir
	#o grafo.
	#med = np.median(eigenVectors[1])

	nodesleft = []
	nodesright = []

	#divide-se entao o grafo em 2 componentes, baseado no sinal
	#do vetor orthonormal. Compara-se a lista de nodos com o vetor.
	#Se o valor for maior que zero, vai pra uma componente, caso contrario,
	#vai pra outra.
	for node, vec in zip(G.nodes(), orthoVector):
		if(vec > 0):
			nodesleft.append(node)
		else:
			nodesright.append(node)
	
	return (nodesleft, nodesright)



def add50edges(G, func, loops=50):
	i = 0
	tmpG = G
	efficiencies = []
	edges = []
	while(i<50):
		edge = func(tmpG)
		edges.append(edge)
		if(not(tmpG.has_edge(*edge))):
			#print str(func.__name__)+" | "+str(i)+" | "+str(G.number_of_edges()) #+" | "+str(GlobalEfficiency(tmpG))
			tmpG.add_edge(*edge)
			efficiencies.append(GlobalEfficiency(tmpG))
			i+=1
	f = open("results/normal/strategies/"+func.__name__+".data", 'w')
	pickle.dump(efficiencies, f)
	return tmpG, edges

def addOneEdge(G, func):
	i = 0
	tmpG = G
	edges = []

	edge = func(tmpG) if callable(func) else func
	edges.append(edge)
	if(not(tmpG.has_edge(*edge))):
		#print str(func.__name__)+" | "+str(i)+" | "+str(G.number_of_edges()) #+" | "+str(GlobalEfficiency(tmpG))
		tmpG.add_edge(*edge)
	return tmpG, edges

def mostCentralNodes(G):

	bet1 = 0
	degree1 = 0
	bet2 = 0
	degree2 = 0

	b = nx.betweenness_centrality(G)

	for node, bet in b.iteritems():
		if(float(bet) > bet1):
			bet1 = bet
			node1 = node
	
	del b[node1]

	for node, bet in b.iteritems():
		if(float(bet) > bet2):
			bet2 = bet
			node2 = node
	
	return (node1 ,node2)

def mostCentralEdge(G):
	b=nx.edge_betweenness_centrality(G)
	vals=list(b.values())
	keys=list(b.keys())
	max_link = keys[vals.index(max(vals))]
	return max_link

def findVVGEdge(G):

	node1 = 0
	degree1 = float("inf")
	node2 = 0
	degree2 = float("inf")
	i=0

	nodes = mostCentralNodes(G)

	neigh = (G.neighbors(nodes[0]), G.neighbors(nodes[1]))

	while True:
		for n in neigh[0]:
			if(G.degree(n) < degree1):
				degree1 = G.degree(n)
				node1 = n

		for n in neigh[1]:
			if(G.degree(n) < degree2):
				degree2 = G.degree(n)
				node2 = n

		edge = (node1,node2)

		if(G.has_edge(*edge)):
			neigh[i%2].remove(edge[i%2])
			degree1 = float("inf")
			degree2 = float("inf")
		else:
			break
		i+=1

	edgeVvg = edge
	return edgeVvg

def findBestEdge(G):
	return bestEdges.pop(0)

def findVMGEdge(G):

	node1 = 0
	degree1 = float("inf")
	node2 = 0
	degree2 = float("inf")
	i = 0

	nodes = cp.deepcopy(G.nodes())

	while(True):
		for n in nodes:
			if(G.degree(n) < degree1):
				degree1 = G.degree(n)
				node1 = n

		for n in nodes:
			if(G.degree(n) < degree2) and (n != node1):
				degree2 = G.degree(n)
				node2 = n

		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			nodes.remove(edge[i%2])
			degree1 = float("inf")
			degree2 = float("inf")
		i+=1

	return edge

def findVMBEdge(G):

	node1 = 0
	bet1 = float("inf")
	node2 = 0
	bet2 = float("inf")
	i = 0

	b = nx.betweenness_centrality(G)

	while(True):
		for node, bet in b.iteritems():
			if (float(bet) < bet1) and (bet > 0):
				bet1 = bet
				node1 = node

		for node, bet in b.iteritems():
			if (float(bet) < bet2) and (bet > 0) and (bet != bet1):
				bet2 = bet
				node2 = node

		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			del b[edge[i%2]]
			bet1 = float("inf")
			bet2 = float("inf")

		i+=1

	return edge

def findMedClEdge(G):
	node1 = 0
	cen1 = 0#float("inf")
	node2 = 0
	cen2 = 0#float("inf")
	nodelist = []

	closeness = nx.closeness_centrality(G)

	#for n in cut[0]:
	i = 0
	while(True):
		node1, node2 = median(closeness)
		edge = (node1,node2)

		if not(G.has_edge(*edge)):
			break
		p = i%2
		del closeness[edge[p]]
		i+=1

	return edge

def findMedBetEdge(G):
	node1 = 0
	cen1 = 0#float("inf")
	node2 = 0
	cen2 = 0#float("inf")

	betweenness = nx.betweenness_centrality(G)

	i = 0
	while(True):
		node1, node2 = median(betweenness)
		edge = (node1,node2)

		if not(G.has_edge(*edge)):
			break
		p = i%2
		del betweenness[edge[p]]
		i+=1

	return edge


def findVCCEdge(G):

	node1 = 0
	cen1 = float("inf")
	node2 = 0
	cen2 = float("inf")
	i = 0

	closeness = nx.closeness_centrality(G)

	while(True):
		for node, close in closeness.iteritems():
			if (float(close) < cen1) and (close > 0):
				cen1 = close
				node1 = node

		for node, close in closeness.iteritems():
			if (float(close) < cen2) and (close > 0) and (node != node1):
				cen2 = close
				node2 = node
		
		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			del closeness[edge[i%2]]
			cen1 = float("inf")
			cen2 = float("inf")

		i+=1

	return edge

def GlobalEfficiency(G):
    avg = 0.0
    n = len(G)
    for node in G:
        path_length=nx.single_source_dijkstra_path_length(G, node, weight='weight')
        avg += sum(1.0/v for v in path_length.values() if v !=0)
    avg *= 1.0/(n*(n-1))
    return avg

def median(vector):
	from collections import OrderedDict
	vector =  OrderedDict(sorted(vector.items(), key=lambda t: t[1]))
	res = 0
	n = len(vector)
	if n%2 == 1:
		res1 = vector.keys()[int((n-1)/2)]
		res2 = vector.keys()[int((n-1)/2)+1]
	else:
		res1 = vector.keys()[int((n-2)/2)]
		res2 = vector.keys()[int((n-2)/2)+1]
	return res1, res2
