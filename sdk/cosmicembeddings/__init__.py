"""
CosmicEmbeddings SDK - A decentralized semantic network for AIs built on embeddings.
"""

from .block_builder import BlockBuilder
from .signer import Signer
from .validator import CosmicValidator
from .config import Config
from .sync_client import SyncClient
from .node import Node, NodeIdentity
from .discovery import DiscoveryService

__version__ = "0.1.0"

__all__ = [
    "BlockBuilder",
    "Signer",
    "CosmicValidator",
    "Config",
    "SyncClient",
    "Node",
    "NodeIdentity",
    "DiscoveryService"
]
