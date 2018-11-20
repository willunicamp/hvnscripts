Este arquivo é um pequeno guia para executar os arquivos contidos neste diretório da forma correta. Verifique se possui instalado os módulos necessários antes de executar estes arquivos.

O arquivo download_rede.py é responsável por acessar o site do SINDAT da ONS e transformar os dados disponibilizados em HTML no formato GML, além de salvar duas imagens do grafo nos formatos EPS e PNG. Na primeira execução, é necessário adicionar o parâmetro 'yes' como primeiro argumento, para que o programa faça o download do arquivo de linhas e o salve como "linhas.html".

>python download_rede.py yes

Além deste arquivo, há mais dois diretórios, "estratégias" e "falhas". No primeiro, tem-se os scripts que calculam a eficiência da rede para a adição de novas arestas, para todas as estratégias, com o grafo original e com os grafos artificiais. No diretório "falhas", encontram-se os scripts que fazem o teste de resiliência da rede. Detalhes de como executar os arquivos destes diretórios encontram-se nos arquivos "leiame.txt" presentes em cada um.

---

Este arquivo é um pequeno guia para executar os arquivos contidos neste diretório da forma correta. Verifique se possui instalado os módulos necessários antes de executar estes arquivos.

O arquivo download_rede.py é responsável por acessar o site do SINDAT da ONS e transformar os dados disponibilizados em HTML no formato GML, além de salvar duas imagens do grafo nos formatos EPS e PNG. Na primeira execução, é necessário adicionar o parâmetro 'yes' como primeiro argumento, para que o programa faça o download do arquivo de linhas e o salve como "linhas.html".

>python download_rede.py yes

Além deste arquivo, há mais dois diretórios, "estratégias" e "falhas". No primeiro, tem-se os scripts que calculam a eficiência da rede para a adição de novas arestas, para todas as estratégias, com o grafo original e com os grafos artificiais. No diretório "falhas", encontram-se os scripts que fazem o teste de resiliência da rede. Detalhes de como executar os arquivos destes diretórios encontram-se nos arquivos "leiame.txt" presentes em cada um.
