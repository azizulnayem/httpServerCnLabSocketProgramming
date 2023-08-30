import socket

HOST, PORT = '', 8080

HTML_FILES = {
    '/': 'index.html',
    '/index.html': 'index.html',
    '/about.html': 'about.html'
}

HTTP_200_OK = 'HTTP/1.0 200 OK\n\n'
HTTP_404_NOT_FOUND = 'HTTP/1.0 404 NOT FOUND\n\n'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Serving HTTP on port', PORT)

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

while True:
    client_connection, client_address = server_socket.accept()
    
    request_message = client_connection.recv(1024).decode()
    
    path = request_message.split()[1]
    
    file_path = HTML_FILES.get(path, None)
    
    if not file_path:
        response_message = HTTP_404_NOT_FOUND.encode()
        client_connection.sendall(response_message)
        client_connection.close()
        continue
    
    file_contents = read_file(file_path)
    response_message = (HTTP_200_OK + file_contents).encode()
    client_connection.sendall(response_message)

    client_connection.close()
