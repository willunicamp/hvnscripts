Este arquivo é um pequeno guia para executar os arquivos contidos neste diretório da forma correta. Verifique se possui instalado os módulos necessários antes de executar estes arquivos.

Executar primeiro o arquivo efficiency50Edges_AAI.py, para gerar os arquivos contendo as arestas ideais.

>python efficiency50Edges_AAI.py

Em seguida, executar o strategiesCompare.py, que irá gerar os gráficos comparativos de todas as estratégias.

>python strategiesCompare.py

Por ultimo, executar graphStrategisCreate.py para criar os grafos de todas as estrategias.

>python graphStrategisCreate.py

O arquivo strategies_1000_graphs.py é responsável por criar grafos artificiais Scale-Free e Aleatórios. Deve ser executado passando o parâmetro "ba" para redes Scale-Free e o parâmetro "er" para redes Aleatórias do modelo Erdós-Renyi.

>python strategies_1000_graphs.py ba
>python strategies_1000_graphs.py er
