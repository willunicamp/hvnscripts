Este arquivo é um pequeno guia para executar os arquivos contidos neste diretório da forma correta. Verifique se possui instalado os módulos necessários antes de executar estes arquivos.

O arquivo download_rede.py é responsável por acessar o site do SINDAT da ONS e transformar os dados disponibilizados em HTML no formato GML, além de salvar duas imagens do grafo nos formatos EPS e PNG. Na primeira execução, é necessário adicionar o parâmetro 'yes' como primeiro argumento, para que o programa faça o download do arquivo de linhas e o salve como "linhas.html".

UPDATE: infelizmente o SINDAT foi modificado e não é mais possível efetuar o download com o script download_rede.py.

>python download_rede.py yes

Além deste arquivo, há mais dois diretórios, "estratégias" e "falhas". No primeiro, tem-se os scripts que calculam a eficiência da rede para a adição de novas arestas, para todas as estratégias, com o grafo original e com os grafos artificiais. No diretório "falhas", encontram-se os scripts que fazem o teste de resiliência da rede. Detalhes de como executar os arquivos destes diretórios encontram-se nos arquivos "leiame.txt" presentes em cada um.

---

This is a short file to execute the scripts in this directory. Check if you have the needed modules before execute them.

The file "download_rede.py" is responsible to acces the ONS SINDAT website and transform the available data from HTML to GML format and to transform it into two figures in the format EPS and PNG. In the first execution, it is necessary to provide the first parameter as "yes", telling the script to download the data.

>python download_rede.py yes

UPDATE: unfortunately, the SINDAT system was modified and is no longer possible to download the data using the script download_rede.py.

There are two more folders, the "estratégias" e "falhas". In the first, you can find the scripts responsible to calculate the network efficiency after adding new edges, for all the strategies and for any providade graph. In the "falhas" directory, the scripts responsible to test the network resilience can be found. Details on how to execute these scripts can be found in the README.md inside their folders.
