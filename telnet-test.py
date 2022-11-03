import socket
import selectors

HOST = ''
PORT = 4848

sel = selectors.DefaultSelector()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []

def accept_new_connection(soc, mask):
    conn, address = soc.accept()
    print(f'New connection ({len(clients) + 1}) from: {address[0]}')
    conn.setblocking(False)
    clients.append(conn)
    sel.register(conn, selectors.EVENT_READ, read_client_data)

def read_client_data(conn, mask):
    data = conn.recv(1000)
    if data:
        # conn.send(data) # Hope it won't block
        try:
            str = data.decode('utf-8').strip()
            print(str)
            if str == "clear":
                clear_screen(conn)
            else:
                broadcast(str + '\r\n')
        except UnicodeDecodeError as e:
            print("Control character received", data)
    else:
        print('Good bye!')
        sel.unregister(conn)
        clients.remove(conn)
        conn.close()

def broadcast(msg):
    for client in clients:
        client.send(msg.encode('utf-8'))

def clear_screen(conn):
    conn.send("\033[2J".encode('utf-8'))

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
finally:
    soc.close()
