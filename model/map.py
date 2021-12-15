
class Map():
    """
        Classe que comporta o grafo com seus vértices (cidades ), servindo de mapa para as companhias.

        Atributos:
            cities -> lista de cidades do mapa
            number_of_cities -> número de cidades que o mapa possui
    """

    def __init__(self):
        """
            Instancia a classe Map, iniciando a lista de cidades vazia e o contador de cidades
        """
        self.cities = list()
        self.number_of_cities = 0

    def add_city(self, newCity):
        """
            Adiciona uma nova cidade ao mapa

            Parâmetros:
                newCity -> nova cidade que será adicionada (Objeto City)
        """
        self.cities.append(newCity)
        self.number_of_cities += 1

    def get_cities(self):
        """
            Captura todas as cidades do mapa.

            Retorno:
                -Lista de cidades do mapa (list)
        """
        return self.cities

    def get_number_of_cities(self):
        """
            Captura o número de cidades do mapa.

            Retorno:
                -Número de cidades do mapa (int)
        """
        return self.number_of_cities

    def get_city_by_name(self, name):
        """
            Pesquisa por uma cidade no mapa pelo seu nome.

            Parâmetros:
                - Nome da cidade procurada

            Retorno:
                -Uma cidade, caso seja encontrada (Objeto City)
                -None, caso a cidade não exista no mapa (None)
        """
        for city in self.cities:
            if city.get_name() == name:
                return city
        return None

    def get_map_list_of_routes(self):
        """
            Captura a lista de caminhos possíveis com as cidades do mapa.

            Retorno:
                - Lista com todos os caminhos possíveis com as cidades do mapa (list)
        """
        routes = list()
        for city in self.cities:
            for i in range(len(self.cities)):
                if not self.cities[i] == city:
                    finded_routes = self.init_dfs(city.get_name(), self.cities[i].get_name())
                    if finded_routes:
                        routes.extend(finded_routes)
        return routes

    def convert_to_string(self, company_name):
        """
            Converte o mapa em string de acordo com o padrão estabelecido pelo grupo

            Parâmetros:
                company_name -> nome da companhia para filtrar o mapa
            
            Retorno:
                - string com todas as rotas do mapa (string)
        """
        string_map = ''
        for city in self.cities:
            for route in city.get_routes():
                if route.get_company() == company_name:
                    string_map += f'{route.get_origin().get_name()},{route.get_destination().get_name()},{route.get_price()},{route.get_entries()},{route.get_company()}\n'
        return string_map

    def init_dfs(self, origin, destination):
        """
            Algoritmo Depth-First Search (DFS), conhecido por busca em profundidade usado para
            pesquisar caminhos no grafo

            Parâmetros:
                origin -> cidade origem do caminho buscado
                destination -> cidade destino do caminho buscado
            
            Retorno:
                - Uma lista com listas de rotas (caminhos) possíveis entre 'origin' e 'destination' (list)
        """
        visited = list()
        routes = list()
        route = list()
        self.dfs(visited, self.get_city_by_name(origin), self.get_city_by_name(destination), routes, route)
         
        return routes

    def dfs(self, visited, node, destination, routes, route):
        """
            Função para executar a recursão do Depth-First Search DFS, que é iniciada na função
            anterior: init_dfs(...)

            Parâmetros:
                visited -> lista de cidades visitadas (list)
                node -> cidade que está sendo visitada (objeto City)
                destination -> cidade destino (objeto City)
                routes -> lista com as listas de rotas (caminhos) já encontrados (list)
                route -> lista de rotas (caminho) que está sendo pesquisado no momento. (list)
        """
        if node not in visited:
            if node == destination:
                routes.append(route.copy()) 
                return 
            visited.append(node)
            for neighbour in node.get_routes():
                if neighbour.get_entries() > 0:
                    route.append(neighbour)
                    self.dfs(visited, neighbour.get_destination(), destination, routes, route)
                    route.pop()

            visited.pop()