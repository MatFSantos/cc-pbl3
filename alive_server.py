from threading import Thread
import socket

class AliveServer(Thread):
    """
        Classe de servidor socket que faz o papel de ficar ativo avisando aos outros que a companhia à qual pertence
        está ativa.

        Atributos:
            socket -> socket no qual fica ouvindo as outras companhias
    """

    def __init__(self, host):
        """
            Instancia um objeto AliveServer e inicializa seus atributos
        """
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(host)
        self.socket.listen(5)

    def run(self):
        """
            Método que é executado quando a Thread é inicializada
            
            Esse método fica em loop infinito com o socket ouvindo todas as requisições
        """
        while True:
            try:
                conn, client = self.socket.accept()
                conn.recv(1024).decode()
            except:
                pass
            conn.close()


        