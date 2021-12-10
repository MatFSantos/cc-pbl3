from threading import Thread
import time

class AliveClient(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)
        self.company_server = company_server

    def run(self):
        while True:
            result = self.company_server.verify_alive_companies()
            
            if not self.company_server.get_alive_equal():
                self.company_server.set_alive_equal()
                self.company_server.get_full_map()
                if result:
                    if not result[self.company_server.get_atual_coordinator()]:
                        print('coordenador desconectado')
                    else:
                        keys = result.keys()
                        conected = False
                        for key in keys:
                            if result[key]:
                                conected = True
                                break
                        if conected:
                            counts_request = self.company_server.get_counts_request()
                            counts_request[self.company_server.get_name()] = self.company_server.company.get_count_request()

                            keys = counts_request.keys()
                            bigger_company = ''
                            bigger_request = 0
                            for key in keys:
                                if result[key] > bigger_request:
                                    bigger_request = result[key]
                                    bigger_company = key
                            if bigger_company == self.company_server.get_name():
                                print('a')
                                #se torna novo coordenador e avisa aos demais.
                            else:
                                print('a')
                                #avisa ao dono do maior numero de requisições q ele deve ser o coordenador.



            time.sleep(3)