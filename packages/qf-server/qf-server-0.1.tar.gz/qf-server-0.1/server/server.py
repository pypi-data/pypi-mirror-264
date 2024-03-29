import socket
import threading
import ssl
import configparser

# Configurations 
config = configparser.ConfigParser()
config.read('config.ini')
file_path = config['DEFAULT']['linuxpath']
reread_on_query = config.getboolean('DEFAULT', 'REREAD_ON_QUERY', fallback=False)
ssl_enabled = config.getboolean('DEFAULT', 'SSL_ENABLED', fallback=False)

def handle_client(client_socket):
    data = client_socket.recv(1024).decode().rstrip('\x00')
    with open(file_path, 'r') as file:
        if reread_on_query:
            lines = file.readlines()
            if data + '\n' in lines:
                client_socket.send(b'STRING EXISTS\n')
            else:
                client_socket.send(b'STRING NOT FOUND\n')
        else:
            for line in file:
                if line.strip() == data:
                    client_socket.send(b'STRING EXISTS\n')
                    return
            client_socket.send(b'STRING NOT FOUND\n')
    client_socket.close()

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if ssl_enabled:
        server_socket = ssl.wrap_socket(server_socket, certfile='cert.pem', keyfile='key.pem', server_side=True)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f'Server listening on {ip}:{port}')
    while True:
        client_socket, address = server_socket.accept()
        print(f'New connection from {address[0]}:{address[1]}')
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    ip = '192.168.96.1' 
    port = 8086 
    start_server(ip, port)
