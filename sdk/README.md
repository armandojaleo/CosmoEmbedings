
# CosmicEmbeddings SDK

This is the official Python SDK for the CosmicEmbeddings protocol.

It allows you to:
- Generate and sign knowledge blocks (based on embeddings)
- Validate blocks (including cosmic signature and cryptographic signatures)
- Interact with other nodes in the network

---

## 📦 Installation

```bash
cd sdk
pip install -e .
```

---

## 🚀 Usage Example

```bash
python cosmicembeddings/example_usage.py
```

You should see a signed block and its validation result printed.

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
├── signer.py          # Digitally sign a block
├── validator.py       # Validate a block (signature, cosmic, hash)
├── sync_client.py     # Peer-to-peer sync (planned)
├── config.py          # Configuration management
├── cli.py             # CLI entry point
└── example_usage.py   # Basic demo script

tests/
└── test_validator.py  # Minimal validation test
```

---

## 🔧 Configuration (optional)

Create a `.env` file or config object with:
```
NODE_ID=agent_demo
PRIVATE_KEY=demo_private_key
API_ENDPOINT=http://localhost:8080
DEFAULT_MODEL=demo-embedding-model
DEFAULT_LOCATION=40.4168,-3.7038
```

---

## 📚 Documentation

- [Block Specification](../docs/block_spec.md)
- [Node Protocol](../docs/node_protocol.md)
- [Sync Protocol](../docs/sync_protocol.md)
- [Cosmic Validation](../docs/cosmic_validation.md)
- [Architecture Overview](../docs/architecture.md)

---

Contributions are welcome! Let's build the next layer of decentralized AI together. ✨
