Diretório de Arquivos

Neste diretório se encontram os arquivos gerados pelos scripts utilizados nesta pesquisa.

Na raiz, o arquivo "aleatorio-scalefree.xls" é uma planilha contendo o aumento de eficiência para 1000 redes aleatórias e 1000 redes scale-free utilizando todas as estratégias propostas na pesquisa.

Na pasta "dano", estão os arquivos resultantes do teste de resiliência para falhas aleatorias e planejadas das redes resultantes pela adição de 50 arestas na rede original utilizando as estratégias propostas. Os arquivos se encontram no formato "pickle", um tipo de arquivo próprio para armazenar e ler dados por programas na linguagem Python.

No diretório "estratégias" encontram-se os arquivos, também no formato "pickle", com o aumento de eficiência trazido pelas estratégias utilizadas. A pasta "AAI" tem o aumento de eficiência para todas as combinações de arestas na rede, repetido 50 vezes, após adicionar a aresta de maior aumento no cálculo anterior. O arquivo "AAI.pickle" tem o aumento por cada aresta ideal adicionada e o arquivo "AAI-arestas.pickle" possui a combinação de arestas. Nas pastas "mincut" e "normal" tem-se os arquivos com o aumento trazido pela adição de 50 arestas, respectivamente com e sem o auxílio do procedimento mincut.

Na pasta "redes" estão a rede original "altatensao.gml" e todas as redes geradas pela utilização das estratégias propostas. Esta rede original foi utilizada por todos os scripts do projeto.
