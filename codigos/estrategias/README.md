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

---

This is a short guide to execute the scrips in this folder. Check if you have installed the necessary modules before to execute them.

Execute the first file efficiency50edges.py to generate the best edges files. It's recommended to use a high performance computer.

>python efficiency50Edges_AAI.py

Then you can execute the strategiesCompare.py, that will create the charts to compare all the strategies.

>python strategiesCompare.py

At last, you can execute the graphStrategiesCreate.py to create the graphs for all the strategies.

>python graphStrategisCreate.py

The file strategies_100_graphs.py is responsible to create the artificial Scale-Free and Random graphs. It must be executed providing the parameter "ba" for Barabási-Albert Scale Free networks, or "er" for Erdòs-Renyi Random graphs.

>python strategies_1000_graphs.py ba
>python strategies_1000_graphs.py er
