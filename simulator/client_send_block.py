# client_send_block.py

import requests
import json

# Example block to send
block = {
    "id": "block-demo-001",
    "embedding": [0.12, -0.85, 0.33],
    "embedding_format": "demo-embedding-model",
    "input_type": "text",
    "input_reference": {
        "hash": "sha256-of-input",
        "origin": "manual"
    },
    "timestamp": "2025-04-06T18:43:00Z",
    "observer_location": {
        "lat": 40.4168,
        "lon": -3.7038
    },
    "cosmic_signature": "Orion-127.5",
    "created_by": "agent_demo",
    "signature": "demo_signature",
    "version": 1,
    "tags": ["demo", "test"],
    "linked_blocks": []
}

# Send block to the local node
response = requests.post("http://localhost:8080/blocks", json=block)

print("Status:", response.status_code)
print("Response:", response.json())
