import socket
import threading

def multiThreadScanner(host, port_range):
    try:
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            connect = sock.connect_ex((host, port))
            if connect == 0:
                print(f"Port {port} is open")
            sock.close()
    except Exception:
        print("Can't scan the port")

def createThreads(host, num_threads=10):
    threads = []
    ports = range(1, 65536)
    chunk_size = len(ports) // num_threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else 65536
        thread = threading.Thread(target=multiThreadScanner, args=(host, range(start, end)))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    createThreads('127.0.0.1', num_threads=10)