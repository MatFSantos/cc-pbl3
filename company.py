from company_server import CompanyServer
from model.route import Route
from model.city import City
from model.map import Map
from api import Api_Flask

names_of_cities = ('Salvador', 'Maceió', 'Aracaju', 'Recife', 'São Luís', 'João Pessoa', 'Natal', 'Porto Seguro', 'Caruaru', 'Barreiras')

isCoordinator = False

class Company:

    def __init__(self):
        self.name = input("Informe a companhia: ")
        self.company_map = Map()
        self.full_map = Map()
        self.get_routing_company(self.name)    
        CompanyServer(self).start()
        #Api_Flask(self).start()  
        

    def get_name(self):
        return self.name

    def get_company_map(self):
        return self.company_map
    
    def get_full_map(self):
        return self.full_map

    def set_full_map(self, full_map):
        self.full_map = full_map

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

            Route(origin, destination,attr[2],attr[3], attr[4]) #instancio a nova rota.

        print(len(self.company_map.get_cities()))
        for city in self.company_map.get_cities(): #para teste
            if len(city.get_routes()) > 0:
                print('nome cidade: ',city.name)
                print(' rotas:')
                i = 0
                for route in city.routes:
                    print(f'    Rota {i}: ')
                    print("         nome origem: ",route.origin.name)
                    print("         nome destino: ", route.destination.name)
                    print("         preço: ", route.price)
                    print("         assentos: ", route.entries)
                    print("         companhia: ", route.company)
                    i +=1


    def get_routing_full(self, string_map):

        for city in self.company_map.get_cities:
            self.full_map.add_city(city)

        lines = string_map.split('\n')
        for line in lines:
            if line != '':
                attr = line.split(',') # dou split nos atributos da rota
                origin = None
                destination = None
                for city_company in  self.company_map.get_cities():
                    if city_company.get_name() == attr[0]:
                        origin = self.full_map.get_city_by_name(attr[0])
                    if city_company.get_name() == attr[1]:
                        destination = self.full_map.get_city_by_name(attr[1])
                if not origin:
                    origin = City(attr[0])
                    self.full_map.add_city(origin)
                if not destination:
                    destination = City(attr[1])
                    self.full_map.add_city(destination)

            Route(origin, destination,attr[2],attr[3], attr[4]) #instancio a nova rota.

        print(len(self.full_map.get_cities()))
        for city in self.full_map.get_cities(): #para teste
            if len(city.get_routes()) > 0:
                print('nome cidade: ',city.name)
                print(' rotas:')
                i = 0
                for route in city.routes:
                    print(f'    Rota {i}: ')
                    print("         nome origem: ",route.origin.name)
                    print("         nome destino: ", route.destination.name)
                    print("         preço: ", route.price)
                    print("         assentos: ", route.entries)
                    print("         companhia: ", route.company)
                    i +=1

company = Company()