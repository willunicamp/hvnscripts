#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Desc: This program makes the efficiency test with
# different capacities of load on the network

import networkx as nx
import pp, sys, time, os
import copy as cp
import pickle
import itertools as it

sys.path.append('50EdgesTest')
import strategiesHVN50edgesMincut as mincut
import strategiesHVN50edgesNormal as normal

#Funcao que testa a adicao da aresta 'edge' e calcula a nova eficiencia.
#em seguida remove a aresta mais central para verificar a queda
#Retorna um vetor com os valores das eficiencias
def TestEdge(G, func):
	edge = func(G)
	result = -1
	if(not(G.has_edge(*edge))):
		G.add_edge(*edge)
		result = normal.GlobalEfficiency(G)
		G.remove_edge(*edge)
		
	return result

def Compare(G):
	realEff = normal.GlobalEfficiency(G)

	vvgEffNormal = TestEdge(G, normal.findVVGEdge)#Vertices vizinhos de menor grau
	vmgEffNormal = TestEdge(G, normal.findVMGEdge)#Vertices de menor grau
	vmbEffNormal = TestEdge(G, normal.findVMBEdge)#Vertices de menor betweenness (betweenness > 0)
	medBEffNormal = TestEdge(G, normal.findMedBetEdge) #Vertices de menor coeficiente de cluster

	vvgEffMincut = TestEdge(G, mincut.findVVGEdge)#Vertices vizinhos de menor grau
	vmgEffMincut = TestEdge(G, mincut.findVMGEdge)#Vertices de menor grau
	vmbEffMincut = TestEdge(G, mincut.findVMBEdge)#Vertices de menor betweenness (betweenness > 0)
	medBEffMincut = TestEdge(G, mincut.findMedBetEdge) #Vertices de menor coeficiente de cluster

	result = (G.number_of_nodes(), G.number_of_edges(), (sum(G.degree().values())/float(G.number_of_nodes())),realEff, vvgEffNormal, vmgEffNormal, vmbEffNormal, medBEffNormal, vvgEffMincut, vmgEffMincut, vmbEffMincut, medBEffMincut)

	return result

def PrintResult(f, value):
	print >> f, value


#Inicio do programa
os.system("clear")

Gg = nx.read_gml("../altatensao.gml")
Gg.to_undirected()
Gg=nx.Graph(Gg)
Gg.remove_edges_from(Gg.selfloop_edges())
if(not(nx.is_connected(Gg))):
	Gg = nx.connected_component_subgraphs(Gg)[0]
print nx.info(Gg)
print "Max degree: " + str(max(nx.degree(Gg).values()))
print "Min degree: " + str(min(nx.degree(Gg).values()))
print "\n\n"

PrintResult(f, "Nodes, Edges, Med. Degree, Real Eff, VVz Normal, MGr Normal, MCa Normal, CMd Normal, VVz Mincut, MGr Mincut, MCa Mincut, CMd Mincut")
ppservers = ()#("192.168.0.42","192.168.0.3")
job_server = pp.Server(ppservers=ppservers)

for i in xrange(2000):
	filename = "dados/er_1000.txt"
	if (len(sys.argv) > 1):
		if (sys.argv[1] == "ba"):	
			Gg= nx.scale_free_graph(740)#nx.configuration_model(z)
			filename = "dados/ba_1000.txt"
		else:
			Gg= nx.erdos_renyi_graph(760,0.005)#nx.configuration_model(z)
	else:
		Gg= nx.erdos_renyi_graph(760,0.005)#nx.configuration_model(z)

	f = open(filename,'w')

	#Gg= nx.watts_strogatz_graph(737,4,0.5)
	Gg=nx.Graph(Gg)
	Gg.remove_edges_from(Gg.selfloop_edges())
	Gg.to_undirected()
	if(not(nx.is_connected(Gg))):
		Gg = nx.connected_component_subgraphs(Gg)[0]
	#print i
	#print "Max degree: " + str(max(nx.degree(Gg).values()))
	#print "Min degree: " + str(min(nx.degree(Gg).values()))
	#sys.exit()
	job_server.submit(Compare, (Gg,), depfuncs=(TestEdge,), modules=("networkx as nx","strategiesHVN50edgesMincut as mincut","strategiesHVN50edgesNormal as normal"),  callback=PrintResult, callbackargs=(f,))

	if(i%100==0):
		job_server.wait()

job_server.wait()
f.close()

job_server.print_stats()
