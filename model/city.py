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

    def compare_route(self, destination, price, company):
        flag = False
        for route in self.routes:
            if route.get_destination().get_name() == destination.get_name():
                if route.get_price() == price:
                    if route.get_company() == company:
                        flag = True
                    else:
                        flag = False
                else:
                    flag = False        
            else:
                flag = False           
            if flag:
                return flag
        return False
        
