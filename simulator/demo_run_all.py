# demo_run_all.py

import subprocess
import threading
import time
import webbrowser

def run_script(path):
    return subprocess.Popen(["python", path])

def threaded_run(path):
    def wrapper():
        subprocess.run(["python", path])
    t = threading.Thread(target=wrapper)
    t.start()
    return t

if __name__ == "__main__":
    print("🚀 Launching full CosmicEmbeddings simulation...")

    # Start nodes in threads
    print("🛰 Starting simulated nodes...")
    threaded_run("threaded_multi_node_launcher.py")
    time.sleep(2)

    # Send a test block to node 8080
    print("📤 Sending block to node 8080...")
    threaded_run("client_send_block.py")
    time.sleep(1)

    # Start syncing blocks between nodes
    print("🔁 Starting synchronization...")
    threaded_run("sync_blocks_between_nodes.py")

    # Start Web UI
    print("🌐 Starting web interface...")
    threaded_run("web_ui_server.py")
    time.sleep(2)
    webbrowser.open("http://localhost:8090")

    print("✅ All systems active. Visit http://localhost:8090 to monitor blocks.")
    print("Press Ctrl+C to stop everything.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Simulation ended.")
