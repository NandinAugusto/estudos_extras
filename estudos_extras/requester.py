import requests

url = "https://www.example.com"
resposta = requests.get(url)

print("[+] Cabeçalhos da resposta HTTP:")
for chave, valor in resposta.headers.items():
    print(f"{chave}: {valor}")

print("\n[+] Cabeçalhos de segurança detectados:")
cabecalhos_seguranca = [
    'Content-Security-Policy',
    'X-Frame-Options',
    'Strict-Transport-Security',
    'X-XSS-Protection',
    'X-Content-Type-Options',
    'Referrer-Policy'
]

for cabecalho in cabecalhos_seguranca:
    if cabecalho in resposta.headers:
        print(f"✓ {cabecalho}: {resposta.headers[cabecalho]}")