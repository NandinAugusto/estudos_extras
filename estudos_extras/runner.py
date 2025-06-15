import socket

def escanear_portas(host, portas):
    socket.setdefaulttimeout(1)
    for porta in portas:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultado = s.connect_ex((host, porta))
        if resultado == 0:
            print(f"[+] Porta {porta} está aberta")
        else:
            print(f"[-] Porta {porta} está fechada ou filtrada")
        s.close()

host = 'localhost'  
portas = [21, 22, 23, 80, 443, 3389]
escanear_portas(host, portas)