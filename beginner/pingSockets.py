import socket
import time

def checkport(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except Exception:
        return False
    else:
        sock.close()
        return True

def timeCheck(host, port, timeout=2):
    start_time = time.time()
    if checkport(host, port, timeout):
        return time.time() - start_time

def connectPort(host, port, timeout=5, retries=5):
    try:
        minimum = float('inf')
        maximum = float('-inf')
        sumation = 0
        errors = 0
        for _ in range(retries):
            checktime = timeCheck(host, port, timeout)
            if checktime is None:
                print("can't check the time")
                errors += 1
            else:
                maximum = max(maximum, checktime)
                minimum = min(minimum, checktime)
                sumation += checktime
        if retries > errors:
            print(f"Max Time: {maximum:0.5f}s")
            print(f"Min Time: {minimum:0.5f}s")
            print(f"Average: {sumation/(retries-errors):0.2f}s")
        print(f"Failures: {errors}/{retries}")
    except socket.timeout:
        print("the port is not open")

if __name__ == '__main__':
    connectPort('127.0.0.1', 80)
