from threading import Thread
import time

class AliveClient(Thread):

    def __init__(self, company_server):
        Thread.__init__(self)
        self.company_server = company_server

    def run(self):
        while True:
            self.company_server.verify_alive_companies()        
            time.sleep(3)