import psutil
import socket

def get_process_name(pid):
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "Desconhecido"

def monitor_conexoes():
    print(f"{'PID':<8} {'Nome':<25} {'Local':<22} {'Remoto':<22} {'Status'}")
    print("-" * 90)

    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        pid = conn.pid if conn.pid else 0
        name = get_process_name(pid)

        print(f"{pid:<8} {name:<25} {laddr:<22} {raddr:<22} {conn.status}")

if __name__ == "__main__":
    monitor_conexoes()