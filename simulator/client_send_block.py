# client_send_block.py

import os
import sys
import requests
import json
import time
from datetime import datetime

# Add the SDK directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sdk')))

from cosmoembeddings import BlockBuilder, Signer, CosmoValidator, Config

# Initialize SDK components
config = Config()
builder = BlockBuilder()
signer = Signer()
validator = CosmoValidator(
    latitude=40.7128,  # New York coordinates
    longitude=-74.0060,
    elevation=0.0
)

# Create a block using the SDK
content = "This is an example block created by the simulator client."
metadata = {
    "source": "simulator",
    "author": "demo_client",
    "tags": ["demo", "test", "simulator"]
}

# Create the block
block = builder.create_block(content, metadata)

# Sign the block
signed_block = signer.sign_block(block)

# Validate the block with cosmo signature
is_valid, reason = validator.validate_block(signed_block)
if not is_valid:
    print(f"Block validation failed: {reason}")
    sys.exit(1)

# Send block to the local node
response = requests.post("http://localhost:8080/blocks", json=signed_block)

print("Status:", response.status_code)
print("Response:", response.json())
