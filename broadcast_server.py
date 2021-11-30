import socket
   
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ('26.183.229.122', 50000)

company_A = 'ipA,55000'
company_B = 'ipB,56000'
company_C = 'ipC,57000'

tcp.bind(host)
tcp.listen(4)
print("server on")
print("Aguardando conexões. . .")
while True:
    response = ''
    con, cliente = tcp.accept()
    print ('Concetado por', cliente)
    msg = con.recv(1024).decode()
    print ('companhia: ',msg)
    if msg == 'A':
        response = company_B+';'+company_C
    elif msg == 'B':
        response = company_A+';'+company_C
    elif msg == 'C':
        response = company_A+';'+company_B
    con.send(bytes(response, 'utf-8'))
    print ('Finalizando conexão com companhia: ', msg)
    con.close()