import socket
import time
import copy

import json
from alive_server import AliveServer
from alive_client import AliveClient
from model.city import City
from model.map import Map
from threading import Thread

host = ('26.90.73.25', 50000) #sevidor de broadcast


class CompanyServer(Thread):

    def __init__(self, company):
        Thread.__init__(self)
        self.company = company
        self.name = company.get_name()
        self.election_running = False
    
        if self.name == "A":
            self.addr = ('26.90.73.25', 55000)
        elif self.name == "B": 
            self.addr = ('26.90.73.25', 56000)
        else:
            self.addr = ('26.90.73.25', 57000)   
        
        companies = self.get_companies()  
        self.company_addr = []
        self.alive_companies = []
        for company_attr in companies:
            self.company_addr.append(
                {
                    'company': company_attr['company'], 
                    'addr': (company_attr['ip'], int(company_attr['port'])), 
                    'addr_alive_server': (company_attr['ip'], (int(company_attr['port']))+3000) 
                }
            )

        for company_attr in self.company_addr:
            self.alive_companies.append({company_attr['company']: False})

        self.alive_equal = False #para verificar se ouve alguma alteração em uma companhia
        AliveServer((self.addr[0], self.addr[1]+3000)).start() #para verificar

        self.company_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.company_server.bind(self.addr)
        self.company_server.listen(5)

    def run(self):   
        AliveClient(self).start()
        while True:
            response = ''
            conn, cliente = self.company_server.accept()
            print("Conectado pelo cliente: ", cliente)
            msg = conn.recv(1024).decode()
            if msg == "map":
                response = self.company.get_company_map().convert_to_string(self.company.get_name())
                conn.send(bytes(response, 'utf-8'))
                print("Mapa enviado para a companhia: ", cliente)
            if msg == "buy":
                conn.send(bytes("ok", 'utf-8'))
                path = json.loads(conn.recv(1024).decode())
                if self.buy_entry_route(path):
                    conn.send(bytes('ok', 'utf-8'))
                else:
                    conn.send(bytes('', 'utf-8'))

            conn.close()

    def verify_alive_companies(self): 
            
        i = 0
        for company_attr in self.company_addr:
            alive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            flag = self.alive_companies[i][company_attr['company']]      
            try:
                print("Tentativa de conexão com a Companhia: ", company_attr['company'])
                alive_socket.connect(company_attr['addr_alive_server']) 
                alive_socket.close()
                self.alive_companies[i][company_attr['company']] = True
                print("Companhia", company_attr['company'], "está ativa.")
                       
            except Exception as ex:
                print("Companhia", company_attr['company'], "não está ativa.")
                self.alive_companies[i][company_attr['company']] = False

            finally:
                if flag != self.alive_companies[i][company_attr['company']]:
                    self.alive_equal = False
                i += 1
            

    def get_companies(self):
        broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast.connect(host)
        broadcast.send(bytes(self.name, 'utf-8'))
        companies = broadcast.recv(1024).decode()
        companies = companies.split(';')
        company1 = companies[0].split(',')
        company2 = companies[1].split(',')
        return [{'ip': company1[0], 'port': company1[1], 'company':  company1[2]}, {'ip': company2[0], 'port': company2[1], 'company':  company2[2]}]

    def get_full_map(self):
        string_map = ''
        
        i = 0
        for company_attr in self.company_addr:
            full_map_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.alive_companies[i][company_attr['company']]:
                print("Requisitando o mapa da Companhia: ", company_attr['company'])
                full_map_socket.connect(company_attr['addr'])
                full_map_socket.send(bytes("map", 'utf-8'))
                string_map += full_map_socket.recv(1024).decode()
            else:
                print("Companhia: ", company_attr['company'], "inativa.")
            i += 1

        if string_map != '':
            self.company.get_routing_full(string_map)
            print("Full map reestabelecido")
        else:
            print("Companhias inativas, mapa alterado somente para esta companhia.")
            full_map = self.company.get_company_map()
            self.company.set_full_map(full_map)

    def buy_entry_route(self, path):
        origin = self.company.get_full_map().get_city_by_name(path['origin'])
        route = origin.compare_route(path['destination'], int(path['price']), path['company'])
        return route.passanger_buy()

    def buy_entry_route_other_company(self, path):
        buy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        company_addr = None
        for company_attr in self.company_addr:
            if company_attr['company'] == path['company']:
                company_addr = company_attr['addr']
                break
        if company_addr:
            buy_socket.connect(company_addr)
            buy_socket.send(bytes("buy", 'utf-8'))
            resp = buy_socket.recv(1024).decode()
            buy_socket.send(bytes(json.dumps(path), 'utf-8'))
            resp = buy_socket.recv(1024).decode()
            buy_socket.close()

    def get_alive_equal(self):
        return self.alive_equal

    def set_alive_equal(self):
        self.alive_equal = True

    def get_company(self):
        return self.company

    def get_name(self):
        return self.name

