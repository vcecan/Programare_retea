# + S-a creat un server și client care e capabil să se conecteze la server - 5 puncte
# + Server are posibilitate de a accepta concomitent mai mulți clienți - 1 punct
# + Client e capabil să trimită mesaje către server, iar server poate să-l primească și să afișeze în fereastra sa - 1 punct
# + Serverul e capabil să retransmită mesaje către clienți - 1 punct
# - Clienții sunt capabili să afișeze mesaje primite de la server - 1 punct
# - Client și server să poată conecta/deconecta/transmită datele fără excepții critice - 1 punct

import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("127.0.0.1",999))

#primeste toate packetele
server.listen()

print("server started")
clients = []
aliases =[]

def broadcast(message):
    for client in clients:
            client.send(message)



def send_message():
    while True:
            message_input = f'server: {input()}'
            broadcast(message_input.encode('utf-8'))


def handle_client(client):
    while True:
        try:
            message=client.recv(1024)
            if message == False:
                index = clients.index(client)
                alias = aliases[index]
                print(f'Client {alias} closed the connection')
                client.close()
                break
            broadcast(message)
            print(message.decode('utf-8'))
            #message_input = input()
            #broadcast(message_input, client)
            send_thread = threading.Thread(target=send_message)
            send_thread.start()
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias= aliases[index]
            broadcast(f'{alias} left chat '.encode('utf-8'))
            aliases.remove(alias)
            break
def receive():
    while True:
        #print("server is running")
        client,adress = server.accept()
        print(f' connection is established with {str(adress)}')
        client.send('alias?'.encode('utf8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'the alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the server'.encode('utf-8'))
        client.send('\n you are now connected'.encode('utf-8'))
        if not client.fileno():
            print(f'Client disconnected: {adress}')
            client.close()
            break
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__ == '__main__':
            receive()
