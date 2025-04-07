# node_simulator.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
import time
from datetime import datetime

# Add the SDK directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sdk')))

from cosmicembeddings import BlockBuilder, Signer, CosmicValidator, Config

# In-memory store for demo purposes
BLOCKS = {}

# Initialize SDK components
config = Config()
builder = BlockBuilder()
signer = Signer()
validator = CosmicValidator(
    latitude=40.7128,  # New York coordinates
    longitude=-74.0060,
    elevation=0.0
)

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
            
            if not block_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Block ID missing"}).encode())
                return
                
            # Validate the block
            is_valid, reason = validator.validate_block(block)
            if not is_valid:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Block validation failed: {reason}"}).encode())
                return
                
            # Verify the block's signatures
            if not signer.verify_block(block):
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Block signature verification failed"}).encode())
                return
                
            # Verify cosmic signature
            is_valid, reason = validator.verify_cosmic_signature(block)
            if not is_valid:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Cosmic signature verification failed: {reason}"}).encode())
                return
                
            # Store the block
            BLOCKS[block_id] = block
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "stored", "id": block_id}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(b"{}")

def run(server_class=HTTPServer, handler_class=SimpleNodeHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Node simulator running on port {port}")
    print(f"Using SDK version: {config.get('version', 'unknown')}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
