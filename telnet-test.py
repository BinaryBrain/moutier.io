import socket
import selectors

HOST = ''
PORT = 4848

sel = selectors.DefaultSelector()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []

def accept_new_connection(soc, mask):
    connection, address = soc.accept()
    print(f'New connection ({len(clients) + 1}) from: {address[0]}')
    connection.setblocking(False)
    clients.append(connection)
    sel.register(connection, selectors.EVENT_READ, read_client_data)

def read_client_data(connection, mask):
    data = connection.recv(1000)
    if data:
        print(data)
        # connection.send(data) # Hope it won't block
        broadcast(data)
    else:
        print('Good bye!')
        sel.unregister(connection)
        clients.remove(connection)
        connection.close()

def broadcast(msg):
    for client in clients:
        client.send(msg)

def main():
    soc.bind((HOST, PORT))
    soc.listen()
    soc.setblocking(False)

    print('Server listening...')
    sel.register(soc, selectors.EVENT_READ, accept_new_connection)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

try:
    main()
except Exception as e:
    print(str(e))
finally:
    soc.close()
