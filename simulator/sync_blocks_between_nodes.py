# sync_blocks_between_nodes.py

import os
import sys
import requests
import time
import json

# Add the SDK directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sdk')))

from cosmoembeddings import BlockBuilder, Signer, CosmoValidator, Config

NODES = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082"
]

# Initialize SDK components
config = Config()
builder = BlockBuilder()
signer = Signer()
validator = CosmoValidator(
    latitude=40.7128,  # New York coordinates
    longitude=-74.0060,
    elevation=0.0
)

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
        else:
            print(f"Error syncing block to {node_url}: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error posting to {node_url}: {e}")

def validate_block(block):
    """Validate a block using the SDK."""
    # Verify the block's signatures
    if not signer.verify_block(block):
        print(f"Block {block['id']} signature verification failed")
        return False
        
    # Verify cosmo signature
    is_valid, reason = validator.verify_cosmo_signature(block)
    if not is_valid:
        print(f"Block {block['id']} cosmo signature verification failed: {reason}")
        return False
        
    return True

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
                # Validate the block before syncing
                if validate_block(block):
                    post_block(node, block)
                else:
                    print(f"Skipping invalid block {block_id}")

if __name__ == "__main__":
    print("Starting sync loop. Press Ctrl+C to stop.")
    print(f"Using SDK version: {config.get('version', 'unknown')}")
    try:
        while True:
            sync_all()
            time.sleep(10)  # Sync every 10 seconds
    except KeyboardInterrupt:
        print("Stopped sync.")
