import socket

HOST = ''
PORT = 4848

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def main():
    soc.bind((HOST, PORT))
    soc.listen()

    print('Server listening...')

    connection, address = soc.accept()
    with connection:
        print(f"Connected by {address}")
        while True:
            data = connection.recv(1024)
            connection.sendall(data)

try:
    main()
except Exception as e:
    print(str(e))
finally:
    soc.close()
