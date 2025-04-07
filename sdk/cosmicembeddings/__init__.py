"""
CosmicEmbeddings SDK

A decentralized semantic network for AIs built on embeddings.
"""

from .block_builder import BlockBuilder
from .signer import Signer
from .validator import CosmicValidator
from .cosmic_signature import CosmicSignatureGenerator
from .config import Config
from .sync_client import SyncClient

__version__ = "0.1.0"
__all__ = [
    "BlockBuilder",
    "Signer",
    "CosmicValidator",
    "CosmicSignatureGenerator",
    "Config",
    "SyncClient"
]
