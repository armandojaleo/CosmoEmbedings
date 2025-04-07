# example_usage.py
from cosmicembeddings.block_builder import create_block
from cosmicembeddings.signer import sign_block
from cosmicembeddings.validator import validate_block

# Placeholder example functions
def create_block(input_data, input_type, model, location, tags):
    return {
        "id": "block-example",
        "embedding": [0.1, 0.2, 0.3],
        "embedding_format": model,
        "input_type": input_type,
        "input_reference": {
            "hash": "dummyhash",
            "origin": "local"
        },
        "timestamp": "2025-04-06T18:43:00Z",
        "observer_location": {
            "lat": location[0],
            "lon": location[1]
        },
        "cosmic_signature": "Orion-127.5",
        "created_by": "agent_demo",
        "tags": tags,
        "linked_blocks": []
    }

def sign_block(block, private_key):
    block["signature"] = "signed_with_private_key"
    return block

def validate_block(block, public_key):
    return block.get("signature") == "signed_with_private_key"

# Demo
block = create_block("The mitochondria is the powerhouse of the cell.", "text", "demo-embedding-model", (40.4168, -3.7038), ["bio"])
signed = sign_block(block, "demo_private_key")
print("Block signed:", signed)

is_valid = validate_block(signed, "demo_public_key")
print("Validation result:", is_valid)
