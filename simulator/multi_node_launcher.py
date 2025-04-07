# multi_node_launcher.py

import subprocess
import time
import os
import sys

# Add the SDK directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sdk')))

from cosmoembeddings import Config

# Initialize SDK components
config = Config()

def start_node(port):
    return subprocess.Popen(["python", "node_simulator.py", str(port)])

if __name__ == "__main__":
    ports = [8080, 8081, 8082]
    nodes = []

    print(f"Launching multiple CosmoEmbeddings nodes (SDK version: {config.get('version', 'unknown')}):")
    for port in ports:
        print(f" - Node on port {port}")
        nodes.append(subprocess.Popen(["python", "node_simulator.py"], env={**dict(**os.environ), "PORT": str(port)}))
        time.sleep(1)

    print("\nNodes are running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all nodes...")
        for node in nodes:
            node.terminate()
