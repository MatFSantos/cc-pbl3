from company_server import CompanyServer
from model.route import Route
from model.city import City
from model.map import Map
from api import Api_Flask
import time
from copy import deepcopy

names_of_cities = ('Salvador', 'Maceió', 'Aracaju', 'Recife', 'São Luís', 'João Pessoa', 'Natal', 'Porto Seguro', 'Caruaru', 'Barreiras')

isCoordinator = False

class Company:

    def __init__(self):
        self.name = input("Informe a companhia: ")
        self.company_map = Map()
        self.full_map = Map()
        self.get_routing_company(self.name)    
        self.company_server = CompanyServer(self)
        self.company_server.start()
        Api_Flask(self.company_server).start()  
        self.isCoordinator = False

    def get_name(self):
        return self.name

    def get_company_map(self):
        return self.company_map
    
    def get_full_map(self):
        return self.full_map

    def get_is_coordinator(self):
        return self.isCoordinator

    def get_routes_for_api(self, origin, destination):
        routes = self.full_map.init_dfs(origin, destination)
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
                    'origem':route[0].get_origin().get_name(), 
                    'desination': route[-1].get_destination().get_name(),
                    'price': price
                }
            )

        # for city in self.full_map.get_cities():
        #     print("cidade: ", city.get_name())
        #     for route in city.get_routes():
        #         print("rota:")
        #         print("origin: ", route.get_origin().get_name())
        #         print("destination: ", route.get_destination().get_name())
        #         print("company: ", route.get_company())

        return paths_in_dict
                

    def get_routing_company(self, name):    
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
        self.full_map = full_map

    def set_coordinator(self, isCoordinator):
        self.isCoordinator = isCoordinator
company = Company()