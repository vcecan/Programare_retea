import socket
import threading
import random


last_message=None
addresses=None
port =9090
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket de tip udp
client_socket.bind(('127.0.0.1', random.randint(5000,9000))) # connectam la ip si port
nick='' # nickname-ul clientului
#print('Press enter to start')
print("write a nickname: ")
#client_socket.sendto(nick.encode('utf-8'), ("127.0.0.1", 9090))
# send data to server
def send_message():

    while True:
        global port, last_message, addresses, nick
        try:
            message = input("")  #in caz ca e primul mesaj, se va inregistra ca nickname
            if nick=='':
                nick=message
            last_message=message #pastram ultimul mesaj
            if '/connect' in message:  #comanda pentru a ne conecta la un anumit client se scrie sub forma "/connect port"
               mini_messages=message.split(' ')   #split pentru a separa portul
               #print (addresses)
               #for addr  in addresses:
                   #if addr[1] in message:
                       #port =addr[1]
               port=int(mini_messages[-1])
               print(port)
               client_socket.sendto(f'connected to {port}'.encode('utf-8'), ("127.0.0.1",port))

            elif message ==None:
                pass
            else:
                if port != 9090:
                    client_socket.sendto(f'{nick}:{message}'.encode("utf-8"), ("127.0.0.1", port))
                elif port == 9090:
                    client_socket.sendto(message.encode('utf-8'), ("127.0.0.1", port))

        except:
            print("Error!")
            #client_socket.bind(('127.0.0.1', random.randint(5000, 9000)))


def recieve_message():
    global addresses
    # receive response from server
    while True:
        try:
            response, sender_address = client_socket.recvfrom(1024)
            if last_message == '/members':
                addresses= response.decode()
            print(response.decode())
        except:
            print('Error!')
            #client_socket.bind(('127.0.0.1', random.randint(5000, 9000)))


receive_thread=threading.Thread(target=recieve_message)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()