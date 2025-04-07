# CosmicEmbeddings – Simulator

This folder contains a local simulation environment for testing and demo purposes.

---

## 🛰 node_simulator.py

Runs a local HTTP server simulating a CosmicEmbeddings node.

- `POST /blocks` → Store a block
- `GET /blocks` → List all blocks
- `GET /blocks/:id` → Get block by ID

Run:
```bash
python node_simulator.py
```

---

## 📤 client_send_block.py

Sends a sample block to a running node.

```bash
python client_send_block.py
```

---

## 🔁 threaded_multi_node_launcher.py

Launches 3 independent nodes (ports 8080–8082) with separate storage using threads.

```bash
python threaded_multi_node_launcher.py
```

---

## 🔄 sync_blocks_between_nodes.py

Synchronizes blocks across all running nodes every 10 seconds.

```bash
python sync_blocks_between_nodes.py
```

---

## 🌐 web_ui_server.py

Starts a minimal web interface at [http://localhost:8090](http://localhost:8090) to view all blocks.

```bash
python web_ui_server.py
```

---

## 🚀 demo_run_all.py

Runs the full simulation: launches nodes, sends a block, syncs, and opens the UI.

```bash
python demo_run_all.py
```

---

Use this folder to test, extend, and explore the CosmicEmbeddings protocol locally.
