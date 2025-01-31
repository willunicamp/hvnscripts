#!/usr/bin/python
# File: destroy.py
# Author: William paiva
# Email: will.unicamp@gmail.com
# Desc: Este programa faz o teste de resiliencia da rede contra
# falhas planejadas

import networkx as nx
import pp, sys, time, random, os
import copy as cp
import matplotlib 
import matplotlib.pyplot as plt
import pickle

#calculates capacity based on a initial factor
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
    

def Attack(G, capacity):
	results = dict()
	G = setCapacity(G, capacity)
	#print b.values()

	#aqui eh necesssario calcular o betweenness e remover o maior link

	b=nx.edge_betweenness_centrality(G, normalized=True, weight='weight')
	vals=list(b.values())
	keys=list(b.keys())
	max_link = keys[vals.index(max(vals))]				

	start_eff = GlobalEfficiency(G)
	final_eff = start_eff

	G.remove_edge(max_link[0],max_link[1])

	for i in xrange(50):
		#havera aqui 50 iteracoes de calculo de eficiencia para cada novos
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

		eff = GlobalEfficiency(G)
		final_eff = eff if eff < final_eff else final_eff

	#calcula e retorna o dano na rede
	damage = (start_eff-final_eff)/start_eff
	return damage




#DRAW
'''
def Draw(xvalues, yvalues, name):
		fig = plt.figure(1,figsize=(6,3))
		fig.clf()
		ax = plt.subplot(111)
		#define os eixos
		ax.set_xlabel("capacidade (C)")
		ax.set_ylabel("dano (D)")
		plt.xlim(1.0,2.0)
		#plt.ylim(0,max(yvalues)+(max(yvalues)/10))
		plt.title("Dano na rede para diferentes valores de capacidade de sobrecarga")

		plt.plot(xvalues, yvalues,'-', color="#000000")

		#salva o grafico
		plt.savefig("imagens/"+name+".eps", dpi=300, bbox_inches='tight')
'''

def start(G, name):
	#pega somente o maior subgrafo
	if(not(nx.is_connected(G))):
		G = nx.connected_component_subgraphs(G)[0]

	# tuple of all parallel python servers to connect with
	ppservers = ()
	#ppservers = ("a3.ft.unicamp.br","a9.ft.unicamp.br","a7.ft.unicamp.br","a8.ft.unicamp.br","a10.ft.unicamp.br")
        job_server = pp.Server(ppservers=ppservers)
        job_server.set_ncpus(1)

	job = []
	capacities = []
	damage = []
	ran = 30 #range
	print "server e variaveis carregados"

	for i in xrange(1,ran):
		#Aqui faz-se um range de para 50 valores diferentes de capacidade inicial na rede
		capacity = 1.0+(1.0/float(ran)*float(i))
		job.append(job_server.submit(Attack, (cp.copy(G),capacity),(GlobalEfficiency,setCapacity), ("networkx as nx",)))
		capacities.append(capacity)

	job_server.wait()

	for i in xrange(len(job)):
		damage.append(job[i]())

	#Salva o arquivo da estrategia testada
        res = (capacities, damage)
        pickle.dump(res, open("dados/planejada/"+name+".pickle","w"))
        job_server.print_stats()

os.system("clear")

path = "../estrategias/grafos/"
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
