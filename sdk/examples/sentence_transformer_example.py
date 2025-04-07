#!/usr/bin/env python
# sentence_transformer_example.py

"""
This example demonstrates how to use the CosmoEmbeddings SDK with the SentenceTransformer model.
It shows how to create blocks with real embeddings from a pre-trained model.
"""

import os
import sys
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Add the parent directory to the path to import the SDK
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cosmicembeddings import BlockBuilder, Signer, CosmoValidator, Config

class SentenceTransformerModel:
    """A wrapper for the SentenceTransformer model."""
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_size = self.model.get_sentence_embedding_dimension()
    
    def generate_embedding(self, text):
        """Generate an embedding using the SentenceTransformer model."""
        return self.model.encode(text).tolist()
    
    def get_model_info(self):
        """Return information about the model."""
        return {
            "name": self.model_name,
            "version": "2.2.2",  # Current version of sentence-transformers
            "embedding_size": self.embedding_size,
            "description": "SentenceTransformer model for generating text embeddings"
        }

class SentenceTransformerBlockBuilder(BlockBuilder):
    """A block builder that uses the SentenceTransformer model."""
    
    def __init__(self, model=None):
        super().__init__()
        self.model = model or SentenceTransformerModel()
    
    def create_block(self, content, metadata=None):
        """
        Create a block with embeddings from the SentenceTransformer model.
        
        Args:
            content: The text content to embed
            metadata: Additional metadata for the block
            
        Returns:
            A complete block with embeddings from the model
        """
        # Generate embedding using the model
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
    print("CosmoEmbeddings SDK - SentenceTransformer Example")
    print("=================================================")
    
    # Initialize components
    config = Config()
    builder = SentenceTransformerBlockBuilder()
    signer = Signer()
    validator = CosmoValidator(
        latitude=40.7128,  # New York coordinates
        longitude=-74.0060,
        elevation=0.0
    )
    
    # Example texts to embed
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A man is walking down the street with his dog.",
        "The weather is beautiful today in New York."
    ]
    
    # Create blocks for each text
    blocks = []
    for i, text in enumerate(texts, 1):
        print(f"\n{i}. Creating block for text: {text}")
        metadata = {
            "source": "sentence_transformer_example",
            "author": "demo_user",
            "tags": ["sentence_transformer", "example", "embeddings"]
        }
        
        block = builder.create_block(text, metadata)
        print(f"Block created with ID: {block['id']}")
        print(f"Embedding size: {len(block['embedding'])}")
        print(f"Embedding model: {block['embedding_format']}")
        
        # Sign the block
        signed_block = signer.sign_block(block)
        print("Block signed successfully")
        
        # Validate the block
        is_valid, reason = validator.validate_block(signed_block)
        print(f"Block valid: {is_valid}")
        if not is_valid:
            print(f"Reason: {reason}")
        
        blocks.append(signed_block)
    
    # Save all blocks to a file
    output_file = "sentence_transformer_blocks.json"
    print(f"\nSaving all blocks to {output_file}...")
    with open(output_file, "w") as f:
        json.dump(blocks, f, indent=2)
    print("Blocks saved successfully")
    
    # Demonstrate similarity search between blocks
    print("\nDemonstrating similarity search between blocks...")
    for i, block1 in enumerate(blocks):
        for j, block2 in enumerate(blocks[i+1:], i+1):
            # Calculate cosine similarity between embeddings
            embedding1 = np.array(block1["embedding"])
            embedding2 = np.array(block2["embedding"])
            similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
            
            print(f"\nSimilarity between blocks {i+1} and {j+1}: {similarity:.4f}")
            print(f"Text 1: {block1['content']}")
            print(f"Text 2: {block2['content']}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 