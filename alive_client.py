from threading import Thread
import time

class AliveClient(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)
        self.company_server = company_server

    def run(self):
        while True:
            self.company_server.verify_alive_companies()
            if not self.company_server.get_alive_equal():
                self.company_server.set_alive_equal()
                self.company_server.get_full_map()
                if self.company_server.company.get_is_coordinator():
                    # self.company_server.init_election()
                    print("Coordenador é: ", self.company_server.get_atual_coordinator())
                else:
                    flag_coordinator_dead = False
                    for alives in self.company_server.get_alives():
                        if self.company_server.get_atual_coordinator() in alives.keys():
                            if not alives[self.company_server.get_atual_coordinator()]:
                                flag_coordinator_dead = True
                                break
                    if flag_coordinator_dead:
                        
                        if self.company_server.get_atual_coordinator() == 'A':
                            prox_coordinator = 'B'
                        elif self.company_server.get_atual_coordinator() == 'B':
                            prox_coordinator = 'C'
                        else:
                            prox_coordinator = 'A'
                        self.company_server.set_atual_coordinator(prox_coordinator)
                        if self.company_server.get_name() == prox_coordinator:
                            self.company_server.get_company().set_coordinator(True)
                        else:
                            i = 0
                            flag_have_alive = False
                            for company_attr in self.company_server.get_company_addr():
                                if self.company_server.get_alives()[i][company_attr['company']]:
                                    flag_have_alive = True
                                    break
                                i += 1
                            if not flag_have_alive:
                                self.company_server.get_company().set_coordinator(True)
                                self.company_server.set_atual_coordinator(self.company_server.get_name())
            time.sleep(3)