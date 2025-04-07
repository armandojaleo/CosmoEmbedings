---
layout: default
---

# Node Protocol

The Node Protocol is a fundamental component of the CosmoEmbeddings network, enabling nodes to discover each other, establish connections, and maintain a peer-to-peer network.

## Overview

The Node Protocol consists of three main components:

1. **Node Identity**: A unique identifier for each node in the network
2. **Discovery Service**: A mechanism for nodes to find each other
3. **Peer Management**: A system for maintaining connections with other nodes

## Node Identity

Each node in the network has a unique identity represented by the `NodeIdentity` class:

```python
@dataclass
class NodeIdentity:
    node_id: str          # Unique identifier (UUID)
    public_key: str       # Public key for cryptographic operations
    address: str          # Network address
    port: int            # Network port
    version: str         # Protocol version
    capabilities: List[str]  # Node capabilities
    last_seen: float     # Timestamp of last activity
```

### Creating a Node Identity

```python
from cosmoembeddings import Node, Config

# Create a new node
config = Config()
node = Node(config)

# Access node identity
identity = node.identity
print(f"Node ID: {identity.node_id}")
print(f"Address: {identity.address}:{identity.port}")
```

## Discovery Service

The Discovery Service uses UDP broadcast to find other nodes in the network:

```python
# Start node discovery
node.start_discovery()

# Stop discovery when done
node.stop_discovery()
```

### How Discovery Works

1. Each node broadcasts its identity periodically
2. Nodes listen for broadcasts from other nodes
3. When a new node is discovered, it's added to the peer list
4. The discovery service runs in a separate thread to avoid blocking

### Configuration

The discovery service can be configured through the `Config` class:

```python
config = Config()
config.set("discovery_port", 8091)  # Port for discovery service
config.set("node_address", "localhost")  # Node's network address
config.set("node_port", 8090)  # Node's main port
```

## Peer Management

Nodes maintain a list of known peers and can interact with them:

```python
# Get list of known peers
peers = node.get_peers()
for peer in peers:
    print(f"Peer: {peer.node_id} at {peer.address}:{peer.port}")

# Add a peer manually
node.add_peer(peer_identity)

# Remove a peer
node.remove_peer(peer_id)
```

### Peer State

The state of each peer is tracked, including:
- Last seen timestamp
- Connection status
- Capabilities
- Version compatibility

## Best Practices

1. **Identity Management**
   - Always use unique node IDs
   - Keep public keys secure
   - Update node capabilities as needed

2. **Discovery**
   - Use appropriate broadcast intervals
   - Handle network errors gracefully
   - Implement timeout mechanisms

3. **Peer Management**
   - Regularly clean up inactive peers
   - Verify peer capabilities
   - Maintain connection state

## Example Usage

Here's a complete example of using the Node Protocol:

```python
from cosmoembeddings import Node, Config
import time

# Create and configure a node
config = Config()
config.set("node_address", "localhost")
config.set("node_port", 8090)
config.set("discovery_port", 8091)

node = Node(config)

# Start discovery
node.start_discovery()

try:
    # Run for a while
    while True:
        # Get and print peers
        peers = node.get_peers()
        print(f"Known peers: {len(peers)}")
        for peer in peers:
            print(f"  - {peer.node_id} ({peer.address}:{peer.port})")
        
        time.sleep(5)
except KeyboardInterrupt:
    # Clean shutdown
    node.stop_discovery()
```

## Next Steps

The Node Protocol will be extended with:

1. **Node Reputation**
   - Track node behavior
   - Implement trust metrics
   - Add reputation-based routing

2. **Enhanced Configuration**
   - Dynamic port assignment
   - Network interface selection
   - Protocol version negotiation

3. **Security Features**
   - Encrypted communication
   - Authentication mechanisms
   - Access control lists
