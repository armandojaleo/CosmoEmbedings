#!/usr/bin/env python
# custom_embedding_model.py

"""
This example demonstrates how to integrate the CosmoEmbeddings SDK with a custom embedding model.
It shows how to create blocks with embeddings from different sources and share them in the network.
"""

import os
import sys
import json
import numpy as np
from datetime import datetime

# Add the parent directory to the path to import the SDK
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cosmoembeddings import BlockBuilder, Signer, CosmoValidator, Config

# Custom embedding model class
class CustomEmbeddingModel:
    """A simple custom embedding model for demonstration purposes."""
    
    def __init__(self, model_name="custom-model-v1"):
        self.model_name = model_name
        self.embedding_size = 384  # Standard size for many embedding models
    
    def generate_embedding(self, text):
        """
        Generate an embedding for the given text.
        In a real implementation, this would use a pre-trained model.
        For demonstration, we'll generate a random embedding.
        """
        # In a real implementation, you would use a model like:
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # return model.encode(text)
        
        # For demonstration, generate a random embedding
        np.random.seed(hash(text) % 2**32)  # Deterministic based on text
        return np.random.rand(self.embedding_size).tolist()
    
    def get_model_info(self):
        """Return information about the model."""
        return {
            "name": self.model_name,
            "version": "1.0.0",
            "embedding_size": self.embedding_size,
            "description": "Custom embedding model for demonstration"
        }

# Custom block builder that uses our custom model
class CustomBlockBuilder(BlockBuilder):
    """A block builder that uses a custom embedding model."""
    
    def __init__(self, model=None):
        super().__init__()
        self.model = model or CustomEmbeddingModel()
    
    def create_block(self, content, metadata=None):
        """
        Create a block with embeddings from the custom model.
        
        Args:
            content: The text content to embed
            metadata: Additional metadata for the block
            
        Returns:
            A complete block with embeddings from the custom model
        """
        # Generate embedding using the custom model
        embedding = self.model.generate_embedding(content)
        
        # Get model information
        model_info = self.model.get_model_info()
        
        # Create the block
        block = super().create_block(content, metadata)
        
        # Update the embedding and model information
        block["embedding"] = embedding
        block["embedding_format"] = model_info["name"]
        block["embedding_model"] = model_info
        
        return block

def main():
    """Run the example."""
    print("CosmoEmbeddings SDK - Custom Embedding Model Example")
    print("=====================================================")
    
    # Initialize components
    config = Config()
    builder = CustomBlockBuilder()
    signer = Signer()
    validator = CosmoValidator(
        latitude=40.7128,  # New York coordinates
        longitude=-74.0060,
        elevation=0.0
    )
    
    # Create a block with custom embeddings
    content = "This is an example of using a custom embedding model with CosmoEmbeddings."
    metadata = {
        "source": "custom_example",
        "author": "demo_user",
        "tags": ["custom", "example", "embeddings"]
    }
    
    print("\n1. Creating a block with custom embeddings...")
    block = builder.create_block(content, metadata)
    print(f"Block created with ID: {block['id']}")
    print(f"Embedding size: {len(block['embedding'])}")
    print(f"Embedding model: {block['embedding_format']}")
    
    # Sign the block
    print("\n2. Signing the block...")
    signed_block = signer.sign_block(block)
    print("Block signed successfully")
    
    # Validate the block
    print("\n3. Validating the block...")
    is_valid, reason = validator.validate_block(signed_block)
    print(f"Block valid: {is_valid}")
    if not is_valid:
        print(f"Reason: {reason}")
    
    # Save the block to a file
    output_file = "custom_block.json"
    print(f"\n4. Saving the block to {output_file}...")
    with open(output_file, "w") as f:
        json.dump(signed_block, f, indent=2)
    print("Block saved successfully")
    
    # Demonstrate how to load and verify a block
    print("\n5. Loading and verifying the block...")
    with open(output_file, "r") as f:
        loaded_block = json.load(f)
    
    # Verify the block's signature
    is_valid = signer.verify_block(loaded_block)
    print(f"Signature valid: {is_valid}")
    
    # Verify the cosmo signature
    is_valid, reason = validator.verify_cosmo_signature(loaded_block)
    print(f"Cosmo signature valid: {is_valid}")
    if not is_valid:
        print(f"Reason: {reason}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 