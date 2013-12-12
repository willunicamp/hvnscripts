# Autor original: PAIVA, W.R., Faculdade de Tecnologia
# Universidade Estadual de Campinas
# Limeira, Outubro de 2012.
__author__ = """William Roberto de Paiva (will.unicamp@gmail.com)"""

import networkx as nx
import os
import re
import string
import sys
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.patches as mpatches
import random

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}

matplotlib.rc('font', **font)

TAG_RE = re.compile(r'<[^>]+>')
TAG_JS = re.compile(r"(?is)(<script[^>]*>)(.*?)(</script>)")

def remove_tags(text):
    return TAG_RE.sub('', text)

def remove_js(text):
    return TAG_JS.sub('', text)


#Limpa a tela
os.system("clear")

if(sys.argv[1] == 'yes'):
	os.system("wget http://aplicsindat.ons.org.br/sindat/search.cfm --output-document=linhas.html --force-html")

a = open("linhas.html")
texto = a.read()
texto = remove_js(texto)
texto = remove_tags(texto)
texto = texto.replace ('\t',' ')
texto = texto.replace ('\r',' ')
texto = texto.replace ('&nbsp;',' ')
while(texto.find ("  ") >= 0):
	texto = texto.replace ("  "," ")

while(texto.find ("\n\n") >= 0):
	texto = texto.replace ("\n\n","\n")

while(texto.find ("\n \n") >= 0):
	texto = texto.replace ("\n \n","\n")

texto = texto.strip()

myarr = string.split(texto,"\n")

G=nx.Graph()

for row in myarr:
	#remove desnecessario no final
	txtAux = row.strip()	
	last = txtAux.rfind(" ")
	last = txtAux[0:last].rfind(" ")	
	txtAux = txtAux[0:last]
	
	#remove desnecessario no inicio
	txtAux = txtAux.strip()	
	first = txtAux.find("kV ")+3	
	txtAux = txtAux[first:]
	
	vt1 = row.strip().find(" ")+1;
	vt2 = row.strip().find("kV ");
	voltage = row[vt1:vt2].strip()
	voltage = int(float(voltage.replace(",",".")))

	st1 = row.strip().rfind(" ")+1;
	states = row[st1:].strip()

	st2 = states.find("/")
	if(st2 > 0):
		st_source = states[0:st2]
		st_dest = states[st2+1:]
	else:
		st_source = states
		st_dest = states
	

	#divide os edges
	source = txtAux[0:txtAux.find("/")].strip()
	destiny = txtAux[txtAux.find("/")+1:].strip()
	G.add_node(source, uf=st_source)
	G.add_node(destiny, uf=st_dest)
	G.add_edge(source,destiny,voltage=voltage,capacity=0,weight=1.0)

#print(G.nodes(data=True))
G.to_undirected()
nx.write_gml(G,"altatensao.gml")


#Desenha colorido por estado

plt.figure(1,figsize=(8,8))
# layout graphs with positions using graphviz neato
# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot, sfdp
pos=nx.graphviz_layout(G,prog="neato")
# pos=nx.fruchterman_reingold_layout(G)

import colorsys
N = 30
HSV_tuples = [(x*1.0/N, random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)) for x in range(N)]
RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

print RGB_tuples[0]
nodes_color = []
states_color = {}
posi = 0
for v in G.nodes(data=True):
	uf = v[1].get('uf')
	if not uf in states_color:
		print "a"
        	states_color[uf] = RGB_tuples[posi]#[round(random.uniform(0, 0.9),1),round(random.uniform(0, 0.9),1),round(random.uniform(0, 0.9),1)]
		posi += 1
	nodes_color.append(states_color[uf])


#imprime a legenda dos estados
state_y = 2000
for key,value in states_color.items(): 
	art = mpatches.Rectangle((2500, state_y), 40, 40, color=value)
	plt.gca().add_patch(art)
	plt.text(2600, state_y, key, ha='left', rotation=0)
	state_y -= 60


#desenha o grafo
nx.draw(G,
     pos,
     node_size=[float(G.degree(v))*10 for v in G],
     node_color=nodes_color,
     with_labels=False
     )
plt.savefig("graph.eps",dpi=300)
plt.savefig("graph.png",dpi=300)
plt.show()
