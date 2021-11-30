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