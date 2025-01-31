#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa adiciona 50 arestas na rede usando todas as
# estrategias COM auxilio do mincut. Em seguida, gera os gráficos
# de comparacao das estrategias.

import networkx as nx
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
	plt.savefig("results/mincut/images/"+img, dpi=300, transparent=False, format="eps")
	#plt.show()

def Compare(G):
	realEff = GlobalEfficiency(G)

	edgeCentral = mostCentralEdge(G)

	maxG = cp.deepcopy(G)
	edgeMax = (180,359)
	maxG.add_edge(*edgeMax)
	finalMaxEff = GlobalEfficiency(maxG)
	#print nx.info(maxG)

	DrawGraph(maxG, [edgeMax], "AAI.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de betweenness medianos
	GMedBet, edges = add50edges(cp.deepcopy(G), findMedBetEdge)
	finalVmbetfEff = GlobalEfficiency(GMedBet)
	#print nx.info(GMedBet)
	DrawGraph(GMedBet, edges, "CMd.eps")


	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau vizinhos dos de maior betweenness
	GVvg, edges = add50edges(cp.deepcopy(G), findVVGEdge)
	finalVvgEff = GlobalEfficiency(GVvg)
	#print nx.info(GVvg)
	DrawGraph(GVvg, edges, "VVz.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor grau
	GVmg, edges = add50edges(cp.deepcopy(G), findVMGEdge)
	finalVmgEff = GlobalEfficiency(GVmg)
	#print nx.info(GVmg)
	DrawGraph(GVmg, edges, "MGr.eps")

	#Adiciona arestas usando estrategia de pegar os
	#vertices de menor betweenness, com betweenness
	#maior que zero
	GVmb, edges = add50edges(cp.deepcopy(G), findVMBEdge)
	finalVmbEff = GlobalEfficiency(GVmb)
	#print nx.info(GVmb)
	DrawGraph(GVmb, edges, "MCa.eps")


	print "Default efficiency: \t\t" + str(realEff) + " - 100%"
	print "Most central edge: \t\t" + str(edgeCentral)
	print "Maximum efficiency: \t\t" + str(finalMaxEff) + " - " + str(100.0*finalMaxEff/realEff) + "\t " + str(edgeMax)
	print "VVz efficiency (min-cut): \t\t" + str(finalVvgEff) + " - " + str(100.0*finalVvgEff/realEff) 
	print "MGr efficiency (min-cut): \t\t" + str(finalVmgEff) + " - " + str(100.0*finalVmgEff/realEff)
	print "MCa efficiency (min-cut): \t\t" + str(finalVmbEff) + " - " + str(100.0*finalVmbEff/realEff)
	print "CMd efficiency (min-cut): \t\t" + str(finalVmbetfEff) + " - " + str(100.0*finalVmbetfEff/realEff)


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
	GBestEdges, edges = addOneEdge(cp.deepcopy(G), edgeMax)
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
	while(i<loops):
		edge = func(tmpG)
		edges.append(edge)
		if(not(tmpG.has_edge(*edge))):
			#print str(func.__name__)+" | "+str(i)+" | "+str(G.number_of_edges()) #+" | "+str(GlobalEfficiency(tmpG))
			tmpG.add_edge(*edge)
			efficiencies.append(GlobalEfficiency(tmpG))
			i+=1
	f = open("dados/estrategias/mincut/"+func.__name__+".data", 'w')
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

	cut = MinCut(G)

	for n in cut[0]:
		if(float(b[n]) > bet1):
			bet1 = b[n]
			node1 = n

	for n in cut[1]:
		if(float(b[n]) > bet2):
			bet2 = float(b[n])
			node2 = n
	
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

def findVMGEdge(G):

	node1 = 0
	degree1 = float("inf")
	node2 = 0
	degree2 = float("inf")
	i = 0

	cut = MinCut(G)

	while(True):
		for n in cut[0]:
			if(G.degree(n) < degree1):
				degree1 = G.degree(n)
				node1 = n

		for n in cut[1]:
			if(G.degree(n) < degree2):
				degree2 = G.degree(n)
				node2 = n

		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			cut[i%2].remove(edge[i%2])
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

	cut = MinCut(G)

	b = nx.betweenness_centrality(G)

	while(True):
		for n in cut[0]:
			if((float(b[n]) < bet1) and (b[n] > 0)):
				bet1 = b[n]
				node1 = n

		for n in cut[1]:
			if((float(b[n]) < bet2) and (b[n] > 0)):
				bet2 = b[n]
				node2 = n

		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			cut[i%2].remove(edge[i%2])
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

	clustering = []
	clustering.append(dict())
	clustering.append(dict())

	cut = MinCut(G)

	for n in cut[0]:
		clustering[0][n] = nx.closeness_centrality(G, n)

	for n in cut[1]:
		clustering[1][n] = nx.closeness_centrality(G, n)

	#for n in cut[0]:
	i = 0
	while(True):
		med1 = median(clustering[0].values())
		med2 = median(clustering[1].values())
		node1 = [k for k, v in clustering[0].iteritems() if v == med1]
		node2 = [k for k, v in clustering[1].iteritems() if v == med2]

		edge = (node1[0] ,node2[0])

		if not(G.has_edge(*edge)):
			break
		p = i%2
		del clustering[p][edge[p]]
		i+=1

	return edge

def findMedBetEdge(G):
	node1 = 0
	cen1 = 0#float("inf")
	node2 = 0
	cen2 = 0#float("inf")
	nodelist = []

	betweenness = []
	betweenness.append(dict())
	betweenness.append(dict())

	cut = MinCut(G)

	bet = nx.betweenness_centrality(G)
	for n in cut[0]:
		if(bet[n] > 0):
			betweenness[0][n] = bet[n]

	for n in cut[1]:
		if(bet[n] > 0):
			betweenness[1][n] = bet[n]

	#for n in cut[0]:
	i = 0
	while(True):
		med1 = median(betweenness[0].values())
		med2 = median(betweenness[1].values())
		node1 = [k for k, v in betweenness[0].iteritems() if v == med1]
		node2 = [k for k, v in betweenness[1].iteritems() if v == med2]

		edge = (node1[0] ,node2[0])

		if not(G.has_edge(*edge)):
			break
		p = i%2
		del betweenness[p][edge[p]]
		i+=1

	return edge

def findBestEdge(G):
	return bestEdges.pop(0)

def findVCCEdge(G):

	node1 = 0
	cen1 = float("inf")
	node2 = 0
	cen2 = float("inf")
	i = 0

	c = nx.closeness_centrality(G)

	cut = MinCut(G)

	while(True):
		for n in cut[0]:
			if((float(c[n]) < cen1) and (c[n] > 0)):
				cen1 = c[n]
				node1 = n

		for n in cut[1]:
			if((float(c[n]) < cen2) and (c[n] > 0)):
				cen2 = c[n]
				node2 = n
		
		edge = (node1 ,node2)

		if not(G.has_edge(*edge)):
			break
		else:
			cut[i%2].remove(edge[i%2])
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
	vector = sorted(vector)
	res = 0
	n = len(vector)
	if n%2 == 1:
		res = vector[int((n-1)/2)]
	else:
		res = vector[int((n-2)/2)]
	return res
