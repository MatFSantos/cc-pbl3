from flask import Flask, json, jsonify, request
from threading import Thread
import time

class Api_Flask(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)  
        self.company_server = company_server
        self.company_name = self.company_server.get_name()
        self.count_request = 0

    def run(self):
        app = Flask(__name__)

        app.debug = False
        app.use_reloader = False

        @app.route(f'/{self.company_name}')
        def index():
            return jsonify({"A": self.company.name})

        @app.route(f'/{self.company_name}/routes', methods=['GET'])
        def get_company_routes():
            paths = self.company_server.get_company().get_company_routes_for_api()
            return jsonify(paths)
            
        @app.route(f'/{self.company_name}/<string:origin>/<string:destination>')
        def get_travel_paths(origin, destination):
            paths = self.company_server.get_company().get_routes_for_api(origin, destination)
            return jsonify(paths)

        @app.route(f'/{self.company_name}/buy', methods=['POST'])# 
        def buy_travel(): #rascunho
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
        
        port = ''
        if self.company_name == 'A':
            port = '52000'
        elif self.company_name == 'B':
            port = '53000'
        else:
            port = '54000'
            
        app.run(host='0.0.0.0', port=port)