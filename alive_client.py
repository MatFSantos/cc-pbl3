from threading import Thread
import socket
import time

class AliveClient(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)
        self.company_server = company_server
        self.counter_to_election = 0

    def run(self):
        result = self.company_server.verify_alive_companies()
        if not result:
            self.init_already_alives()
        while True:
            result = self.company_server.verify_alive_companies()
            if self.company_server.get_atual_coordinator() == self.company_server.get_name():
                if self.counter_to_election == 5:
                    self.election(True)
                else:
                    self.counter_to_election += 1
            if result:
                self.company_server.get_full_map()
                if self.company_server.get_atual_coordinator() in result.keys():
                    self.election(False)
                else:
                    keys = result.keys()
                    conected = False
                    for key in keys:
                        if result[key]:
                            conected = True
                            break
             
                    if conected & (self.company_server.get_atual_coordinator() == self.company_server.get_name()):
                        self.election(True)
            time.sleep(1)
            print("O atual coodenador é: ", self.company_server.get_atual_coordinator())
            print(self.company_server.get_company().get_is_coordinator())

    def init_already_alives(self):
        flag = False
        for company in self.company_server.get_alives():
            key = list(company)[0]
            if company[key]:
                flag = True
                break
        
        if not flag:
            self.company_server.set_atual_coordinator(self.company_server.get_name())

    def election(self, normal):
        print("Fazendo eleição")
        counts_request = self.company_server.get_counts_request()
        if not normal:
            counts_request[self.company_server.get_name()] = self.company_server.company.get_count_request()
        bigger_company = ''
        bigger_request = -1
        if counts_request:
            keys = counts_request.keys()       
            for key in keys:
                if counts_request[key] > bigger_request:
                    bigger_request = counts_request[key]
                    bigger_company = key
                elif counts_request[key] == bigger_request:
                    if key < bigger_company:
                        bigger_company = key
                        bigger_request = counts_request[key]


        else:
            bigger_company = self.company_server.get_name()
            
        if normal | (self.company_server.get_name() == bigger_company):
            self.company_server.set_atual_coordinator(bigger_company)
            self.notify_new_coordinator(bigger_company)
            self.counter_to_election = 0
  
    def notify_new_coordinator(self, new_coordinator):
        response = ''
        i = 0
        for company_attr in self.company_server.get_company_addr():
            notify_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.company_server.get_alives()[i][company_attr['company']]:
                notify_socket.connect(company_attr['addr'])
                notify_socket.send(bytes("new coordinator", 'utf-8'))
                response = notify_socket.recv(1024).decode()
                notify_socket.send(bytes(new_coordinator, 'utf-8'))
                notify_socket.close()
            i += 1