from threading import Thread
import socket

class AliveServer(Thread):

    def __init__(self, host):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(host)
        self.socket.listen(5)

    def run(self):
        while True:
            try:
                conn, client = self.socket.accept()
                msg = conn.recv(1024).decode()
            except:
                pass
            conn.close()  


        