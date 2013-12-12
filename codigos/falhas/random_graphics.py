import pickle, sys
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import networkx as nx

AAIFile = open("dados/aleatorias/AAI.pickle", 'r')
originalFile = open("dados/aleatorias/original.pickle", 'r')
CMdFile = open("dados/aleatorias/CMdNormal.pickle", 'r')
MGrFile = open("dados/aleatorias/MGrNormal.pickle", 'r')
VVzFile = open("dados/aleatorias/VVzNormal.pickle", 'r')
MCaFile = open("dados/aleatorias/MCaNormal.pickle", 'r')

AAI = pickle.load(AAIFile)
VVz = pickle.load(VVzFile)
MGr = pickle.load(MGrFile)
MCa = pickle.load(MCaFile)
CMd = pickle.load(CMdFile)
original = pickle.load(originalFile)

originalFile.close()
AAIFile.close()
VVzFile.close()
MGrFile.close()
MCaFile.close()
CMdFile.close()

xvalues = MGr[0]
xvalues2 = MCa[0]

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.5])
plt.xlim([1.0, 1.6])

lns0 = ax.plot(AAI[0], AAI[1], '--', label = 'Aresta ideal', color="#9999FF", linewidth=2.0)
lns4 = ax.plot(CMd[0], CMd[1], ':', label = 'CMd', color="#000000", linewidth=1.0)
lns2 = ax.plot(MGr[0], MGr[1], '--', label = 'MGr', color="#008800", linewidth=1.0)
lns1 = ax.plot(VVz[0], VVz[1], '-', label = 'VVz', color="#FF0000", linewidth=1.0)
lns3 = ax.plot(MCa[0], MCa[1], '-', label = 'MCa', color="#5555FF", linewidth=1.0)
lns5 = ax.plot(original[0], original[1], '-', label = 'Original', color="#000000", linewidth=1.0)

lns = lns0+lns1+lns2+lns3+lns4+lns5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha aleatoria na rede com 50 \nnovas arestas adicionadas pelas 4 estrategias")
plt.savefig("imagens/aleatorias/dano_50_arestas_normal.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

CMdFile = open("dados/aleatorias/CMdMincut.pickle", 'r')
MGrFile = open("dados/aleatorias/MGrMincut.pickle", 'r')
VVzFile = open("dados/aleatorias/VVzMincut.pickle", 'r')
MCaFile = open("dados/aleatorias/MCaMincut.pickle", 'r')

VVz = pickle.load(VVzFile)
MGr = pickle.load(MGrFile)
MCa = pickle.load(MCaFile)
CMd = pickle.load(CMdFile)

VVzFile.close()
MGrFile.close()
MCaFile.close()
CMdFile.close()

xvalues = AAI[0]

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capacidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.5])
plt.xlim([1.0, 1.6])

lns0 = ax.plot(AAI[0], AAI[1], '--', label = 'Aresta ideal', color="#9999FF", linewidth=2.0)
lns4 = ax.plot(CMd[0], CMd[1], ':', label = 'CMd', color="#000000", linewidth=1.0)
lns2 = ax.plot(MGr[0], MGr[1], '--', label = 'MGr', color="#008800", linewidth=1.0)
lns1 = ax.plot(VVz[0], VVz[1], '-', label = 'VVz', color="#FF0000", linewidth=1.0)
lns3 = ax.plot(MCa[0], MCa[1], '-', label = 'MCa', color="#5555FF", linewidth=1.0)
lns5 = ax.plot(original[0], original[1], '-', label = 'Original', color="#000000", linewidth=1.0)

lns = lns0+lns1+lns2+lns3+lns4+lns5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha aleatoria na rede com 50 \nnovas arestas adicionadas pelas 4 estrategias (min-cut)")
plt.savefig("imagens/aleatorias/dano_50_arestas_mincut.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

#plt.figure(1,figsize=(8,8))
#fig.clf()
# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot, sfdp
#pos=nx.graphviz_layout(G,prog="neato")

