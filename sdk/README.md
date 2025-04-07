# CosmoEmbeddings SDK

The CosmoEmbeddings SDK is a Python library for creating, signing, and validating knowledge blocks based on embeddings. It allows you to generate and sign knowledge blocks, validate blocks with cosmic signatures, and cryptographically sign with Ed25519.

## 📦 Installation

### Option 1: Install with pip (recommended)

```bash
cd sdk
pip install -e .
```

This will install the SDK in development mode and all required dependencies.

### Option 2: Install dependencies manually

If you prefer to install dependencies manually:

```bash
cd sdk
pip install -r requirements.txt
pip install -e .
```

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
from cosmicembeddings import BlockBuilder, Signer, CosmoValidator

# Create a block
builder = BlockBuilder()
block = builder.create_block("Your text here", metadata={"source": "example"})

# Sign the block
signer = Signer()
signed_block = signer.sign_block(block)

# Validate with cosmic signature
validator = CosmoValidator(latitude=40.7128, longitude=-74.0060)
is_valid, reason = validator.validate_block(signed_block)
```

For a complete example, run:
```bash
python cosmicembeddings/example_usage.py
```

## 📚 Advanced Examples

The SDK includes several examples that demonstrate different functionalities:

### Custom Embedding Model Example

```bash
# Run the custom embedding model example
python examples/custom_embedding_model.py
```

This example shows how to integrate a custom embedding model with the SDK.

### SentenceTransformer Example

```bash
# Run the SentenceTransformer example
python examples/sentence_transformer_example.py
```

This example demonstrates how to use the SDK with the SentenceTransformer model to generate real embeddings and perform similarity searches.

## 🧪 Running Tests

### Using the test script

```bash
# Run all tests
cosmicembeddings-test

# Run tests in verbose mode
cosmicembeddings-test --verbose

# Generate coverage report
cosmicembeddings-test --coverage

# Run specific tests
cosmicembeddings-test --test test_block_builder.py --test test_signer.py
```

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run tests in verbose mode
pytest -v tests/

# Generate coverage report
pytest --cov=cosmicembeddings --cov-report=term-missing tests/
```

## 📁 SDK Structure

```
cosmicembeddings/
├── block_builder.py      # Create new blocks with embeddings and metadata
├── signer.py             # Ed25519 cryptographic signatures
├── validator.py          # Cosmo validation using celestial positions
├── cosmic_signature.py   # Cosmo signature generation
├── config.py             # Configuration management
├── sync_client.py        # Client for synchronization with other nodes
├── cli.py                # Command-line interface
├── __init__.py           # Package exports
└── example_usage.py      # Complete usage example

examples/
├── custom_embedding_model.py    # Example with custom model
└── sentence_transformer_example.py  # Example with SentenceTransformer

tests/
├── test_block_builder.py  # Tests for block creation
├── test_signer.py         # Tests for cryptographic signatures
└── test_validator.py      # Tests for cosmic validation
```

## 🔧 Configuration

The SDK can be configured through environment variables or directly in code:

```python
# Using environment variables
import os
os.environ["COSMIC_LATITUDE"] = "40.7128"
os.environ["COSMIC_LONGITUDE"] = "-74.0060"
os.environ["COSMIC_ELEVATION"] = "0.0"

# Or directly in code
from cosmicembeddings import Config
config = Config()
config.set_location(40.7128, -74.0060, 0.0)
```

## 📚 Documentation

For detailed documentation, see:

- [SDK Detailed Documentation](../docs/sdk_detailed.md) - Complete guide with examples and best practices
- [Block Specification](../docs/block_spec.md) - Structure and fields of blocks
- [Node Protocol](../docs/node_protocol.md) - Node behavior and responsibilities
- [Sync Protocol](../docs/sync_protocol.md) - How nodes communicate
- [Cosmo Validation](../docs/cosmic_validation.md) - How cosmic signatures work
- [Architecture](../docs/architecture.md) - System overview

## 🌟 Features

### Block Creation
- Generate text embeddings using state-of-the-art models
- Add metadata and timestamps
- Save and load blocks from JSON files

### Cryptographic Signatures
- Ed25519 digital signatures
- Public/private key management
- Signature verification

### Cosmo Validation
- Celestial position-based validation
- Sun and moon position tracking
- Timestamp verification
- Location-based validation

### Sync Client
- Interaction with other nodes in the network
- Search for blocks by tags or similarity
- Share blocks with other nodes

### CLI Interface
- Create and verify blocks from command line
- Support for file input/output
- Metadata management
- Validation options

---

Contributions are welcome! Let's build the next layer of decentralized AI together. ✨
