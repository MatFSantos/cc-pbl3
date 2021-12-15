from threading import Thread
import socket
import time

class AliveClient(Thread):
    """
        Classe de cliente socket que faz o papel de executar a conexão com as demais companhias (e seus servidores AliveServer)
        e verificar se houve alguma mudança em seu status de conexão.

        A classe verifica essa mudança e executa alguma ação de acordo com a mudança ocorrida

        -> nova conexão: é feito uma nova eleição de coordenador e o mapa geral das companhias é reestabelecido
        -> desconexão do coordenador: é feito uma nova eleição e o mapa geral das companhias é reestabelecido
        -> desconexão de um não-coordenador: apenas o mapa geral das companhias é reestabelecido

        Atributos:
            company_server -> servidor da companhias à qual o cliente socket está vinculado
            counter_to_election -> contador que avisa quando é a hora de fazer uma nova eleição (para o coordenador, apenas)
    """

    def __init__(self, company_server):
        """
            Instancia um objeto AliveClient e inicializa seus atributos
        """
        Thread.__init__(self)
        self.company_server = company_server
        self.counter_to_election = 0

    def run(self):
        """
            Método que é executado quando a Thread é inicializada
            
            Esse método fica em loop infinito fazendo sempre a verificação de status das companhias conhecidas e toma
            alguma decisão de acordo com esse status.
        """
        ## Esse trecho executa uma única vez que é quando a companhia é iniciada.
        # É verificado se tem mais alguma companhia conectada e o mapa geral é estabelecido, independente de ter 
        # alguma outra companhia conectada ou não. Se existem outras companhias conectadas além dessa, o método
        # init_already_alives() é executado
        result = self.company_server.verify_alive_companies()
        self.company_server.get_full_map()
        if not result:
            self.init_already_alives()
        
        ## Fica em loop sempre verificando o status
        while True:
            result = self.company_server.verify_alive_companies() ## verifica o status
            if self.company_server.get_atual_coordinator() == self.company_server.get_name():
                ## Se a companhia for a coordenadora, ela soma o contador da eleição até o máximo.
                ## No máximo é feita a eleição de um novo coordenador.
                if self.counter_to_election == 5:
                    self.election(True)
                else:
                    self.counter_to_election += 1
            if result:
                ## Caso o status tenha mudado o mapa geral é reestabelecido e é verificado o que aconteceu
                self.company_server.get_full_map()
                if self.company_server.get_atual_coordinator() in result.keys():
                    ## Se o que aconteceu foi a desconexão do coordenador, a eleição é chamada
                    self.election(False)
                else:
                    ## Caso não tenha sido a desconexão do coordenador, é verificado se foi uma nova conexão
                    keys = result.keys()
                    conected = False
                    for key in keys:
                        if result[key]:
                            conected = True
                            break
             
                    if conected & (self.company_server.get_atual_coordinator() == self.company_server.get_name()):
                        ## se foi uma nova conexão, a eleição feita pelo coordenador
                        self.election(True)
            ## um timer de 1 segundo
            time.sleep(1)
            print("O atual coodenador é: ", self.company_server.get_atual_coordinator())
            print(self.company_server.get_company().get_is_coordinator())

    def init_already_alives(self):
        """
            Método utilizado para eleger uma companhia como coordenadora quando
            não tem mais nenhuma outra companhia conectada
        """
        flag = False
        ## Verifica se tem alguem 'vivo'
        for company in self.company_server.get_alives():
            key = list(company)[0]
            if company[key]:
                flag = True
                break
        
        ## se não tiver elege ela própria
        if not flag:
            self.company_server.set_atual_coordinator(self.company_server.get_name())

    def election(self, normal):
        """
            Método que realiza a eleição de um novo coordenador em tempo de execução.

            Parâmetros:
                normal -> booleano que indica se a eleição é normal ou não
                    eleição normal(true): quando o contador chega ao limite ou quando alguma nova companhia se conecta
                        (SEMPRE FEITA PELO COORDENADOR)
                    eleição não-normal(false): quando o coordenador desconectado (FEITA EM CONSENSO GERAL)
        """
        print("Fazendo eleição")

        ##captura os contadores de requisições das outras companhias
        counts_request = self.company_server.get_counts_request()
        if not normal:
            ## se o coordenador foi  desconectado, a companhia atual também é candidata, então também pega o contador
            ## de requisições dela mesma.
            counts_request[self.company_server.get_name()] = self.company_server.company.get_count_request()

        ## verifica se tem alguma companhia que é canditada, se não tiver a própria companhia se elege
        ## se tiver, é escolhido a companhia com maior contador de requisições ou a primeira em ordem alfabética, caso
        ## tenham o mesmo contador de requisições
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
        """
            Método que notifica o novo coordenador, se a atual companhia não for, e as demais companhias que um novo
            coordenador foi eleito

            Parâmetros:
                new_coordinator -> nome do novo coordenador
        """
        i = 0
        for company_attr in self.company_server.get_company_addr():
            notify_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.company_server.get_alives()[i][company_attr['company']]:
                notify_socket.connect(company_attr['addr'])
                notify_socket.send(bytes("new coordinator", 'utf-8'))
                notify_socket.recv(1024).decode()
                notify_socket.send(bytes(new_coordinator, 'utf-8'))
                notify_socket.close()
            i += 1