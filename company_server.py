import socket
import time
import copy
import string
import random

import json
from alive_server import AliveServer
from alive_client import AliveClient
from model.city import City
from model.map import Map
from threading import Thread

host = ('127.0.0.1', 50000) #sevidor de broadcast


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
        
        # companies, coordinator = self.get_companies()
        companies = self.get_companies()
        
        # if coordinator == self.name:
        #     self.company.set_coordinator(True)
        # else:
        #     self.company.set_coordinator(False)

        self.atual_coordinator = ''
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

        alive_server = AliveServer((self.addr[0], self.addr[1]+3000)) #para verificar
        alive_server.start()
        
        self.company_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.company_server.bind(self.addr)
        self.company_server.listen(5)

    def run(self):   
        alive_client = AliveClient(self)
        alive_client.start()
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
            if msg == "count_request":
                conn.send(bytes(str(self.company.get_count_request()),'utf-8'))
                print("Contador de requisições enviado a companhia: ", cliente)
            if msg == "new coordinator":
                conn.send(bytes('ok', 'utf-8'))
                self.set_atual_coordinator(conn.recv(1024).decode())
            conn.close()

    def get_counts_request(self):
        i = 0
        counts_request = {}
        for company_attr in self.company_addr:
            request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.alive_companies[i][company_attr['company']]:
                request_socket.connect(company_attr['addr'])
                request_socket.send(bytes("count_request", 'utf-8'))
                counts_request[company_attr['company']] = int(request_socket.recv(1024).decode())
            i += 1

        return counts_request

    def verify_alive_companies(self):            
        i = 0
        change = {}
        for company_attr in self.company_addr:
            alive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            flag = self.alive_companies[i][company_attr['company']]
            try:
                alive_socket.connect(company_attr['addr_alive_server']) 
                alive_socket.close()
                self.alive_companies[i][company_attr['company']] = True
                print("Companhia", company_attr['company'], "está ativa.")
                       
            except Exception as ex:
                print("Companhia", company_attr['company'], "não está ativa.")
                self.alive_companies[i][company_attr['company']] = False
            finally:
                if flag != self.alive_companies[i][company_attr['company']]:
                    change[company_attr['company']] = self.alive_companies[i][company_attr['company']]
                i += 1
        
        return change

    def get_companies(self):
        broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast.connect(host)
        broadcast.send(bytes(self.name, 'utf-8'))
        companies = broadcast.recv(1024).decode()
        companies = companies.split(';')
        company1 = companies[0].split(',')
        company2 = companies[1].split(',')
        coordinator = companies[-1]
        return [{'ip': company1[0], 'port': company1[1], 'company':  company1[2]}, {'ip': company2[0], 'port': company2[1], 'company':  company2[2]}]

    def get_full_map(self):
        string_map = ''
        i = 0
        for company_attr in self.company_addr:
            full_map_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.alive_companies[i][company_attr['company']]:
                full_map_socket.connect(company_attr['addr'])
                full_map_socket.send(bytes("map", 'utf-8'))
                string_map += full_map_socket.recv(1024).decode()
                print("mapa requisitado à Companhia: ", company_attr['company'])
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
            return(bool(resp))

    def init_election(self):
        choice = random.choice(string.ascii_uppercase[0:3])
        # while self.atual_coordinator == choice:
        #     choice = random.choice(string.ascii_uppercase[0:3])
       
        # for company in self.alive_companies:
        #     if choice in company.keys():
        #         if company[choice]:
        #             self.atual_coordinator = choice
        #             self.company.set_coordinator(False)
        #             i = 0
        #             for company_attr in self.company_addr:      
        #                 if self.alive_companies[i]
        #                 election_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #                 election_socket.connect(self.company_addr[i]['addr'])
        #                 election_socket.send(bytes("newCoordinator", 'utf-8'))

        #                 i += 1
            # if self.alive_companies[i][company_attr['company']]:
            #     print("Requisitando o mapa da Companhia: ", company_attr['company'])
            #     full_map_socket.connect(company_attr['addr'])
            #     full_map_socket.send(bytes("map", 'utf-8'))
            #     string_map += full_map_socket.recv(1024).decode()
            # else:
            #     print("Companhia: ", company_attr['company'], "inativa.")
            # i += 1
    # def election_is_running(self):
    #     i = 0
    #     for company_attr in self.company_addr:
    #         election_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         if self.alive_companies[i][company_attr['company']]:
    #             election_socket.connect(company_attr['addr'])
    #             election_socket.send(bytes("election", 'utf-8'))
    #             if bool(election_socket.recv(1024).decode()):
    #                 election_socket.close()
    #                 return True      
                
    #         i += 1


    def get_priority_queue():
        priority_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        priority_socket.connect(host)
        priority_socket.send(bytes("queue", 'utf-8'))
        priority_queue = priority_socket.recv(1024).decode()

        priority_socket.close()
        return priority_queue.split(',')

    def get_alives(self):
        return self.alive_companies

    def get_company_addr(self):
        return self.company_addr

    def get_atual_coordinator(self):
        return self.atual_coordinator
    
    def get_company(self):
        return self.company

    def get_name(self):
        return self.name
        
    def set_atual_coordinator(self, coordinator):
        self.atual_coordinator = coordinator
        if self.atual_coordinator == self.name:
            self.company.set_coordinator(True)
        else:
            self.company.set_coordinator(False)
        print("atual coordenador é: ", self.atual_coordinator)
