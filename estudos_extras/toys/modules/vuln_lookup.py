# modules/vuln_lookup.py
import requests

def buscar_vulnerabilidades(tech, max_results=5):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={tech}&resultsPerPage={max_results}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    cves = []
    for item in data.get('vulnerabilities', []):
        cve_id = item['cve']['id']
        desc = item['cve']['descriptions'][0]['value']
        cves.append((cve_id, desc))
    return cves