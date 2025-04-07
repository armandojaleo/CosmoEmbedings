# Handles block creation

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Union, Optional
import json
import time
from datetime import datetime

class BlockBuilder:
    """Class for building embedding blocks with metadata."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the BlockBuilder with an embedding model.
        
        Args:
            model_name: Name of the SentenceTransformers model to use
        """
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        
    def create_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding for the given text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            np.ndarray: Embedding vector
        """
        return self.model.encode(text)
    
    def create_block(self, 
                    content: Union[str, List[str]], 
                    metadata: Optional[Dict] = None) -> Dict:
        """
        Create a block with embeddings and metadata.
        
        Args:
            content: Text or list of texts to generate embeddings for
            metadata: Additional metadata for the block
            
        Returns:
            Dict: Block with embeddings and metadata
        """
        if isinstance(content, str):
            content = [content]
            
        embeddings = [self.create_embedding(text) for text in content]
        
        block = {
            "version": "1.0",
            "timestamp": int(time.time()),
            "datetime": datetime.utcnow().isoformat(),
            "model": {
                "name": self.model_name,
                "dimensions": embeddings[0].shape[0]
            },
            "embeddings": [emb.tolist() for emb in embeddings],
            "content": content,
            "metadata": metadata or {}
        }
        
        return block
    
    def save_block(self, block: Dict, filepath: str) -> None:
        """
        Save a block to a JSON file.
        
        Args:
            block: Block to save
            filepath: Path to save the file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(block, f, indent=2)
            
    def load_block(self, filepath: str) -> Dict:
        """
        Load a block from a JSON file.
        
        Args:
            filepath: Path to load the file from
            
        Returns:
            Dict: Loaded block
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
