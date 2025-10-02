import nmap

def nmapWrapper(host):
    # Initialize the portscanner
    try:
        portScanner = nmap.PortScanner()
        # scan the host with arguments -sC -sV
        portScanner.scan(hosts=host, arguments='-sC -sV')
        csv = portScanner.csv()
        print(csv)
    except nmap.PortScannerError:
        print("Can't use the portScanner")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    nmapWrapper('127.0.0.1')

