import re 
import ipaddress
def ipExtractor(ips):
 candidates = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
 valid = set()
 for ip in candidates:
    try:
          valid.add(str(ipaddress.IPv4Address(ip)))
    except:
        continue
    return sorted(valid, key=lambda ip: tuple(int(x) for x in ip.split('.')))
text = "hosts: 10.0.0.1, 10.0.0.1, 256.0.0.1, 192.168.0.5"
print(ipExtractor(text))
