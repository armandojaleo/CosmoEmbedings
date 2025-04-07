# multi_node_launcher.py

import subprocess
import time

def start_node(port):
    return subprocess.Popen(["python", "node_simulator.py", str(port)])

if __name__ == "__main__":
    ports = [8080, 8081, 8082]
    nodes = []

    print("Launching multiple CosmicEmbeddings nodes:")
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
