# CosmoEmbeddings SDK - Detailed Documentation

This document provides detailed information about the CosmoEmbeddings SDK, including API references, examples, and best practices.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Core Components](#core-components)
   - [BlockBuilder](#blockbuilder)
   - [Signer](#signer)
   - [CosmoValidator](#cosmovalidator)
   - [Config](#config)
   - [SyncClient](#syncclient)
4. [CLI Interface](#cli-interface)
5. [Examples](#examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Introduction

The CosmoEmbeddings SDK is a Python library that enables the creation, signing, and validation of knowledge blocks based on embeddings. It provides a decentralized semantic network where different AGIs using various LLMs can securely share and validate embeddings.

## Installation

```bash
# Install with pip (recommended)
cd sdk
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
pip install -e .
```

## Core Components

### BlockBuilder

The `BlockBuilder` class is responsible for creating knowledge blocks with embeddings and metadata.

```python
from cosmoembeddings import BlockBuilder

# Initialize the builder
builder = BlockBuilder()

# Create a block with text content
content = "This is an example text for embedding generation."
metadata = {
    "source": "example",
    "author": "user123",
    "tags": ["example", "test"]
}

# Create the block
block = builder.create_block(content, metadata)

# The block contains:
# - id: A unique identifier
# - embedding: A vector representation of the content
# - input_type: The type of input (e.g., "text")
# - input_reference: Information about the input
# - timestamp: When the block was created
# - observer_location: Where the block was created
# - cosmo_signature: A signature based on celestial positions
# - created_by: Who created the block
# - version: The block version
# - tags: Keywords for the block
# - linked_blocks: References to related blocks
```

### Signer

The `Signer` class provides cryptographic signing of blocks using Ed25519.

```python
from cosmoembeddings import Signer

# Initialize the signer
signer = Signer()

# Sign a block
signed_block = signer.sign_block(block)

# The signed block now includes:
# - signature: The Ed25519 signature of the block

# Verify a block's signature
is_valid = signer.verify_block(signed_block)
print(f"Signature valid: {is_valid}")
```

### CosmoValidator

The `CosmoValidator` class validates blocks using cosmo signatures based on celestial positions.

```python
from cosmoembeddings import CosmoValidator

# Initialize the validator with location
validator = CosmoValidator(
    latitude=40.7128,  # New York coordinates
    longitude=-74.0060,
    elevation=0.0
)

# Validate a block
is_valid, reason = validator.validate_block(signed_block)
print(f"Block valid: {is_valid}")
if not is_valid:
    print(f"Reason: {reason}")

# Get a celestial signature for a block
signature = validator.get_celestial_signature(block)
print(f"Celestial signature: {signature}")

# Verify a cosmo signature
is_valid, reason = validator.verify_cosmo_signature(signed_block)
print(f"Cosmo signature valid: {is_valid}")
if not is_valid:
    print(f"Reason: {reason}")
```

### Config

The `Config` class manages the SDK configuration.

```python
from cosmoembeddings import Config

# Initialize the config
config = Config()

# Load configuration from environment variables
config.load_from_env()

# Or load from a file
config.load_from_file("config.json")

# Get a configuration value
node_id = config.get("node_id", "default_node_id")

# Set a configuration value
config.set("api_endpoint", "https://api.cosmoembeddings.org")

# Save configuration to a file
config.save_to_file("config.json")
```

### SyncClient

The `SyncClient` class enables interaction with other nodes in the network.

```python
from cosmoembeddings import SyncClient

# Initialize the client
client = SyncClient(api_endpoint="https://api.cosmoembeddings.org")

# Push a block to the network
success = client.push_block(signed_block)
print(f"Block pushed: {success}")

# Get a block by ID
block = client.get_block("block_id_123")

# Search for blocks by tag
blocks = client.search_blocks("example")
print(f"Found {len(blocks)} blocks with tag 'example'")
```

## CLI Interface

The SDK provides a command-line interface for common operations.

```bash
# Create a new block with embeddings
cosmoembeddings create --content "Your text here" --sign --validate --latitude 40.7128 --longitude -74.0060

# Verify a block
cosmoembeddings verify block.json --latitude 40.7128 --longitude -74.0060

# Run tests
cosmoembeddings-test --verbose
```

## Examples

### Complete Workflow

```python
from cosmoembeddings import BlockBuilder, Signer, CosmoValidator, Config

# Initialize components
config = Config()
builder = BlockBuilder()
signer = Signer()
validator = CosmoValidator(
    latitude=40.7128,
    longitude=-74.0060,
    elevation=0.0
)

# Create a block
content = "This is an example of the complete workflow."
metadata = {
    "source": "example",
    "author": "user123",
    "tags": ["example", "workflow"]
}
block = builder.create_block(content, metadata)

# Sign the block
signed_block = signer.sign_block(block)

# Validate the block
is_valid, reason = validator.validate_block(signed_block)
print(f"Block valid: {is_valid}")
if not is_valid:
    print(f"Reason: {reason}")

# Save the block to a file
import json
with open("example_block.json", "w") as f:
    json.dump(signed_block, f, indent=2)
```

## Best Practices

1. **Always validate blocks before using them**:
   ```python
   is_valid, reason = validator.validate_block(block)
   if not is_valid:
       print(f"Invalid block: {reason}")
       return
   ```

2. **Use meaningful metadata**:
   ```python
   metadata = {
       "source": "your_source",
       "author": "your_name",
       "tags": ["relevant", "tags"],
       "description": "A brief description of the content"
   }
   ```

3. **Keep your private keys secure**:
   ```python
   # Store private keys in environment variables or secure storage
   import os
   private_key = os.environ.get("COSMIC_PRIVATE_KEY")
   ```

4. **Use consistent locations for cosmo validation**:
   ```python
   # Use the same location for creating and validating blocks
   validator = CosmoValidator(latitude=40.7128, longitude=-74.0060)
   ```

## Troubleshooting

### Common Issues

1. **Block validation fails**:
   - Check that the block has all required fields
   - Verify that the cosmo signature was generated at the correct location
   - Ensure the timestamp is valid

2. **Signature verification fails**:
   - Check that the block was signed with the correct private key
   - Verify that the block hasn't been tampered with

3. **Embedding generation fails**:
   - Check that the required models are installed
   - Verify that the input is in the correct format

### Getting Help

If you encounter issues not covered here, please:

1. Check the [GitHub repository](https://github.com/armandojaleo/CosmoEmbeddings/) for updates
2. Open an issue on GitHub with details about your problem
3. Join the [Discord community](https://discord.gg/cosmoembeddings) for real-time help 