# CosmicEmbeddings SDK

This is the official Python SDK for the CosmicEmbeddings protocol.

It allows you to:
- Generate and sign knowledge blocks (based on embeddings)
- Validate blocks with cosmic signatures (using celestial positions)
- Cryptographically sign blocks with Ed25519
- Interact with the network through a CLI interface

---

## 📦 Installation

```bash
cd sdk
pip install -e .
```

---

## 🚀 Quick Start

### Using the CLI

```bash
# Create a new block with embeddings
cosmicembeddings create --content "Your text here" --sign --validate --latitude 40.7128 --longitude -74.0060

# Verify a block
cosmicembeddings verify block.json --latitude 40.7128 --longitude -74.0060
```

### Using the Python API

```python
from cosmicembeddings import BlockBuilder, Signer, CosmicValidator

# Create a block
builder = BlockBuilder()
block = builder.create_block("Your text here", metadata={"source": "example"})

# Sign the block
signer = Signer()
signed_block = signer.sign_block(block)

# Validate with cosmic signature
validator = CosmicValidator(latitude=40.7128, longitude=-74.0060)
is_valid, reason = validator.validate_block(signed_block)
```

For a complete example, run:
```bash
python cosmicembeddings/example_usage.py
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📁 SDK Structure

```
cosmicembeddings/
├── block_builder.py   # Create new blocks with embeddings and metadata
├── signer.py          # Ed25519 cryptographic signatures
├── validator.py       # Cosmic validation using celestial positions
├── cli.py             # Command-line interface
├── __init__.py        # Package exports
└── example_usage.py   # Complete usage example

tests/
├── test_block_builder.py  # Tests for block creation
├── test_signer.py         # Tests for cryptographic signatures
└── test_validator.py      # Tests for cosmic validation
```

---

## 🔧 Configuration

The SDK can be configured through environment variables or directly in code:

```python
# Using environment variables
import os
os.environ["COSMIC_LATITUDE"] = "40.7128"
os.environ["COSMIC_LONGITUDE"] = "-74.0060"
os.environ["COSMIC_ELEVATION"] = "0.0"

# Or directly in code
validator = CosmicValidator(latitude=40.7128, longitude=-74.0060, elevation=0.0)
```

---

## 📚 Documentation

- [Block Specification](../docs/block_spec.md)
- [Node Protocol](../docs/node_protocol.md)
- [Sync Protocol](../docs/sync_protocol.md)
- [Cosmic Validation](../docs/cosmic_validation.md)
- [Architecture Overview](../docs/architecture.md)

---

## 🌟 Features

### Block Creation
- Generate embeddings from text using state-of-the-art models
- Add metadata and timestamps
- Save and load blocks from JSON files

### Cryptographic Signatures
- Ed25519 digital signatures
- Public/private key management
- Signature verification

### Cosmic Validation
- Celestial position-based validation
- Sun and moon position tracking
- Timestamp verification
- Location-based validation

### CLI Interface
- Create and verify blocks from command line
- Support for file input/output
- Metadata management
- Validation options

---

Contributions are welcome! Let's build the next layer of decentralized AI together. ✨
