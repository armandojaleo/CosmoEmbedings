# web_ui_server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

NODES = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082"
]

def get_all_blocks():
    all_blocks = []
    for url in NODES:
        try:
            r = requests.get(f"{url}/blocks", timeout=2)
            if r.status_code == 200:
                blocks = r.json()
                all_blocks.extend([
                    {**block, "source": url} for block in blocks
                ])
        except:
            pass
    return all_blocks

class WebHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        blocks = get_all_blocks()
        html = "<html><head><title>CosmoEmbeddings UI</title></head><body>"
        html += "<h1>🧠 CosmoEmbeddings - Block Viewer</h1><ul>"
        for block in blocks:
            html += f"<li><b>{block['id']}</b> @ {block['source']} | Tags: {', '.join(block.get('tags', []))}</li>"
        html += "</ul></body></html>"
        self.wfile.write(html.encode())

def run(server_class=HTTPServer, handler_class=WebHandler, port=8090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🌐 Web UI running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
