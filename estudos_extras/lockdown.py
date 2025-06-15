import socket

HOST = '0.0.0.0' 
PORT = 12345     

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escutando na porta {PORT}...")
    conn, addr = server_socket.accept()
    with conn:
        print(f"Conexão recebida de {addr}")
        conn.sendall('Olá, cliente!'.encode('utf-8'))
        print("Mensagem enviada. Encerrando conexão.")