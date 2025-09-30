import nmap
#portScanner
portScanner = nmap.PortScanner()
#define the host to scan the ports
ports =portScanner.scan('127.0.0.1 ', '0-2040')
commandLine = portScanner.command_line()
checkTheHost = portScanner.all_hosts()
hostName = portScanner['127.0.0.1'].hostname()
checkTheState = portScanner["127.0.0.1"].state()
checkAllProtocols = portScanner["127.0.0.1"].all_protocols()
protocols = portScanner["127.0.0.1"].keys()
checkTheProtocol = portScanner["127.0.0.1"].has_tcp(22)


for host in portScanner.all_hosts():
    print("--------------------------------")
    print('Host : %s (%s)' % (host,portScanner[host].hostname()))
    print('State : %s ' % portScanner[host].state())
    for proto in portScanner[host].all_protocols():
        print("------------")
        print('Protocol : %s'  % proto)
        lport = portScanner[host][proto].keys()
        lport.sort()
        for port in lport:
            print('port : %s\tstate :%s' % (port,portScanner[host][proto][port]['state']))
print("scan" , ports, "command line",commandLine,"check the host" ,checkTheHost,"check the hostname" ,hostName,"check the state" , checkTheState,"family protoclos"
      ,checkAllProtocols)
print("protcols" , protocols,"check if the machine has the port ", checkTheProtocol)
print(portScanner.csv())