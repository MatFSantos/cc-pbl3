from flask import Flask, json, jsonify
from threading import Thread

from model.city import City
from model.route import Route
from model.map import Map

names_of_cities = ('Salvador', 'Maceió', 'Aracaju', 'Recife', 'São Luís', 'João Pessoa', 'Natal', 'Porto Seguro', 'Caruaru', 'Barreiras')
company_map = Map()
full_map = Map()

class Company:

    def __init__(self):
        self.name = input("Informe a companhia: ")
        self.get_routing(self.name)
        Api_Flask(self.name).start()

    def get_routing(self, name):    
        file = open(f"maps\company{name}.txt", mode='r', encoding='utf-8') #abro o file

        for line in file: # ler linha por linha do file
            attr = line.split(',') # dou split nos atributos da rota
            origin = None
            destination = None
            for city in  company_map.get_cities():
                if city.get_name() == attr[0]:
                    origin = company_map.get_city_by_name(attr[0])              
                if city.get_name() == attr[1]:
                    destination = company_map.get_city_by_name(attr[1])
            if not origin:
                origin = City(attr[0])
                company_map.add_city(origin) 
            if not destination:
                destination = City(attr[1])
                company_map.add_city(destination)

            Route(origin, destination,attr[2],attr[3], name) #instancio a nova rota.
        print(len(company_map.get_cities()))
        for city in company_map.get_cities(): #para teste
            if len(city.get_routes()) > 0:
                print('nome cidade: ',city.name)
                print(' rotas:')
                i = 0
                for route in city.routes:
                    print(f'    Rota {i}: ')
                    print("         nome origem: ",route.origin.name)
                    print("         nome destino: ", route.destination.name)
                    print("         preço: ", route.price)
                    print("         assentos: ", route.entries)
                    print("         companhia: ", route.company)
                    i +=1


class Api_Flask(Thread):

    def __init__(self, name):
        Thread.__init__(self)  
        self.company_name = name

    def run(self):
        app = Flask(__name__)

        app.debug = False
        app.use_reloader = False

        @app.route(f'/{self.company_name}')
        def index():
            return jsonify({"A": company.name})

        app.run()

company = Company()