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
        number_of_paths = self.get_number_of_cities() * 2
        paths = list()
        companies = [Company("A"), Company("B"), Company("C")]


        while number_of_paths > 0: #each iteration it's a path
            number_of_routes = random.randint(0, self.get_number_of_cities())
            routes = list()
            index_cities = self.index_cities_generator(number_of_routes+1)
            i = 0
            for index in index_cities:
                selected_company = random.randint(0, len(companies)-1)
                if(i != number_of_routes): #indicate that is the last city of path
                    routes.append(Route(City(names_of_cities[index]), City(names_of_cities[index_cities[index + 1]]), random.randint(10, 100), 10, companies[selected_company]))        
                i += 1
            paths.append(Path(routes))
            number_of_paths = number_of_paths - 1

    def index_cities_generator(self, n):
        index_cities = random.sample(range(0, self.get_number_of_cities()), n)
        return index_cities

mapa = Map()
mapa.get_routing()


#c1 = City("c1")
#c2 = City("c2")
#company = Company("company")
#r1 = Route(c1,c2,50,10,company)
#print(c1.get_routes()[0].get_origin().get_name())