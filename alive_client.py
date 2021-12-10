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
                
            time.sleep(3)