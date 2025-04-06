# Network Synchronization Protocol – CosmicEmbeddings

This document defines how nodes in the CosmicEmbeddings network discover each other and synchronize knowledge blocks.

The goal is to enable decentralized, reliable propagation of validated knowledge without relying on a central authority.

---

## 🔹 Peer Discovery

Nodes can find each other using:

- **Bootstrap list**: A configurable list of known, trusted nodes.
- **Gossip protocol**: Nodes share info about peers they know, forming a dynamic graph.
- **DID registry (optional)**: Use decentralized identity registries to locate active nodes and their endpoints.

---

## 🔹 Communication Protocol

Nodes communicate over HTTPS or WebSocket using a simple JSON-based API.

Endpoints to support:

- `GET /blocks/:id` – Retrieve a block by ID
- `GET /blocks?tag=...` – Search blocks by tag
- `POST /blocks` – Submit a new block
- `GET /status` – Get node status and block count
- `GET /peers` – List known peers

---

## 🔹 Sync Strategies

Nodes may use one or more of the following:

- **Push**: On creation or validation, a node sends blocks to peers immediately.
- **Pull**: Nodes periodically query peers for new or updated blocks.
- **Diff sync**: Nodes exchange lists of known block IDs or timestamps to resolve deltas.
- **Subscription**: Nodes can subscribe to changes in specific tags or agents.

---

## 🔹 Trust and Verification

Each received block must go through full validation (as defined in `block_spec.md`) before acceptance.

- Peers that repeatedly send invalid or corrupted blocks can be blacklisted.
- Trust heuristics may influence propagation preferences or sync frequency.

---

## 🔹 Storage and Propagation

- Each node maintains a local store of blocks (e.g., database or flat files).
- Nodes may choose to cache all blocks or only those relevant to their interest/tags.
- Large-scale nodes can serve as public mirrors or archives for resilience.

---

## 🔹 Federation and Interoperability

- Multiple independent networks of CosmicEmbedding nodes may federate via bridge nodes.
- Translation layers can allow integration with non-native nodes or alternate formats.

---

This protocol is designed to scale horizontally and operate over unstable or disconnected networks.
