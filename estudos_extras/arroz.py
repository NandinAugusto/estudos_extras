import os
import json
import pytz
import platform
from datetime import datetime
from browser_history import get_history
import win32evtlog  
from tqdm import tqdm  

timeline = []

def normalize_time(ts):
    local_tz = pytz.timezone("America/Sergipe") 
    local_dt = local_tz.localize(ts)
    return local_dt.astimezone(pytz.utc)

def coletar_metadados(caminho):
    print("Coletando metadados de arquivos...")
    for root, dirs, files in os.walk(caminho):
        for f in tqdm(files, desc=f"Pasta: {root}", leave=False):
            try:
                full_path = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
                timeline.append({
                    "tipo": "arquivo",
                    "caminho": full_path,
                    "timestamp": normalize_time(mtime).isoformat()
                })
            except:
                continue

def coletar_eventos():
    print("Coletando eventos de log...")
    server = 'localhost'
    log_types = ['Security', 'System', 'Application']
    for log_type in log_types:
        hand = win32evtlog.OpenEventLog(server, log_type)
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        print(f"📋 Log: {log_type} ({total} eventos)")
        events = win32evtlog.ReadEventLog(
            hand, 
            win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 
            0
        )
        for event in tqdm(events, desc=f"🧾 {log_type}", leave=False):
            timestamp = normalize_time(event.TimeGenerated)
            timeline.append({
                "tipo": f"eventlog_{log_type}",
                "mensagem": str(event.StringInserts),
                "timestamp": timestamp.isoformat()
            })

def coletar_navegador():
    print("Coletando histórico do navegador...")
    outputs = get_history()
    for entry in tqdm(outputs.histories, desc="🌐 Histórico Navegador"):
        timestamp = normalize_time(entry[0])
        timeline.append({
            "tipo": "navegador",
            "url": entry[1],
            "timestamp": timestamp.isoformat()
        })

coletar_metadados("C:\\Users\\") 

if platform.system() == "Windows":
    coletar_eventos()

coletar_navegador()

timeline.sort(key=lambda x: x["timestamp"])

with open("timeline_forense.json", "w", encoding='utf-8') as f:
    json.dump(timeline, f, indent=4, ensure_ascii=False)

print("Timeline forense gerada: timeline_forense.json")
