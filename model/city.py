class City: #vertex
    """
        Classe cidade, que se comporta como os vértices do grafo utilizado
        como mapa.

        Atributos:
            name -> nome da cidade
            routes -> lista de rotas em que a cidade é origem
    """

    def __init__(self, name):
        """
            Instancia a classe City, dando seu nome e iniciando a lista de rotas (vázia).
        """
        self.name = name
        self.routes = list()

    def get_routes(self):
        """
            Retorna as rotas em que a cidade é origem.

            Retorno:
                lista com as rotas da cidade. (list)
        """
        return self.routes
        
    def get_name(self):
        """
            retorna o nome da cidade.
            
            Retorno:
                string com nome da cidade. (string)
        """
        return self.name
    
    def add_route(self, newRoute):
        """
            Adiciona uma nova roda à cidade.
        """
        self.routes.append(newRoute)

    def compare_route(self, destination, price, company):
        """
            Procura uma rota com as características passadas como parâmetro.

            Parâmetros:
                destination -> destino da rota procurada
                price -> preço da rota procurada
                company -> companhia da rota procurada
            Retorno:
                - uma rota, caso encontrada (objeto Route)
                - None, caso a rota não exista na cidade (None)
        """
        flag = None
        for route in self.routes:
            if route.get_destination().get_name() == destination:
                if route.get_price() == price:
                    if route.get_company() == company:
                        flag = route        
            if flag:
                return flag
        return None