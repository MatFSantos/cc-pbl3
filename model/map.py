
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

    def get_city_by_name(self, name):
        for city in self.cities:
            if city.get_name() == name:
                return city
        return None

    def get_map_list_of_routes(self):
        routes = list()
        for city in self.cities:
            for i in range(len(self.cities)):
                if not self.cities[i] == city:
                    finded_routes = self.init_dfs(city.get_name(), self.cities[i].get_name())
                    if finded_routes:
                        routes.extend(finded_routes)
        return routes

    def convert_to_string(self, company_name):
        string_map = ''
        for city in self.cities:
            for route in city.get_routes():
                if route.get_company() == company_name:
                    string_map += f'{route.get_origin().get_name()},{route.get_destination().get_name()},{route.get_price()},{route.get_entries()},{route.get_company()}\n'
        return string_map

    def init_dfs(self, origin, destination):
        visited = list()
        routes = list()
        route = list()
        self.dfs(visited, self.get_city_by_name(origin), self.get_city_by_name(destination), routes, route)
         
        return routes

    def dfs(self, visited, node, destination, routes, route):
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