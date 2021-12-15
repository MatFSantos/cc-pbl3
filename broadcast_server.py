import socket

"""
    Servidor de broadcast, sendo a primeira conexão das companhias.
"""

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ('0.0.0.0', 50000)

company_A = '26.183.229.122,55000,A' #ip de hospedagem da companhia A
company_B = '26.90.73.25,56000,B' #ip de hospedagem da companhia A
company_C = '26.90.73.25,57000,C' #ip de hospedagem da companhia A


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

    con.send(bytes(response, 'utf-8'))
    print ('Finalizando conexão com companhia: ', msg)
    con.close()