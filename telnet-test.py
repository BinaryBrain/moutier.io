import socket
import selectors

HOST = ''
PORT = 4848

KEY_UP = b'\x1b[A'
KEY_DOWN = b'\x1b[B'
KEY_RIGHT = b'\x1b[C'
KEY_LEFT = b'\x1b[D'

sel = selectors.DefaultSelector()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []

def accept_new_connection(soc, mask):
    conn, address = soc.accept()
    print(f'New connection ({len(clients) + 1}) from: {address[0]}')
    conn.setblocking(False)
    clients.append(conn)
    set_mode(conn)
    sel.register(conn, selectors.EVENT_READ, read_client_data)

def read_client_data(conn, mask):
    data = conn.recv(1024)
    if data:
        if data == KEY_UP:
            send(conn, "UP")
        if data == KEY_DOWN:
            send(conn, "DOWN")
        if data == KEY_LEFT:
            send(conn, "LEFT")
        if data == KEY_RIGHT:
            send(conn, "RIGHT")

        try:
            str = data.decode('utf-8').strip()
            print(str)
            if str == "clear":
                clear_screen(conn)
            # else:
                # broadcast(str + '\r\n')
        except UnicodeDecodeError as e:
            print("Control character received", data)
    else:
        print('Good bye!')
        sel.unregister(conn)
        clients.remove(conn)
        conn.close()

def send(conn, msg):
    conn.send(msg.encode('utf-8'))

def broadcast(msg):
    for client in clients:
        client.send(msg.encode('utf-8'))

def clear_screen(conn):
    conn.send("\033[2J".encode('utf-8'))

# Change the mode so that each character is sent without pressing ENTER
def set_mode(conn):
    conn.send(b"\xff\xfd\x22") # IAC DO LINEMODE
    conn.send(b"\xff\xfa\x22\x01\x00\xff\xf0") # IAC SB LINEMODE MODE 0 IAC SE

def set_client_echo(conn, bool):
    if bool:
        conn.send(b"\xff\xfb\x01") # IAC WILL ECHO
    else:
        conn.send(b"\xff\xfc\x01") # IAC WILL NOT ECHO

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
