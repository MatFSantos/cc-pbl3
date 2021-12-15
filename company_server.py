import socket
import json

from alive_server import AliveServer
from alive_client import AliveClient
from threading import Thread

host = ('26.183.229.122', 50000) #sevidor de broadcast

companyA = ('26.183.229.122', 55000) #ip de hospedagem da companhia A
companyB = ('26.90.73.25', 56000) #ip de hospedagem da companhia B
companyC = ('26.90.73.25', 57000) #ip de hospedagem da companhia C

class CompanyServer(Thread):
    """
        Classe que faz o papel do servidor da companhia que o instancia.

        Atributos:
            name -> Nome da companhia à qual o servidor pertence
            company -> Companhia à qual o servidor pertence
            addr -> Endereço 'IP:PORT' no qual a companhia ficará escutando requisições por socket
            atual_coordinator -> String que informa qual o atual coordenador
            company_addr -> Lista de dicionários que possuem a companhia, o endereço 'IP:PORT' em que ela escuta
                requisições por socket e o endereço 'IP:PORT' que o servidor usa para avisar que está 'vivo'.
            alive_companies -> Lista com sinalizadores que informam qual companhia está desativada e qual está ativa
            company_server -> Socket que é iniciado no endereço 'addr'.
    """

    def __init__(self, company):
        """
            Instancia um objeto CompanyServer e inicializa seus atributos.
        """
        Thread.__init__(self)
        print('inicio do init')
        self.company = company
        self.name = company.get_name()
        if self.name == "A":
            self.addr = companyA
        elif self.name == "B": 
            self.addr = companyB
        else:
            self.addr = companyC
        
        print('inicio da comunicação com broadcast')
        companies = self.get_companies()
        print('fim da comunicação com broadcast')

        self.atual_coordinator = ''

        #preenche o atributo company_addr
        self.company_addr = []        
        for company_attr in companies:
            self.company_addr.append(
                {
                    'company': company_attr['company'], 
                    'addr': (company_attr['ip'], int(company_attr['port'])), 
                    'addr_alive_server': (company_attr['ip'], (int(company_attr['port']))+3000)
                }
            )

        #preenche o atributo alive_companies
        self.alive_companies = []
        for company_attr in self.company_addr:
            self.alive_companies.append({company_attr['company']: False})

        #Thread utilizada para avisar que a companhia está viva para as demais companhias
        alive_server = AliveServer((self.addr[0], self.addr[1]+3000)) 
        alive_server.start()
        
        # dá "bind" no socket que ficará escutando requisições
        self.company_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.company_server.bind(self.addr)
        self.company_server.listen(5)

    def run(self):
        """
            Função que é executada quando a Thread do servidor é inicia.

            Essa função fica em loop infinito sempre escutando novas conexões no socket para resolver requisições que chegam.
        """
        # Inicia a Thread que fará a verificação se as demais estão vivas e também a eleição de um novo coordenador (algoritmo *bully*)
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
                if self.buy_entry_in_full_map(path):
                    conn.send(bytes('ok', 'utf-8'))
                else:
                    conn.send(bytes('', 'utf-8'))
            if msg == "count_request":
                conn.send(bytes(str(self.company.get_count_request()),'utf-8'))
                print("Contador de requisições enviado a companhia: ", cliente)
            if msg == "new coordinator":
                conn.send(bytes('ok', 'utf-8'))
                self.set_atual_coordinator(conn.recv(1024).decode())
            if msg == "decrement":
                conn.send(bytes('ok', 'utf-8'))
                path = json.loads(conn.recv(1024).decode())
                ## captura a cidade origem pelo nome
                origin = self.company.get_full_map().get_city_by_name(path['origin'])
                ## captura a rota pelo seus atributos
                route = origin.compare_route(path['destination'], int(path['price']), path['company'])
                if route:
                    if route.passanger_buy():
                        print("numero de acentos", route.get_entries())
                        conn.send(bytes('ok', 'utf-8'))
                    else:
                        conn.send(bytes('', 'utf-8'))
                else:
                    conn.send(bytes('', 'utf-8'))

            conn.close()

    def get_counts_request(self):
        """
            Captura os contadores de requisições das outras companhias.

            Retorno:
                - Dicionário com as companhias como chave e os valores sendo os seus contadores de requisições das APIs (dict)
        """
        i = 0
        counts_request = {}
        for company_attr in self.company_addr:
            request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            request_socket.settimeout(3)
            if self.alive_companies[i][company_attr['company']]:
                request_socket.connect(company_attr['addr'])
                request_socket.send(bytes("count_request", 'utf-8'))
                counts_request[company_attr['company']] = int(request_socket.recv(1024).decode())
            i += 1

        return counts_request

    def verify_alive_companies(self):
        """
            Verifica se as demais companhias conhecidas estão conectadas. Verifica também se ocorreu alguma mudança
            em relação à ultima verificação.

            Retorno:
                - Dicionário contendo como chave as companhias que mudaram sua situação em relação a ultima verificação
                e como valor o seu valor atual(True para conectado ou False para desconectado). (dict)

        """          
        i = 0
        change = {}
        for company_attr in self.company_addr:
            alive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alive_socket.settimeout(3)
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
        """
            Faz a comunicação com o servidor broadcast para saber quem são as companhias com as quais irá se comunicar

            Retorno:
                - Lista de dicionários em que se têm IP, porta e nome de uma companhia. (list)
        """
        broadcast = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast.connect(host)
        broadcast.send(bytes(self.name, 'utf-8'))
        companies = broadcast.recv(1024).decode()
        companies = companies.split(';')
        company1 = companies[0].split(',')
        company2 = companies[1].split(',')
        return [{'ip': company1[0], 'port': company1[1], 'company':  company1[2]}, {'ip': company2[0], 'port': company2[1], 'company':  company2[2]}]

    def get_full_map(self):
        """
            Faz a comunicação com as demais companhias para requisitas uma string com o mapa delas.
            Após receber essa string, o mapa é montado. Caso não receba nenhum mapa, o novo mapa geral será o mapa da
            própria companhia.
        """
        string_map = ''
        i = 0
        for company_attr in self.company_addr:
            full_map_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            full_map_socket.settimeout(3)
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
        """
            Compra uma passagem de uma rota que possue a essa companhia

            Parâmetros:
                path -> dicionário possuindo as características da rota que será comprada (dict)

            Retorno:
                -True, caso a compra seja bem sucedida (boolean)
                -False, caso não tenha sido possível comprar a passagem (boolean)
        """
        ## captura a cidade origem pelo nome
        origin = self.company.get_full_map().get_city_by_name(path['origin'])
        ## captura a rota pelo seus atributos
        route = origin.compare_route(path['destination'], int(path['price']), path['company'])
        ## faz a compra
        if route:
            if route.passanger_buy():
                print("numero de acentos", route.get_entries())
                i = 0
                for company_attr in self.company_addr:
                    socket_decrement = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_decrement.settimeout(3)
                    if self.alive_companies[i][company_attr['company']]:
                        socket_decrement.connect(company_attr['addr'])
                        socket_decrement.send(bytes("decrement", 'utf-8'))
                        socket_decrement.recv(1024)
                        socket_decrement.send(bytes(json.dumps(path), 'utf-8'))
                        response = bool(socket_decrement.recv(1024).decode())
                    i += 1
                return True
            else:
                return False
        else:
            return False
        

    def buy_entry_route_other_company(self, path):
        """
            Compra uma passagem de uma rota que possue a outras companhias.

            Parâmetros:
                path -> dicionário possuindo as características da rota que será comprada (dict)

            Retorno
                -True, caso a compra seja bem sucedida (boolean)
                -False, caso não tenha sido possível comprar a passagem (boolean)
        """
        buy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = None
        ## procura pelo endereço da companhia que possui a rota que será comprada
        for company_attr in self.company_addr:
            if company_attr['company'] == path['company']:
                address = company_attr['addr'] 
                break
        if address:
            ## se comunica com a companhia via socket e efetua a compra
            try:
                buy_socket.connect(address)
                buy_socket.send(bytes("buy", 'utf-8'))
                resp = buy_socket.recv(1024).decode()
                buy_socket.send(bytes(json.dumps(path), 'utf-8'))
                resp = buy_socket.recv(1024).decode()
                buy_socket.close()
                ## se foi possível fazer a compra, o número de acentos também é decrementado nessa companhia
                print('resp: ', resp)
                if bool(resp):
                    i = 0
                    for company_attr in self.company_addr:
                        socket_decrement = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socket_decrement.settimeout(3)
                        if self.alive_companies[i][company_attr['company']] & (address != company_attr['addr']):
                            socket_decrement.connect(company_attr['addr'])
                            socket_decrement.send(bytes("decrement", 'utf-8'))
                            socket_decrement.recv(1024)
                            socket_decrement.send(bytes(json.dumps(path), 'utf-8'))
                            response = bool(socket_decrement.recv(1024).decode())
                        i += 1
                    self.buy_entry_in_full_map(path)
                    return True
                else:
                    return False
            except:
                return False

    def buy_entry_in_full_map(self, path):
        """
            Decrementa no mapa compartilhado (full_map) os acentos que foram comprados com sucesso em outras
            companhias.

            Parâmetros:
                path -> dicionário possuindo as características da rota que será comprada (dict)
        """
        city = self.company.get_full_map().get_city_by_name(path['origin'])
        route = city.compare_route(path['destination'], path['price'], path['company'])
        if route:
            if route.passanger_buy():
                print("Numero de acentos: ", route.get_entries())
                return True
            else:
                return False
        return False

    def get_alives(self):
        """
            Captura a lista que informa a situação atual das companhias: ativas(true) ou inativas(false)

            Retorno:
                -Lista com dicionários que informam a situação atua das companhias (list)
        """
        return self.alive_companies

    def get_company_addr(self):
        """
            Captura a lista que informa os endereços das companhias conhecidas.

            Retorno:
                -Lista com dicionários que informam a companhia, o endereço do socket que responde requisições e o endereço do
                socket que avisa que a companhia está viva. (list)
        """
        return self.company_addr

    def get_atual_coordinator(self):
        """
            Captura qual o coordenador atual. (algoritmo *bully*)

            Retorno:
                -Nome do coordenador atual (string)
        """
        return self.atual_coordinator
    
    def get_company(self):
        """
            Captura a companhia à qual o servidor pertence.

            Retorno:
                -Companhia dona do servidor. (objeto Company)
        """
        return self.company

    def get_name(self):
        """
            Captura o nome da companhia dona do servidor.

            Retorno:
                -Nome da companhia do servidor. (string)
        """
        return self.name
        
    def set_atual_coordinator(self, coordinator):
        """
            Altera o atual coordenador.

            Parâmetros:
                - Nome do novo Coordenador (string)
        """
        self.atual_coordinator = coordinator
        if self.atual_coordinator == self.name:
            self.company.set_coordinator(True)
        else:
            self.company.set_coordinator(False)
        print("atual coordenador é: ", self.atual_coordinator)
