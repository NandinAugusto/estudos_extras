# modules/tech_fingerprint.py
import requests
from bs4 import BeautifulSoup

def fingerprint_techs(url):
    headers = requests.get(url).headers
    techs = []

    server = headers.get("Server")
    if server:
        techs.append(server)

    x_powered = headers.get("X-Powered-By")
    if x_powered:
        techs.append(x_powered)

    # Analisa bibliotecas JS em HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.find_all("script", src=True)
    for s in scripts:
        src = s['src']
        if "jquery" in src.lower():
            techs.append("jQuery")
        if "bootstrap" in src.lower():
            techs.append("Bootstrap")
        if "react" in src.lower():
            techs.append("ReactJS")
        if "vue" in src.lower():
            techs.append("VueJS")

    return list(set(techs)) 