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