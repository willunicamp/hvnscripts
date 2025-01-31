import pickle, sys
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import networkx as nx

AAIFile = open("dados/planejadas/AAI.pickle", 'r')
originalFile = open("dados/planejadas/original.pickle", 'r')
CMdFile = open("dados/planejadas/CMdNormal.pickle", 'r')
MGrFile = open("dados/planejadas/MGrNormal.pickle", 'r')
VVzFile = open("dados/planejadas/VVzNormal.pickle", 'r')
MCaFile = open("dados/planejadas/MCaNormal.pickle", 'r')

original = pickle.load(originalFile)
AAI = pickle.load(AAIFile)
VVz = pickle.load(VVzFile)
MGr = pickle.load(MGrFile)
MCa = pickle.load(MCaFile)
CMd = pickle.load(CMdFile)

originalFile.close()
AAIFile.close()
VVzFile.close()
MGrFile.close()
MCaFile.close()
CMdFile.close()


#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.8])

lns0 = ax.plot(AAI[0], AAI[1], '--', label = 'Aresta ideal', color="#9999FF", linewidth=2.0)
lns4 = ax.plot(CMd[0], CMd[1], ':', label = 'CMd', color="#000000", linewidth=1.0)
lns2 = ax.plot(MGr[0], MGr[1], '--', label = 'MGr', color="#008800", linewidth=1.0)
lns1 = ax.plot(VVz[0], VVz[1], '-', label = 'VVz', color="#FF0000", linewidth=1.0)
lns3 = ax.plot(MCa[0], MCa[1], '-', label = 'MCa', color="#5555FF", linewidth=1.0)
lns5 = ax.plot(original[0], original[1], '-', label = 'Original', color="#000000", linewidth=1.0)

lns = lns0+lns1+lns2+lns3+lns4+lns5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha planejada na rede com 50 \nnovas arestas adicionadas pelas 4 estrategias")
plt.savefig("imagens/planejadas/dano_50_arestas_normal.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

CMdFile = open("dados/planejadas/CMdMincut.pickle", 'r')
MGrFile = open("dados/planejadas/MGrMincut.pickle", 'r')
VVzFile = open("dados/planejadas/VVzMincut.pickle", 'r')
MCaFile = open("dados/planejadas/MCaMincut.pickle", 'r')

VVz = pickle.load(VVzFile)
MGr = pickle.load(MGrFile)
MCa = pickle.load(MCaFile)
CMd = pickle.load(CMdFile)

VVzFile.close()
MGrFile.close()
MCaFile.close()
CMdFile.close()

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.8])

lns0 = ax.plot(AAI[0], AAI[1], '--', label = 'Aresta ideal', color="#9999FF", linewidth=2.0)
lns4 = ax.plot(CMd[0], CMd[1], ':', label = 'CMd', color="#000000", linewidth=1.0)
lns2 = ax.plot(MGr[0], MGr[1], '--', label = 'MGr', color="#008800", linewidth=1.0)
lns1 = ax.plot(VVz[0], VVz[1], '-', label = 'VVz', color="#FF0000", linewidth=1.0)
lns3 = ax.plot(MCa[0], MCa[1], '-', label = 'MCa', color="#5555FF", linewidth=1.0)
lns5 = ax.plot(original[0], original[1], '-', label = 'Original', color="#000000", linewidth=1.0)

lns = lns0+lns1+lns2+lns3+lns4+lns5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha planejada na rede com 50 \nnovas arestas adicionadas pelas 4 estrategias (min-cut)")
plt.savefig("imagens/planejadas/dano_50_arestas_mincut.eps", dpi=300, bbox_inches='tight')


#-------------=========-------------

CMdFileA = open("dados/planejadas/CMdMincut.pickle", 'r')
CMdFileF = open("dados/aleatorias/CMdMincut.pickle", 'r')

CMdA = pickle.load(CMdFileA)
CMdF = pickle.load(CMdFileF)

CMdFileA.close()
CMdFileF.close()

xvaluesA = CMdA[0]
xvaluesF = CMdF[0]

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.8])

lns0 = ax.plot(xvaluesF, CMdF[1], '-', label = 'Aleatorio', color="#FF0000", linewidth=1.0)
lns1 = ax.plot(xvaluesA, CMdA[1], '-', label = 'Planejado', color="#000000", linewidth=1.0)

lns = lns0+lns1
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha planejada e aleatoria na rede com 50 \nnovas arestas adicionadas pelas estrategia CMd com min-cut")
plt.savefig("images/dano_cmd.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

CMdFileM = open("dados/planejadas/CMdMincut.pickle", 'r')
CMdFileN = open("dados/planejadas/CMdNormal.pickle", 'r')

CMdM = pickle.load(CMdFileM)
CMdN = pickle.load(CMdFileN)

CMdFileM.close()
CMdFileN.close()

xvaluesM = CMdM[0]
xvaluesN = CMdN[0]

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.8])

lns0 = ax.plot(xvaluesM, CMdM[1], '-', label = 'Com min-cut', color="#FF0000", linewidth=1.0)
lns1 = ax.plot(xvaluesN, CMdN[1], '-', label = 'Sem min-cut', color="#000000", linewidth=1.0)

lns = lns0+lns1
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha planejada na rede com 50 novas\narestas adicionadas pelas estrategia CMd com e sem min-cut")
plt.savefig("images/dano_med_bet_plan.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

CMdFileM = open("pickle/failure/CMdMincut.pickle", 'r')
CMdFileN = open("pickle/failure/CMdNormal.pickle", 'r')

CMdM = pickle.load(CMdFileM)
CMdN = pickle.load(CMdFileN)

CMdFileM.close()
CMdFileN.close()

xvaluesM = CMdM[0]
xvaluesN = CMdN[0]

#define a figura
fig = plt.figure(1,figsize=(6,4))
fig.clf()
ax = plt.subplot(111)
ax.set_xlabel("capcidade (C)")
ax.set_ylabel("dano (D)")
plt.ylim([0.0, 0.8])

lns0 = ax.plot(xvaluesM, CMdM[1], '-', label = 'Com min-cut', color="#FF0000", linewidth=1.0)
lns1 = ax.plot(xvaluesN, CMdN[1], '-', label = 'Sem min-cut', color="#000000", linewidth=1.0)

lns = lns0+lns1
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.title("Dano por falha aleatoria na rede com 50 novas\narestas adicionadas pelas estrategia CMd com e sem min-cut")
plt.savefig("images/dano_med_bet_alea.eps", dpi=300, bbox_inches='tight')

#-------------=========-------------

#plt.figure(1,figsize=(8,8))
#fig.clf()
# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot, sfdp
#pos=nx.graphviz_layout(G,prog="neato")
