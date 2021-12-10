class Route: #trecho/edge
    
    def __init__(self, origin, destination, price, entries, company):
        self.origin = origin #class City
        self.destination = destination #class City
        self.price = price
        self.entries = entries
        self.company = company #name Company
        self.origin.add_route(self)
    
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