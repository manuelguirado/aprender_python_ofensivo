import socket 
def scannerPorts(host,start_port, end_port ):
    try:
        for port in range (start_port, end_port +1):
              #the AF_INET param specifies the address family for IPv4 or IPv6 and the SOCKT_STREAM the comunication protocol
             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             sock.settimeout(0.5)
             #Connect to the remote socket 
             result = sock.connect_ex((host,port))
        if result == 0:
            #open ports
            print(f"port {port}: Open")
            #generating an file with the open ports
            openedFiles = open("port.txt", "w")
            sock.close
       
    except:
        print("unable to scan the ports")



scannerPorts("127.0.0.1",1,1000)

