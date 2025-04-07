import pytest
import numpy as np
import os
import tempfile
from cosmoembeddings.block_builder import BlockBuilder

def test_block_builder_initialization():
    builder = BlockBuilder()
    assert builder.model_name == "all-MiniLM-L6-v2"
    assert builder.model is not None

def test_create_embedding():
    builder = BlockBuilder()
    text = "Hello, world!"
    embedding = builder.create_embedding(text)
    assert isinstance(embedding, np.ndarray)
    assert embedding.ndim == 1

def test_create_block_single_text():
    builder = BlockBuilder()
    text = "Hello, world!"
    block = builder.create_block(text)
    
    assert "version" in block
    assert "timestamp" in block
    assert "datetime" in block
    assert "model" in block
    assert "embeddings" in block
    assert "content" in block
    assert "metadata" in block
    
    assert len(block["embeddings"]) == 1
    assert len(block["content"]) == 1
    assert block["content"][0] == text

def test_create_block_multiple_texts():
    builder = BlockBuilder()
    texts = ["Hello, world!", "Another text"]
    block = builder.create_block(texts)
    
    assert len(block["embeddings"]) == 2
    assert len(block["content"]) == 2
    assert block["content"] == texts

def test_create_block_with_metadata():
    builder = BlockBuilder()
    text = "Hello, world!"
    metadata = {"source": "test", "author": "tester"}
    block = builder.create_block(text, metadata)
    
    assert block["metadata"] == metadata

def test_save_and_load_block():
    builder = BlockBuilder()
    text = "Hello, world!"
    metadata = {"source": "test"}
    block = builder.create_block(text, metadata)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        filepath = tmp.name
        
    try:
        builder.save_block(block, filepath)
        loaded_block = builder.load_block(filepath)
        
        assert loaded_block["version"] == block["version"]
        assert loaded_block["content"] == block["content"]
        assert loaded_block["metadata"] == block["metadata"]
        assert len(loaded_block["embeddings"]) == len(block["embeddings"])
    finally:
        os.unlink(filepath) 