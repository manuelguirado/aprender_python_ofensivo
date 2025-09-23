import socket

def scannPorts(host):
    try:
        for port in range(1,1024):
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host,port))
        if result == 0:
            print(f'this port {port}: are opened')
            sock.close( )
        else:
            print("this machine doesn't have any opened port")
    except:
            print("unable to scan the opened ports ")


scannPorts('127.0.0.1')
