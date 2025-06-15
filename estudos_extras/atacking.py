import socket

HOST = '127.0.0.1'  
PORT = 12345        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    mensagem = client_socket.recv(1024)
    print(f"Mensagem recebida do servidor: {mensagem.decode()}")
    