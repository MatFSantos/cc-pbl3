import random
names_of_cities = ('Salvador', 'Maceió', 'Aracaju', 'Recife', 'São Luís', 'João Pessoa', 'Natal', 'Porto Seguro', 'Caruaru', 'Barreiras')

class City: #vertex

    def __init__(self, name):
        self.name = name
        self.routes = list()

    def get_routes(self):
        return self.routes

    def get_name(self):
        return self.name

    def add_route(self, newRoute):#adding a route (already created)
        self.routes.append(newRoute)

class Route: #trecho/edge
    
    def __init__(self, origin, destination, price, entries, company):
        self.origin = origin #class City
        self.destination = destination #class City
        self.price = price
        self.entries = entries
        self.company = company #class Company
        self.origin.add_route(self)
        self.company.add_route(self)
    
    def get_origin(self):
        return self.origin
    
    def get_destination(self):
        return self.destination
    
    def get_price(self):
        return self.price

    def get_entries(self):
        return self.entries

    def get_company(self):
        return self.company

    def passanger_buy(self):
        if self.has_entries():
            self.entries = self.entries - 1
            return True
        return False

    def has_entries(self):
        return (self.entries > 0)

class Company:

    def __init__(self, name):
        self.name = name
        self.routes = list()

    def add_route(self, newRoute):#adding a route (already created)
        self.routes.append(newRoute)
    
    def get_routes(self):
        return self.routes

class Path: #trajeto/caminho

    def __init__(self, routes):
        self.routes = routes #routes => [route,route,route] in order. (newPath = Path([route1,route2,route3]))

    def get_routes(self):
        return self.routes
    def get_price(self):
        price = 0
        for route in self.routes:
            price += route.get_price()
        return price

class Map():

    def __init__(self):
        self.cities = list()
        self.number_of_cities = 0

    def add_city(self, newCity):
        self.cities.append(newCity)
        self.number_of_cities += 1

    def get_cities(self):
        return self.cities

    def get_number_of_cities(self):
        return self.number_of_cities

    def get_routing(self):    
        for city in names_of_cities:
            self.add_city(City(city))
        
        companies = {"A":Company("A"),"B": Company("B"),"C": Company("C")} # mudei para dicionário, pra facilitar
        this_company = input("Informe Compania: ") #capturo de qual compania é o mapa
        # file = open(f"backend\company{this_company}.txt", mode='r', encoding='utf-8') #abro o file
        file = open(f"backend\fullMap.txt", mode='r', encoding='utf-8')

        for line in file: # ler linha por linha do file
            attr = line.split(',') # dou split nos atributos da rota
            origin = None
            destination = None
            for city in self.cities: # procuro as cidades de origem e destino na lista de cidades do mapa
                if city.name == attr[0]:
                    origin = city
                elif city.name == attr[1]:
                    destination = city
            Route(origin, destination,attr[2],attr[3],companies[this_company]) #instancio a nova rota.
        
        for city in self.cities: #para teste
            if len(city.routes) > 0:
                print('nome cidade: ',city.name)
                print(' rotas:')
                i = 0
                for route in city.routes:
                    print(f'    Rota {i}: ')
                    print("         nome origem: ",route.origin.name)
                    print("         nome destino: ", route.destination.name)
                    print("         preço: ", route.price)
                    print("         assentos: ", route.entries)
                    print("         companhia: ", route.company.name)
                    i +=1


    def index_cities_generator(self, n):
        index_cities = random.sample(range(0, self.get_number_of_cities()), n)
        return index_cities

    def init_dfs(self, origin, destination):
        visited = list()
        path = list()
        paths = list()
        self.dfs(visited, path,paths, origin, destination)
        for caminho in paths:
            print("caminho:")
            for city in caminho:
                print(" ",city.get_name())


    def dfs(self, visited, path,paths, node, destination):
        if node not in visited:
            path.append(node)
            if node == destination:
                paths.append(path.copy())
                path.pop()
                return
            visited.append(node)
            for neighbour in node.get_routes():
                self.dfs(visited,path,paths, neighbour.get_destination(), destination)
                
            path.pop()
            visited.pop()



mapa = Map()
mapa.get_routing()
mapa.init_dfs(mapa.get_cities()[0], mapa.get_cities()[2])




#c1 = City("c1")
#c2 = City("c2")
#company = Company("company")
#r1 = Route(c1,c2,50,10,company)
#print(c1.get_routes()[0].get_origin().get_name())