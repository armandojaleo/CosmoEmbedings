# CosmoEmbeddings – Simulator

This folder contains a local simulation environment for testing and demo purposes. The simulator now uses the CosmoEmbeddings SDK for all operations, including block creation, signing, validation, and cosmic signature verification.

---

## 🔧 Installation

Install all required dependencies:

```bash
# From the simulator directory
pip install -r requirements.txt
```

This will install the SDK in development mode and all other required packages.

---

## 🛰 node_simulator.py

Runs a local HTTP server simulating a CosmoEmbeddings node. Now includes:
- Full SDK integration
- Block validation with cosmic signatures
- Ed25519 signature verification
- Real-time block validation

- `POST /blocks` → Store a block (with validation)
- `GET /blocks` → List all blocks
- `GET /blocks/:id` → Get block by ID

Run:
```bash
python node_simulator.py
```

---

## 📤 client_send_block.py

Creates and sends a sample block to a running node using the SDK:
- Uses BlockBuilder for block creation
- Signs blocks with Ed25519
- Validates blocks with cosmic signatures
- Includes real embedding generation

```bash
python client_send_block.py
```

---

## 🔁 threaded_multi_node_launcher.py

Launches 3 independent nodes (ports 8080–8082) with separate storage using threads. Each node:
- Uses the SDK configuration
- Validates blocks with cosmic signatures
- Maintains its own block storage

```bash
python threaded_multi_node_launcher.py
```

---

## 🔄 sync_blocks_between_nodes.py

Synchronizes blocks across all running nodes every 10 seconds:
- Validates blocks before syncing
- Verifies Ed25519 signatures
- Checks cosmic signatures
- Ensures block integrity

```bash
python sync_blocks_between_nodes.py
```

---

## 🌐 web_ui_server.py

Starts a minimal web interface at [http://localhost:8090](http://localhost:8090) to:
- View all blocks
- Monitor block validation status
- Check cosmic signatures
- Track block synchronization

```bash
python web_ui_server.py
```

---

## 🚀 demo_run_all.py

Runs the full simulation with SDK integration:
1. Launches nodes with cosmic validation
2. Creates and sends a block with real embeddings
3. Syncs blocks with signature verification
4. Opens the UI for monitoring

```bash
python demo_run_all.py
```

---

## 🔧 Requirements

- Python 3.7+
- CosmoEmbeddings SDK (installed from `../sdk`)
- Required Python packages (see `requirements.txt`):
  - numpy
  - scikit-learn
  - transformers
  - torch
  - requests
  - flask
  - flask-cors
  - python-dotenv
  - skyfield
  - ed25519
  - pandas
  - tqdm

---

Use this folder to test, extend, and explore the CosmoEmbeddings protocol locally. The simulator now provides a complete demonstration of the SDK's capabilities, including real embedding generation, cryptographic signatures, and cosmic validation.
