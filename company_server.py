import socket
import time

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
        if self.name == "A":
            self.addr = ('26.90.73.25', 55000)
        elif self.name == "B": 
            self.addr = ('26.90.73.25', 56000)
        else:
            self.addr = ('26.90.73.25', 57000)   
        
        companies = self.get_companies()  
        self.company_addr = []
        self.active_companies = []
        for company_attr in companies:
            self.company_addr.append(
                {
                    'company': company_attr['company'], 
                    'addr': (company_attr['ip'], int(company_attr['port'])), 
                    'addr_alive_server': (company_attr['ip'], (int(company_attr['port']))+3000) 
                }
            )

        for company_attr in self.company_addr:
            self.active_companies.append({company_attr['company']: False})

        self.active_companies_copy = self.active_companies.copy() #para verificar se ouve alguma alteração em uma companhia
        AliveServer((self.addr[0], self.addr[1]+3000)).start() #para verificar

        self.company_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.company_server.bind(self.addr)
        self.company_server.listen(5)

    def run(self):    
        AliveClient(self).start()
        time.sleep(5)
        self.get_full_map()
        while True:
            response = ''
            conn, cliente = self.company_server.accept()
            print("Conectado pelo cliente: ", cliente)
            msg = conn.recv(1024).decode()
            if msg == "map":
                file = open(f"maps\company{self.name}.txt", mode='r', encoding='utf-8')
                response = file.read()
                conn.send(bytes(response, 'utf-8'))
                print("Mapa enviado para a companhia: ", cliente)

            # if self.active_companies != self.active_companies_copy:
        #         print("Houve uma mudança nas companhias ativas, reestabelecendo mapa de trechos...")
        #         self.get_full_map()
        #         print("Mapa restabelecido!")
        #         self.active_companies_copy = self.active_companies.copy()

            conn.close()
            
            

    def verify_alive_companies(self): 
            
        i = 0
        for company_attr in self.company_addr:
            alive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           
            try:
                print("Tentativa de conexão com a Companhia: ", company_attr['addr_alive_server'])
                alive_socket.connect(company_attr['addr_alive_server']) 
                print("conectou")
                alive_socket.close()
                self.active_companies[i][company_attr['company']] = True
                print("Companhia", company_attr['company'], "está ativa.")
                
            except Exception as ex:
                print("Companhia", company_attr['company'], "não está ativa.")
                self.active_companies[i][company_attr['company']] = False

            finally:
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
            if self.active_companies[i][company_attr['company']]:
                print("Requisitando o mapa da Companhia: ", company_attr['company'])
                full_map_socket.connect(company_attr['addr'])
                full_map_socket.send(bytes("map", 'utf-8'))
                string_map += full_map_socket.recv(1024).decode()
            else:
                print("Companhia: ", company_attr['company'], "inativa.")
            i += 1

        if string_map != '':
            self.company.get_routing_full(string_map)
        else:
            print("Full map estabelecido")
            full_map = self.company.get_company_map()
            self.company.set_full_map(full_map)

        #for city_company_map in company_map.get_cities():
        #    full_map.add_city(city_company_map)
