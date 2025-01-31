#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Calcula o aumento de eficiencia pela estrategia AAI para
# 50 arestas e armazena os valores em arquivos.

import networkx as nx
import pp, sys, time, os
import copy as cp
import pickle
import itertools as it

def TestAllEfficiency(G, num):
	combinations = list(it.combinations(G.nodes(), 2))

	ppservers = ()#("a3.ft.unicamp.br","a5.ft.unicamp.br","a6.ft.unicamp.br","a9.ft.unicamp.br")
	#ppservers = ("192.168.0.42","192.168.0.3")
	job_server = pp.Server(ppservers=ppservers)
	results = dict()
	print "Starting calcs with " + str(len(combinations)) + " combinations" 
	i = 0	
	jobs = []
	for edge in combinations:
		if(not(G.has_edge(*edge))):
			i = i+1	
			job_server.submit(Diff, (G, edge), depfuncs=(GlobalEfficiency,), modules=("networkx as nx",), callback=addInResults,callbackargs=(results,))

			if(i>100):
				i = 0
				job_server.wait()

	job_server.wait()

	f = open("dados/eff_edge_"+str(num)+".res",'w')
	SaveInFile(f, results)
	f.close()
	job_server.print_stats()

	maximum = max(results, key=results.get)

	return maximum
	
def Diff(G, edge):
	G.add_edge(*edge)
	finalEff = GlobalEfficiency(G)
	G.remove_edge(*edge)
	ret = (edge, finalEff)
	return ret

def addInResults(results, value):
	results[value[0]] = value[1]

def SaveInFile(f, results):
	pickle.dump(results, f)

def GlobalEfficiency(G):
    avg = 0.0
    n = len(G)
    for node in G:
        path_length=nx.single_source_dijkstra_path_length(G, node, weight='weight')
        avg += sum(1.0/v for v in path_length.values() if v !=0)
    avg *= 1.0/(n*(n-1))
    return avg



#Main program
def Main():
	filename = sys.argv[1]
	
	G = nx.read_gml(filename)
	G = G.to_undirected()

	#pega somente o maior subgrafo
	if(not(nx.is_connected(G))):
		G = nx.connected_component_subgraphs(G)[0]

	edges = []
	#adiciona 50 arestas pela AAI
	for i in xrange(50):
		print "Starting graph "+str(i)
		new_edge = TestAllEfficiency(G,i)
		edges.append(new_edge)
		print new_edge
		G.add_edge(*new_edge)

	#salva em arquivo as arestas
	SaveInFile(open('dados/edges.pickle','w'), edges)

Main()
