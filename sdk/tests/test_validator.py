# test_validator.py
from cosmoembeddings.validator import validate_block
import pytest
import time
from datetime import datetime
from cosmoembeddings.validator import CosmoValidator

def test_dummy_validation():
    block = {"signature": "signed_with_private_key"}
    assert validate_block(block, "demo_public_key") == True

def test_validator_initialization():
    validator = CosmoValidator(40.7128, -74.0060)  # New York coordinates
    assert validator.latitude == 40.7128
    assert validator.longitude == -74.0060
    assert validator.elevation == 0.0
    assert validator.location is not None

def test_get_celestial_signature():
    validator = CosmoValidator(40.7128, -74.0060)
    signature = validator.get_celestial_signature()
    
    assert "timestamp" in signature
    assert "location" in signature
    assert "celestial_bodies" in signature
    
    assert signature["location"]["latitude"] == 40.7128
    assert signature["location"]["longitude"] == -74.0060
    
    assert "sun" in signature["celestial_bodies"]
    assert "moon" in signature["celestial_bodies"]
    
    # Check sun data
    sun = signature["celestial_bodies"]["sun"]
    assert "altitude" in sun
    assert "azimuth" in sun
    assert "distance_au" in sun
    
    # Check moon data
    moon = signature["celestial_bodies"]["moon"]
    assert "altitude" in moon
    assert "azimuth" in moon
    assert "distance_au" in moon
    assert "phase" in moon

def test_get_celestial_signature_with_timestamp():
    validator = CosmoValidator(40.7128, -74.0060)
    timestamp = time.time()
    signature = validator.get_celestial_signature(timestamp)
    
    assert abs(signature["timestamp"] - timestamp) < 1  # Allow 1 second difference

def test_validate_block():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": int(time.time())
    }
    
    is_valid, reason = validator.validate_block(block)
    assert is_valid is True
    assert reason == "Block validated with cosmo signature"
    
    assert "cosmo_signature" in block
    assert "cosmo_hash" in block

def test_validate_block_missing_timestamp():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content"
    }
    
    is_valid, reason = validator.validate_block(block)
    assert is_valid is False
    assert reason == "Block missing timestamp"

def test_verify_cosmo_signature():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": int(time.time())
    }
    
    # First validate the block
    validator.validate_block(block)
    
    # Then verify the signature
    is_valid, reason = validator.verify_cosmo_signature(block)
    assert is_valid is True
    assert reason == "Cosmo signature verified"

def test_verify_cosmo_signature_missing_fields():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": int(time.time())
    }
    
    is_valid, reason = validator.verify_cosmo_signature(block)
    assert is_valid is False
    assert reason == "Block missing cosmo signature or hash"

def test_verify_cosmo_signature_modified():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": int(time.time())
    }
    
    # First validate the block
    validator.validate_block(block)
    
    # Modify the signature
    block["cosmo_signature"]["celestial_bodies"]["sun"]["altitude"] += 1.0
    
    # Then verify the signature
    is_valid, reason = validator.verify_cosmo_signature(block)
    assert is_valid is False
    assert "hash mismatch" in reason

def test_verify_cosmo_signature_old_timestamp():
    validator = CosmoValidator(40.7128, -74.0060)
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": int(time.time()) - 3600  # 1 hour ago
    }
    
    # First validate the block
    validator.validate_block(block)
    
    # Then verify the signature
    is_valid, reason = validator.verify_cosmo_signature(block)
    assert is_valid is False
    assert "timestamp too old" in reason
