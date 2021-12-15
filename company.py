from company_server import CompanyServer
from model.route import Route
from model.city import City
from model.map import Map
from api import Api_Flask

class Company:
    """
        Classe de companhia que possui os mapas e servidores.

        Atributos:
            name -> nome da companhia
            company_map -> mapa da companhia com as rotas que somente ela oferece
            full_map -> mapa em conjunto com outras companhias
            isCoordinator -> boleano que sinaliza caso a companhia seja o coordenador (algoritmo *bully*)
            company_server -> servidor da companhia que faz a comunicação com outras companhias
            api -> API que possui as rotas de comunicação com a interface
    """

    def __init__(self):
        """
            instancia um objeto Company e inicializa seus atributos.
        """
        self.name = input("Informe a companhia: ")
        self.company_map = Map()
        self.full_map = Map()
        self.get_routing_company(self.name) #carrega o mapa da companhia a partir do arquivo fornecido
        self.isCoordinator = False
        self.company_server = CompanyServer(self)
        self.api = Api_Flask(self.company_server)
        self.company_server.start() #inicia a thread do company_server
        self.api.start() #inicia a thread da API
    
    def get_count_request(self):
        """
            Captura o contador de requisições da API da companhia.

            Retorno:
                - A quantidade de requisições em espera de conclusão na API (int)
        """
        return int(self.api.count_request)

    def get_name(self):
        """
            Captura o nome da companhia

            Retorno:
                -Nome da companhia (string)
        """
        return self.name

    def get_company_map(self):
        """
            Captura o mapa da companhia (company_map).

            Retorno:
                -Mapa da companhia (Objeto Map)
        """
        return self.company_map
    
    def get_full_map(self):
        """
            Captura o mapa geral da companhia com as demais companhias conectadas à ela.

            Retorno:
                -Mapa geral com as companhias (Objeto Map)
        """
        return self.full_map

    def get_is_coordinator(self):
        """
            Verifica se ele é o coordenador (algoritmo *bully*)

            Retorno:
                - atributo da companhia que sinaliza se ela é a coordenadora atual ( boolean) 
        """
        return self.isCoordinator

    def get_all_routes_for_api(self, origin, destination):
        """
            Faz a caputra de todos os caminhos possíveis de uma cidade origem à uma cidade destino no mapa geral

            Parâmetros:
                origin -> nome da cidade origem (string)
                destination -> nome da cidade de destino (string)

            Retorno:
                - Uma lista com dicionários informando os caminhos encontrados já formatado para enviar em formato JSON (list)
        """
        routes = self.full_map.init_dfs(origin, destination)
        return self.get_list_of_routes(routes)

    def get_company_routes_for_api(self):
        """
            Faz a caputra de todos os caminhos possíveis com as rotas da companhia, ignorando as demais

            Retorno:
                - Uma lista com dicionários informando os caminhos encontrados já formatado para enviar em formato JSON (list)
        """
        routes = self.company_map.get_map_list_of_routes()
        routes_in_dict = []
        for route in routes:
            flag = False
            for path in route:
                if path.get_company() != self.name:
                    flag = True
                    break
            if not flag:
                routes_in_dict.append(route)
        routes_in_dict = self.get_list_of_routes(routes_in_dict)
        return routes_in_dict

    def get_list_of_routes(self, routes):
        """
            Transforma uma lista de caminhos (lista de listas de routes) em uma lista de dicionários

            Parâmetros:
                routes -> lista de caminhos que será formatada (list)
            
            Retorno:
                - Lista de caminhos em formato de dicionário já formatado para enviar em formato JSON (list)
        """
        paths_in_dict = []
        for route in routes:
            path_in_dict = []
            price = 0
            for path in route:
                price_path = int(path.get_price())
                price += price_path
                path_in_dict.append(
                    {
                        'origin': path.get_origin().get_name(), 
                        'destination': path.get_destination().get_name(), 
                        'price': price_path, 
                        'company': path.get_company()
                    }
                )
            paths_in_dict.append(
                {
                    'path': path_in_dict, 
                    'origin':route[0].get_origin().get_name(), 
                    'destination': route[-1].get_destination().get_name(),
                    'price': price
                }
            )

        return paths_in_dict

    def get_routing_company(self, name):
        """
            Faz a leitura do arquivo-mapa da companhia e carrega o mapa na companhia

            Parâmetros:
                name -> nome da companhia (string)
        """
        file = open(f"maps\company{name}.txt", mode='r', encoding='utf-8') #abro o file

        for line in file: # ler linha por linha do file
            if line != '':
                attr = line.split(',') # dou split nos atributos da rota
                origin = None
                destination = None
                for city in  self.company_map.get_cities():
                    if city.get_name() == attr[0]:
                        origin = self.company_map.get_city_by_name(attr[0])              
                    if city.get_name() == attr[1]:
                        destination = self.company_map.get_city_by_name(attr[1])
                if not origin:
                    origin = City(attr[0])
                    self.company_map.add_city(origin)
                if not destination:
                    destination = City(attr[1])
                    self.company_map.add_city(destination)
                Route(origin, destination,attr[2],attr[3], attr[4].replace("\n", "")) #instancio a nova rota.
        self.full_map = self.company_map
        print(f"Rotas da companhia {self.name} estabelecidas")

    def get_routing_full(self, string_map):
        """
            Concatena um novo mapa com o mapa existente na companhia e cria um novo mapa (full_map)

            Parâmetros:
                string_map -> mapa que será concatenado com o mapa da companhia (string)
        """
        self.full_map = Map()
        for city in self.company_map.get_cities():
            self.full_map.add_city(city)

        lines = string_map.split('\n')
        for line in lines:
            if line != '':
                attr = line.split(',') # dou split nos atributos da rota
                origin = None
                destination = None
                for city in  self.full_map.get_cities():
                    if city.get_name() == attr[0]:
                        origin = self.full_map.get_city_by_name(attr[0])
                    if city.get_name() == attr[1]:
                        destination = self.full_map.get_city_by_name(attr[1])
                if not origin:
                    origin = City(attr[0])
                    self.full_map.add_city(origin)
                if not destination:
                    destination = City(attr[1])
                    self.full_map.add_city(destination)
                if not origin.compare_route(destination.get_name(), int(attr[2]), attr[4]):
                    Route(origin, destination, attr[2], attr[3], attr[4].replace("\n", "")) #instancio a nova rota.  
    
    def set_full_map(self, full_map):
        """
            Altera o mapa conjunto das companhias (full map)
        """
        self.full_map = full_map

    def set_coordinator(self, newIsCoordinator):
        """
            Altera o sinalizador de coordenador (algoritmo *bully*)

            Parâmetros:
                newIsCoordinator -> novo valor para o sinalizador de coordenador (boolean)
        """
        self.isCoordinator = newIsCoordinator        
company = Company()