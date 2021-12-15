class Route: #trecho/edge
    """
        Classe da rota entre cidades, que tem o papel de aresta do grafo utilizado como mapa das companhias.

        Atributos:
            origin -> cidade origem da rota
            destination -> cidade destino da rota
            price -> preço da rota
            entries -> número de assentos que a rota possui
            company -> companhia que faz essa rota
    """
    
    def __init__(self, origin, destination, price, entries, company):
        """
            Instancia a classe Route, iniciando os seus atributos.
        """
        self.origin = origin #class City
        self.destination = destination #class City
        self.price = int(price)
        self.entries = int(entries)
        self.company = company #name Company
        self.origin.add_route(self) # a rota é automáticamente adicionada a cidade origem
    
    def get_origin(self):
        """
            Captura a cidade origem da rota.

            Retorno:
                - cidade origem da rota (objeto City)
        """
        return self.origin
    
    def get_destination(self):
        """
            Captura a cidade destino da rota.

            Retorno:
                - cidade destino da rota (objeto City)
        """
        return self.destination
        
    def get_price(self):
        """
            Captura o preço da rota.

            Retorno:
                - preço da rota (int)
        """
        return self.price

    def get_entries(self):
        """
            Captura o número de assentos da rota.

            Retorno:
                - número de assentos da rota (int)
        """
        return self.entries

    def get_company(self):
        """
            Captura a companhia que faz a rota.

            Retorno:
                - Companhia que oferece a rota (string)
        """
        return self.company

    def passanger_buy(self):
        """
            Faz a compra de uma passagem, subtraindo um ao número de assentos da rota

            Retorno:
                - True se foi possível subtrair (boolean)
                - False caso não tenha mais o que subtrair (boolean)
        """
        if self.has_entries():
            self.entries = self.entries - 1
            return True
        return False

    def has_entries(self):
        """
            Verifica se ainda possuem lugares vagos na rota

            Retorno:
                - True se existem lugares vagos na rota (assentos for maior que 0) (boolean)
                - False se não existem mais lugares vagos na rota (assentos for menor ou igual a 0) (boolean)
        """
        return (self.entries > 0)