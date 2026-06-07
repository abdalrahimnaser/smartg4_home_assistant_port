import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", 6000))

print("Listening on UDP 6000...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"{addr}: {data.hex(' ')}")