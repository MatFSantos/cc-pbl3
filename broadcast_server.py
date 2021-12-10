import socket
   
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ('0.0.0.0', 50000)

company_A = '26.183.229.122,55000,A'
company_B = '26.183.229.122,56000,B'
company_C = '26.183.229.122,57000,C'

first_company = None

priority_queue = 'A,B,C'
#broadcast tem que enviar um ping as companhias de tempos em tempos para verificar se estão ativas
#se alguma não estiver ativa deve ser enviado uma msg a todas as comapanhias ativas
#as companhias ativas não requisitarão o mapa dessa companhia inativa
tcp.bind(host)
tcp.listen(4)
print("server on")
print("Aguardando conexões. . .")
while True:
    response = ''
    con, cliente = tcp.accept()
   
    print ('Conectado por', cliente)
    msg = con.recv(1024).decode()
    print ('companhia: ',msg)

    if msg == 'A':
        response = company_B+';'+company_C
    elif msg == 'B':
        response = company_A+';'+company_C
    elif msg == 'C':
        response = company_A + ';' + company_B
    elif msg == 'queue':
        response = priority_queue
    con.send(bytes(response, 'utf-8'))
    print ('Finalizando conexão com companhia: ', msg)
    con.close()