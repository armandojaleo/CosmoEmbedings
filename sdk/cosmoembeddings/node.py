"""
Node protocol implementation for CosmoEmbeddings.
This module handles node discovery, peer management, and node identity.
"""

import uuid
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from .config import Config
from .discovery import DiscoveryService

@dataclass
class NodeIdentity:
    """Represents a node's identity in the network."""
    node_id: str
    public_key: str
    address: str
    port: int
    version: str
    capabilities: List[str]
    last_seen: float

class Node:
    """
    Represents a node in the CosmoEmbeddings network.
    Handles node discovery, peer management, and identity.
    """
    
    def __init__(self, config: Config):
        """Initialize a new node with the given configuration."""
        self.config = config
        self.identity = self._create_identity()
        self.peers: Dict[str, NodeIdentity] = {}
        self.discovery_port = config.get("discovery_port", 8091)
        self.discovery_service = DiscoveryService(port=self.discovery_port)
        
    def _create_identity(self) -> NodeIdentity:
        """Create a new node identity."""
        return NodeIdentity(
            node_id=str(uuid.uuid4()),
            public_key=self.config.get("public_key", ""),
            address=self.config.get("node_address", "localhost"),
            port=self.config.get("node_port", 8090),
            version="0.1.0",
            capabilities=["block_creation", "validation", "sync"],
            last_seen=time.time()
        )
    
    def start_discovery(self) -> None:
        """Start the node discovery service."""
        self.discovery_service.start(
            self.identity,
            self._handle_discovered_node
        )
    
    def stop_discovery(self) -> None:
        """Stop the node discovery service."""
        self.discovery_service.stop()
    
    def _handle_discovered_node(self, peer: NodeIdentity) -> None:
        """Handle a newly discovered node."""
        self.add_peer(peer)
        # Update last seen timestamp
        peer.last_seen = time.time()
    
    def add_peer(self, peer: NodeIdentity) -> None:
        """Add a new peer to the node's peer list."""
        self.peers[peer.node_id] = peer
        
    def remove_peer(self, peer_id: str) -> None:
        """Remove a peer from the node's peer list."""
        if peer_id in self.peers:
            del self.peers[peer_id]
            
    def get_peers(self) -> List[NodeIdentity]:
        """Get a list of all known peers."""
        return list(self.peers.values())
    
    def broadcast_identity(self) -> None:
        """Broadcast the node's identity to the network."""
        self.discovery_service._broadcast_identity(self.identity)
    
    def to_dict(self) -> Dict:
        """Convert the node's identity to a dictionary."""
        return asdict(self.identity)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Node':
        """Create a node instance from a dictionary."""
        config = Config()
        node = cls(config)
        node.identity = NodeIdentity(**data)
        return node
    
    def save_state(self, filepath: str) -> None:
        """Save the node's state to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f)
    
    @classmethod
    def load_state(cls, filepath: str) -> 'Node':
        """Load a node's state from a file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data) 