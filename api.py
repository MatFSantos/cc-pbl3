from flask import Flask, json, jsonify
from threading import Thread

class Api_Flask(Thread):

    def __init__(self, company):
        Thread.__init__(self)  
        self.company = company
        self.company_name = company.get_name()

    def run(self):
        app = Flask(__name__)

        app.debug = False
        app.use_reloader = False

        @app.route(f'/{self.company_name}')
        def index():
            return jsonify({"A": self.company.name})

        @app.route('/travel/<string:origin>/<string:destination>')
        def get_travel_paths(origin, destination):
            #pressupondo que ja temos todo o mapa
            paths = self.company.get_full_map().init_dfs(origin, destination)
            return jsonify({"origem": self.get_company_map().get_cities()[0].get_name(), "destino":destination})

        @app.route('/travel/buy/<string:path>')# path = cidade-cidade.companhia;cidade-cidade.companhia...
        def buy_travel(path): #rascunho
            print()
            # if isCoordinator:
            #     routes = path.split(";")
            #     for route in routes:
            #         splited_route =  route.split(".")
            #         cities = splited_route[0] #cidade-cidade
            #         company_route = splited_route[1] #companhia
            # else:
            #     return jsonify({"message": "Por favor, tente novamente."})


        @app.route('/teste')
        def teste():
            return jsonify({"conteudo": "isso é um teste, amigo"})
        
        port = ''
        if self.company_name == 'A':
            port = '52000'
        elif self.company_name == 'B':
            port = '53000'
        else:
            port = '54000'
            
        app.run(host='0.0.0.0', port=port)