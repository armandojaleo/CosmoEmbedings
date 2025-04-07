"""
CosmicEmbeddings SDK

A decentralized semantic network for AIs built on embeddings.
"""

from .block_builder import BlockBuilder
from .signer import Signer
from .validator import CosmicValidator

__version__ = "0.1.0"
__all__ = ["BlockBuilder", "Signer", "CosmicValidator"]
