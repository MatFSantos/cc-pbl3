# CCPBL3

Repositório destinado ao problema 3 da disciplina de Concorrência e Conectividade

## Requisitos

- É necessário ter o Python 3.7+ instalado com o Framework Flask, a extensão flask_cors e flask_restful.

## Organização das pastas e arquivos

- O projeto está organizado na pasta raiz, onde conta com seis arquivos ``.py`` e duas pastas que contém os mapas das companhias *A, B e C* e as classes:
  - **Pasta ``maps``**
    - Essa pasta contém três arquivos ``.txt``  que armazenam os mapas de cada companhia. Os arquivos são lidos quando o código é executado para carregar o mapa.
  - **Pasta ``model``**
    - Essa pasta possui as classes de cidade, mapa e rota,(``city.py``, ``map.py`` e ``route.py``) que dizem respeito a representação de grafo utilizada na solução.
  - **Arquivo ``api.py``**
    - Esse arquivo contém o código da classe *Api_Flask* que executa a *API rest* em uma *Thread*.
  - **Arquivo ``company.py``**
    - Esse arquivo contém o código da classe *Company* que representa a companhia do sistema. É nessa classe que as *Threads* da *API rest* e do servidor da companhia são iniciadas.
  - **Arquivo ``alive_client.py``**
    - Esse arquivo contém a classe *AliveClient* que nada mais é que uma *Thread* que executa à parte do servidor da companhia verificando o status das demais companhias.
  - **Arquivo ``alive_server.py``**
    - Esse arquivo contém a classe *AliveServer* que nada mais é que uma *Thread* que executa à parte do servidor da companhia recebendo comunicações de outros servidores de companhias e avisando o status da sua companhia.
  - **Arquivo ``broadcast_server.py``**
    - Esse arquivo contém o código do servidor socket que simula um broadcast para a rede de companhias. É nesse servidor que as companhias se comunicam no primeiro momento para conhecer as companhias.
  - **Arquivo ``company_server.py``**
    - Esse arquivo contém o código da classe *CompanyServer* que é o servidor da companhia que fica esperando requisições das demais companhias e faz o intermédio dos dados da sua companhia com as demais. É nessa classe também que as *Threads* de *AliveServer* e *AliveClient* são iniciadas.

## Como Executar

- Aqui será apresentado o passo a passo recomendável para executar o projeto.

  - Passo 1: Vá nos arquivos ``broadcast_server.py`` e ``company_server.py`` e altere os endereços das companhias que estão presentes no topo dos arquivos para os endereços corretos;

  - Passo 2: Na pasta raiz do projeto execute o arquivo ``company.py`` e informe uma das 3 companhias: *A, B ou C*.

    A partir daí uma companhia já foi iniciada, agora as demais companhias já podem ser iniciadas apenas repetindo o passo 2.

    >  **OBS:** os outros servidores que são iniciados, a *API rest* e o *AliveServer* tem seus endereços fixos de acordo com os endereços informados para o *CompanyServer*.
    >
    > - A *API rest* é iniciada no IP local onde o código é executado e as portas escolhidas foram ``52000``,``53000`` e ``54000`` para as companhias *A, B e C* respectivamente.
    >
    > - Já o *AliveServer* possui o mesmo IP informado para o *CompanyServer* e a porta é a ``porta do CompanyServer + 3000``


### Sobre as rotas

- Existem três rotas na API:
  - Rota 1: /{nome da companhia}/routes -> ``GET``
    - Retorna uma lista de possíveis caminhos que a companhia pode fazer independente de origem e destino.
  - Rota 2: /{nome da companhia}/{origin}/{destination} -> ``GET``
    - Retorna os possíveis caminhos que o conjunto de todas as companhias ativas podem fazer de uma origem à um destino informado.
  - Rota 3: /{nome da companhia}/buy -> ``POST``
    - Realiza a compra de uma passagem do caminho que é enviado como parâmetro
