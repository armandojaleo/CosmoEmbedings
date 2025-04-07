---
layout: default
---

# Getting Started with CosmoEmbeddings

This guide will help you get started with CosmoEmbeddings quickly and easily.

## Installation

### Using pip

```bash
# Standard installation
pip install cosmoembeddings

# If you encounter permission errors on Windows, use:
pip install --user cosmoembeddings

# Or create and use a virtual environment (recommended)
python -m venv cosmoenv
# On Windows:
cosmoenv\Scripts\activate
# On Linux/Mac:
source cosmoenv/bin/activate
pip install cosmoembeddings
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
cosmoembeddings create-block --text "Hello, CosmoEmbeddings!" --tag "greeting"
```

Using Python:
```python
from cosmoembeddings import BlockBuilder, Signer

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
cosmoembeddings verify-block --block-file block.json
```

Using Python:
```python
from cosmoembeddings import CosmoValidator

validator = CosmoValidator()
is_valid = validator.validate_block(signed_block)
print(f"Block is valid: {is_valid}")
```

### 3. Search for Blocks

Using the CLI:
```bash
cosmoembeddings search --tag "greeting"
```

Using Python:
```python
from cosmoembeddings import SyncClient

client = SyncClient()
blocks = client.search_blocks(tag="greeting")
for block in blocks:
    print(f"Found block: {block['id']}")
```

## Troubleshooting

### Permission Errors on Windows

If you encounter permission errors like:
```
ERROR: Could not install packages due to an OSError: [WinError 5] Access is denied
```

Try these solutions:

1. **Use the `--user` flag**:
   ```bash
   pip install --user cosmoembeddings
   ```

2. **Run Command Prompt as Administrator**:
   - Right-click on Command Prompt
   - Select "Run as administrator"
   - Try the installation again

3. **Use a Virtual Environment** (recommended):
   ```bash
   python -m venv cosmoenv
   cosmoenv\Scripts\activate
   pip install cosmoembeddings
   ```

### Python Version Compatibility

If you encounter errors related to `ed25519` package installation, especially on Python 3.12:
```
AttributeError: module 'configparser' has no attribute 'SafeConfigParser'
```

This is a known issue with the `ed25519` package on Python 3.12. Try these solutions:

1. **Use Python 3.11 or earlier** (recommended):
   ```bash
   # Create virtual environment with Python 3.11
   python3.11 -m venv cosmoenv
   ```

2. **Install an alternative ed25519 package**:
   ```bash
   pip install pynacl
   # Then install cosmoembeddings
   pip install cosmoembeddings
   ```

### Other Common Issues

- **ModuleNotFoundError**: Make sure you've activated your virtual environment
- **Command not found**: Ensure the package is installed and your PATH is set correctly
- **Connection errors**: Check your internet connection and firewall settings

## Next Steps

1. [Explore Advanced Examples](sdk_detailed.md#advanced-examples)
2. [Learn about Cosmo Validation](cosmo_validation.md)
3. [Understand the Block Specification](block_spec.md)
4. [Join the Network](node_protocol.md)

## Need Help?

- Check the [FAQ](faq.md)
- Join our [Discord community](https://discord.gg/cosmoembeddings)
- Open an [issue](https://github.com/armandojaleo/CosmoEmbeddings/issues) 