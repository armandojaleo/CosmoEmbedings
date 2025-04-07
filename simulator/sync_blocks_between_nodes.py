# sync_blocks_between_nodes.py

import requests
import time

NODES = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082"
]

def fetch_blocks(node_url):
    try:
        r = requests.get(f"{node_url}/blocks", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Error fetching from {node_url}: {e}")
    return []

def post_block(node_url, block):
    try:
        r = requests.post(f"{node_url}/blocks", json=block, timeout=2)
        if r.status_code == 200:
            print(f"Block {block['id']} synced to {node_url}")
    except Exception as e:
        print(f"Error posting to {node_url}: {e}")

def sync_all():
    all_blocks = {}
    # Collect all blocks from all nodes
    for node in NODES:
        blocks = fetch_blocks(node)
        for block in blocks:
            all_blocks[block['id']] = block

    # Push all unique blocks to all nodes
    for node in NODES:
        existing = {b['id'] for b in fetch_blocks(node)}
        for block_id, block in all_blocks.items():
            if block_id not in existing:
                post_block(node, block)

if __name__ == "__main__":
    print("Starting sync loop. Press Ctrl+C to stop.")
    try:
        while True:
            sync_all()
            time.sleep(10)  # Sync every 10 seconds
    except KeyboardInterrupt:
        print("Stopped sync.")
