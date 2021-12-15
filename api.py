from flask import Flask, json, jsonify, request
from threading import Thread
import time
from flask_cors import CORS, cross_origin

class Api_Flask(Thread):
    """
        Classe da API que disponibiliza as rotas para comunicação com a interface

        Atributos:
            company_server -> o servidor da companhia a qual a API está vinculada
            company_name -> nome da companhia a qual a API está vinculada
            count_request -> contador de requisições
    """

    def __init__(self, company_server):
        """
            Instancia um objeto Api_Flask e inicializa seus atributos.
        """
        Thread.__init__(self)  
        self.company_server = company_server
        self.company_name = self.company_server.get_name()
        self.count_request = 0

    def run(self):
        """
            Método que é executado quando a Thread inicia sua execução.

            Esse método conta com a incialização da API FLASK e da definição de suas rotas
        """
        app = Flask(__name__)

        app.debug = False
        app.use_reloader = False
        CORS(app, support_credentials=True)
        
        @app.route(f'/{self.company_name}/routes', methods=['GET'])
        @cross_origin(supports_credentials=True)
        def get_company_routes(supports_credentials=True):
            """
                Rota que faz o cálculo de todos os caminhos possíveis da companhia (apenas da companhia),
                independente de origem e destido

                Retorno:
                    - Um JSON com um lista de dicionários no padrão:
                        [
                            {
                                origin: '',
                                destination: '',
                                path: [{},...,{}],
                                price: '',
                            },
                        ]
            """
            paths = self.company_server.get_company().get_company_routes_for_api()
            return jsonify(paths)
            
        @app.route(f'/{self.company_name}/<string:origin>/<string:destination>')
        @cross_origin(supports_credentials=True)
        def get_travel_paths(origin, destination, supports_credentials=True):
            """
                Rota que faz o cálculo de todos os caminhos possíveis levando em conta o mapa total, com integração das outras
                companhias, com origem e destino.

                Parâmetros:
                    origin -> nome da cidade origem do caminho
                    destination -> nome da cidade destino do camino

                Retorno:
                    - Um JSON com um lista de dicionários no padrão:
                        [
                            {
                                origin: '',
                                destination: '',
                                path: [{},...,{}],
                                price: '',
                            },
                        ]
            """
            paths = self.company_server.get_company().get_all_routes_for_api(origin, destination)
            return jsonify(paths)

        @app.route(f'/{self.company_name}/buy', methods=['POST'])
        @cross_origin(supports_credentials=True)
        def buy_travel(supports_credentials=True):
            """
                Rota que faz a compra, se possível, da passagem do caminho selecionado.

                Parâmetros:
                    resquest -> um dicionário contendo o caminho, no formato:
                        {
                            origin: '',
                            destination: '',
                            path: [{},...,{}],
                            price: '',
                        }
                
                Retorno:
                    - status 200 e uma mensagem avisando que foi possível comprar
                    - status 400 e uma mensagem avisando que não foi possível comprar
            """
            self.count_request += 1
            while not self.company_server.company.get_is_coordinator():
                time.sleep(1)
            paths = request.get_json()["path"]
            for path in paths:
                verify = False
                if path['company'] == self.company_name:
                    verify = self.company_server.buy_entry_route(path)
                else:
                    verify = self.company_server.buy_entry_route_other_company(path)
                
                if not verify:
                    self.count_request -= 1
                    return jsonify({'message': "Não foi possível comprar a rota"}), 400
            self.count_request -= 1
            return jsonify({'message': "A compra foi efetuada"}, 200)
        
        ## aqui é a decisão de qual porta a API irá iniciar para não dá conflito
        port = ''
        if self.company_name == 'A':
            port = '52000'
        elif self.company_name == 'B':
            port = '53000'
        else:
            port = '54000'
            
        app.run(host='0.0.0.0', port=port)