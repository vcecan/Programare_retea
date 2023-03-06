import socket
import threading
import atexit
import signal
import os

alias=input('choose an alias : ')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",999))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            else:
                print (message)
        except:
            print('Error!')
            client.close()
            break
#def ex_thread():
 #   exit_thread = threading.Thread(target=exit)
  #  exit_thread.start()

def exit():
    # clean up code here
    #message=f'{alias} left the server'
    client.send(f'{alias} left the server'.encode("utf-8"))
    #print("left server")
    client.close()

pid = os.getpid()
def client_send():
    while True:
        try:
            message= f'{alias}: {input("")}'
            client.send(message.encode("utf-8"))
        except:
            message=f'{alias}:o l left the server'
            client.send(message.encode("utf-8"))
            os.kill(pid, signal.SIGTERM)
        #atexit.register(exit)


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()



atexit.register(exit)
signal.signal(signal.SIGTERM, exit)
signal.signal(signal.SIGINT, exit)
# force-close the process using os.kill
#os.kill(pid, signal.SIGTERM)