# threaded_multi_node_launcher.py

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

class NodeHandler(BaseHTTPRequestHandler):
    BLOCKS = {}

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/blocks/"):
            block_id = self.path.split("/")[-1]
            block = self.BLOCKS.get(block_id)
            self._set_headers(200 if block else 404)
            self.wfile.write(json.dumps(block or {}).encode())
        elif self.path.startswith("/blocks"):
            self._set_headers()
            self.wfile.write(json.dumps(list(self.BLOCKS.values())).encode())
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
                self.BLOCKS[block_id] = block
                self._set_headers(200)
                self.wfile.write(json.dumps({"status": "stored", "id": block_id}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Block ID missing"}).encode())

def run_node(port):
    class CustomHandler(NodeHandler):
        BLOCKS = {}

    server = HTTPServer(('', port), CustomHandler)
    print(f"Node running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    ports = [8080, 8081, 8082]
    threads = []

    for port in ports:
        t = threading.Thread(target=run_node, args=(port,), daemon=True)
        threads.append(t)
        t.start()

    print("All nodes are running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all nodes...")
