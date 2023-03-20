import socket
import threading
import pickle

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host_ip='127.0.0.1'
host_port=9090

server.bind((host_ip,host_port))

addresses=[]
nicknames=[]
members={}

def broadcast(message,sender):
    for addr in addresses:
        if addr != sender:
                message = f"\033[34m{message}\033[0m"
                server.sendto(message.encode('utf-8'),addr)

def send_message():
    while True:
            message_input = f'server: {input()}'
            broadcast(message_input,('127.0.0.1',9090))

def handle_client():
    while True:
        global addresses
        global nicknames
        try:
            message, addr = server.recvfrom(1024)
            if addr not in addresses:
                nick = message.decode('utf-8')
                addresses.append(addr)
                nicknames.append(nick)
                members[nick] = addr
                print(f"{nick } joined the chat")
                server.sendto('\n you are now connected'.encode('utf-8'), addr)
                print(f'the nickaname of {addr} client is {nick}')
                broadcast(f'{nick} has connected to the server \n addres is: {addr}', (host_ip, host_port))
                thread_handle = threading.Thread(target=handle_client)
                thread_handle.start()
            #print(message.decode('utf-8'))
            if message== None or message== False or message.decode('utf-8')=='' :
                pass
            index=addresses.index(addr)
            message=message.decode('utf-8')
            if message=='/members':
                #print(f'{members} \n')
                #serialized_members = pickle.dumps(members)
                server.sendto(str(members).encode('utf-8'),addr)
            elif 'connected to' in message:
                print(message)
            else:
                message=nicknames[index]+ ' : '+message
                print(message)
                #print(addresses)
                broadcast(message,addr)
            #print(message.decode('utf-8'))

            send_thread = threading.Thread(target=send_message)
            send_thread.start()
        except:
            print('Error,please try again')
            continue


def receive():

    while True:
      global addresses
      global nicknames
      try:
          nickname,  addr =server.recvfrom(1024)
          if addr not in addresses:
            #if addr not in addresses:
                print(f'{str(addr)} joined chat')
                #server.sendto('write a nickname:'.encode('utf8'),addr)
                #nick=server.recvfrom(1024)[0].decode('utf-8')
                nick =nickname.decode('utf-8')
                addresses.append(addr)
                #index = addresses.index(addr)
                nicknames.append(nick)
                members[nick] = addr
                server.sendto('\n you are now connected'.encode('utf-8'), addr)
                print(f'the nickaname of {addr} client is {nick}')
                broadcast(f'{nick} has connected to the server \n addres is: {addr}',(host_ip,host_port))
                thread_handle=threading.Thread(target=handle_client)
                thread_handle.start()
      except:
        print('Error')
        continue

if __name__ == '__main__':
            receive()



            ##################culori diferite la server si private