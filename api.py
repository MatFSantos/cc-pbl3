from flask import Flask, json, jsonify, request
from threading import Thread

class Api_Flask(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)  
        self.company_server = company_server
        self.company_name = self.company_server.get_name()

    def run(self):
        app = Flask(__name__)

        app.debug = False
        app.use_reloader = False

        @app.route(f'/{self.company_name}')
        def index():
            return jsonify({"A": self.company.name})

        @app.route(f'/{self.company_name}/<string:origin>/<string:destination>')
        def get_travel_paths(origin, destination):
            paths = self.company_server.get_company().get_routes_for_api(origin, destination)
            return jsonify(paths)

        @app.route(f'/{self.company_name}/buy', methods=['POST'])# 
        def buy_travel(): #rascunho
            paths = request.get_json()["path"]     
            for path in paths:
                verify = False
                if path['company'] == self.company_name:
                    verify = self.company_server.buy_entry_route(path)
                else:
                    verify = self.company_server.buy_entry_route_other_company(path)
                
                if not verify:
                    return jsonify({'message': "Não foi possível comprar a rota"}), 400

            return jsonify({'message': "A compra foi efetuada"}, 200)

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