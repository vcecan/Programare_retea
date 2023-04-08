import socket
import dns.resolver
print(f'Welcome to DNS application! \nfor begining here are disponible commands:\n'
      f'* /commands - show list of commands\n'
      f'* /resolve_domain / resolve_ip> - show a list of ip adresses assignet to domain or a list of domains assignet to ip adress\n'
      f'* /use_dns<ip> switch DNS server for browsing precedent commands')
while True:
    try:
        message=input('type the command:\n')
        if '/commands' in message:
            print(f'* /resolve<domain/ip> - show a list of ip adresses assignet to domain or a list of domains assignet to ip adress\n'
                  f'* /use_dns<ip> switch DNS server for browsing precedent commands')
        elif '/resolve_domain' in message:
            domain=input('type the domain:\n')
            #addresses = socket.gethostbyname_ex(domain)
            #for addr in addresses:
            print(socket.getaddrinfo(domain, 80))
            print('lista de ip-uri')
        elif '/resolve_ip' in message:
            ip_addr=input("type the ip adress:\n")
            print('lista de domainuri')
        elif '/use_dns' in message:
            dns_addr=input("type the dns adress")
            print(f'switched to {dns_addr} dns')


        #ip_adress = socket.gethostbyname(domain_name)

        #print(f'the ip of {domain_name} is {ip_adress}')
    except:
        print('error')