---
layout: default
---

# Getting Started with CosmoEmbeddings

This guide will help you get started with CosmoEmbeddings quickly and easily.

## Installation

### Using pip

```bash
pip install cosmicembeddings
```

### Manual Installation

```bash
git clone https://github.com/armandojaleo/CosmoEmbeddings.git
cd CosmoEmbeddings/sdk
pip install -e .
```

## Quick Start

### 1. Create a Knowledge Block

Using the CLI:
```bash
cosmicembeddings create-block --text "Hello, CosmoEmbeddings!" --tag "greeting"
```

Using Python:
```python
from cosmicembeddings import BlockBuilder, Signer

# Create a block
builder = BlockBuilder()
block = builder.create_block(
    text="Hello, CosmoEmbeddings!",
    metadata={"tag": "greeting"}
)

# Sign the block
signer = Signer()
signed_block = signer.sign_block(block)
```

### 2. Verify a Block

Using the CLI:
```bash
cosmicembeddings verify-block --block-file block.json
```

Using Python:
```python
from cosmicembeddings import CosmoValidator

validator = CosmoValidator()
is_valid = validator.validate_block(signed_block)
print(f"Block is valid: {is_valid}")
```

### 3. Search for Blocks

Using the CLI:
```bash
cosmicembeddings search --tag "greeting"
```

Using Python:
```python
from cosmicembeddings import SyncClient

client = SyncClient()
blocks = client.search_blocks(tag="greeting")
for block in blocks:
    print(f"Found block: {block['id']}")
```

## Next Steps

1. [Explore Advanced Examples](sdk_detailed.md#advanced-examples)
2. [Learn about Cosmo Validation](cosmic_validation.md)
3. [Understand the Block Specification](block_spec.md)
4. [Join the Network](node_protocol.md)

## Need Help?

- Check the [FAQ](faq.md)
- Join our [Discord community](https://discord.gg/cosmicembeddings)
- Open an [issue](https://github.com/cosmicembeddings/sdk/issues) 