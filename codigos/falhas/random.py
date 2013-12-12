#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa faz o teste de resiliencia da rede contra
# falhas aleatorias

import networkx as nx
import pp, sys, time, random, os
import copy as cp
import matplotlib 
import matplotlib.pyplot as plt
import pickle

#calcuelates capacity based on a initial factor
def setCapacity(G, factor):
	if(G.number_of_edges() > 0):
		bb=nx.edge_betweenness_centrality(G, normalized=True, weight='weight')

		for edge in G.edges(data=True):
			edge[2]['capacity'] = (bb[(edge[0],edge[1])]*factor)

	return G

def GlobalEfficiency(G):
    avg = 0.0
    n = len(G)
    for node in G:
        path_length=nx.single_source_dijkstra_path_length(G, node, weight='weight')
        avg += sum(1.0/v for v in path_length.values() if v !=0)
    avg *= 1.0/(n*(n-1))
    return avg
    

def Failure(originalG, capacity):
	import copy as cp
	import random
	damages = []
	originalG = setCapacity(originalG, capacity)

	start_eff = GlobalEfficiency(originalG)

	for time in xrange(80):
		G = cp.deepcopy(originalG)
		final_eff = start_eff
	
		e = random.choice(G.edges())
		G.remove_edge(*e)	

		for i in xrange(20):
			#havera aqui 20 iteracoes de calculo de eficiencia para cada novos
			#valores de capacidade, recalculando a eficiencia dos nos vizinhos ao removida
			#a aresta, simulando o efeito cascata
			bb=nx.edge_betweenness_centrality(G, normalized=True, weight='weight')
			for edge in G.edges(data=True):
				if(bb[(edge[0],edge[1])] > edge[2]['capacity']):
					cap = 0.000000000000001 if [edge[2]['capacity'] == 0] else edge[2]['capacity'] 
					#ao contrario do pensado, o peso deve ser aumentado, para aumentar os caminhos
					edge[2]['weight'] = (bb[(edge[0],edge[1])]/cap)
				else:
					#se a carga nao excede capacidade, tudo volta ao normal
					edge[2]['weight'] = 1.0

		final_eff = GlobalEfficiency(G)
		#final_eff = eff if eff < final_eff else final_eff
		G.add_edge(*e)	

		#calcula e retorna o dano na rede
		damage = (start_eff-final_eff)/start_eff
		damages.append(damage)
	
	#por ser falha, calcula a media dos danos aleatorios
	return sum(damages)/float(len(damages))

def CascadingEffect(G):

def start(G, name):
	#pega somente o maior subgrafo
	if(not(nx.is_connected(G))):
		G = nx.connected_component_subgraphs(G)[0]

	# tuple of all parallel python servers to connect with
	ppservers = ()
	#ppservers = ("a3.ft.unicamp.br","a9.ft.unicamp.br","a7.ft.unicamp.br","a8.ft.unicamp.br","a10.ft.unicamp.br")
	job_server = pp.Server(ppservers=ppservers)
	job_server.set_ncpus(4)
	job = []
	capacities = []
	damage = []
	ran = 20 #range
	print "server e variaveis carregados"

	for i in xrange(1,ran):
		#Aqui faz-se um range de para 20 valores diferentes de capacidade inicial na rede
		capacity = 1.0+(0.6/float(ran)*float(i))
		job.append(job_server.submit(Failure, (cp.copy(G),capacity),(GlobalEfficiency,setCapacity), ("networkx as nx",)))
		capacities.append(capacity)

	job_server.wait()

	for i in xrange(len(job)):
		damage.append(job[i]())

	#Salva o arquivo da estrategia testada
	res = (capacities, damage)
        pickle.dump(res, open("dados/aleatorias/"+name+".pickle","w"))
        job_server.print_stats()

os.system("clear")

path = "../../arquivos/redes/"
G = nx.read_gml(path+"../altatensao.gml")
GAAI = nx.read_gml(path+"AAI.gml")
GCMdN = nx.read_gml(path+"CMdNormal.gml")
GVVzN = nx.read_gml(path+"VVzNormal.gml")
GMGrN = nx.read_gml(path+"MGrNormal.gml")
GMCaN = nx.read_gml(path+"MCaNormal.gml")
GCMdM = nx.read_gml(path+"CMdMincut.gml")
GVVzM = nx.read_gml(path+"VVzMincut.gml")
GMGrM = nx.read_gml(path+"MGrMincut.gml")
GMCaM = nx.read_gml(path+"MCaMincut.gml")

start(G,"Original")
start(GAAI,"AAI")
start(GCMdN,"CMdNormal")
start(GVVzN,"VVzNormal")
start(GMGrN,"MGrNormal")
start(GMCaN,"MCaNormal")
start(GCMdM,"CMdMincut")
start(GVVzM,"VVzMincut")
start(GMGrM,"MGrMincut")
start(GMCaM,"MCaMincut")
