import socket #one of the most used packege for low-leve network programing
from concurrent import futures #This module will be assist us to run multiple threads for scanning the ports in parallel,
import sys
import time

def check_port(targetIp, portNumber, timeout): # no need to explain
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #af_inet = part of the ipv4 familiy , SOCK_STREAM = USEING TCP socket
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #sets options for reusing the address
    TCPsock.settimeout(timeout)
    try:
        TCPsock.connect((targetIp, portNumber))
        return (portNumber)
    except:
        return

def loading():
    animation = ["|", "/", "-", "\\"] # cool animation that i like ...
    for i in range(40):
        sys.stdout.write("\rScanning Ports " + animation[i % len(animation)]) 
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")

def port_scanner(targetIp, timeout):
    threadPoolSize = 500 # determines the number of threads that will be used to check
    portsToCheck = 10000 #  set to check 10000 ports

    executor = futures.ThreadPoolExecutor(max_workers=threadPoolSize)
    checks = [
        executor.submit(check_port, targetIp, port, timeout) #check_port = will run multiple threads in parallel to check he ports.
        for port in range(0, portsToCheck, 1)
    ]
    loading()
    opened_ports = []
    for response in futures.as_completed(checks):
        if (response.result()):
            opened_ports.append(response.result())
            print('Listening on port: {}'.format(response.result()))
    if not opened_ports:
        print("no ports are open")
    else:
        print("You should close these ports:")
        for port in opened_ports:
            print(port)

def main():
    targetIp = input("Enter the target IP address: ") 
    timeout = int(input("How long before the connection times out: "))
    port_scanner(targetIp, timeout)

if __name__ == "__main__":
    main()
