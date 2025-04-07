# node_simulator.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory store for demo purposes
BLOCKS = {}

class SimpleNodeHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/blocks/"):
            block_id = self.path.split("/")[-1]
            block = BLOCKS.get(block_id)
            self._set_headers(200 if block else 404)
            self.wfile.write(json.dumps(block or {}).encode())
        elif self.path.startswith("/blocks"):
            self._set_headers()
            self.wfile.write(json.dumps(list(BLOCKS.values())).encode())
        else:
            self._set_headers(404)
            self.wfile.write(b"{}")

    def do_POST(self):
        if self.path == "/blocks":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            block = json.loads(post_data.decode())
            block_id = block.get("id")
            if block_id:
                BLOCKS[block_id] = block
                self._set_headers(200)
                self.wfile.write(json.dumps({"status": "stored", "id": block_id}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Block ID missing"}).encode())

def run(server_class=HTTPServer, handler_class=SimpleNodeHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Node simulator running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
