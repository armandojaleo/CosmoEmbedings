import pytest
import base64
from cosmicembeddings.signer import Signer

def test_signer_initialization():
    signer = Signer()
    assert signer.signing_key is not None
    assert signer.verifying_key is not None

def test_signer_from_seed():
    original_signer = Signer()
    seed = original_signer.signing_key.to_seed()
    new_signer = Signer.from_seed(seed)
    assert new_signer.get_public_key() == original_signer.get_public_key()

def test_get_public_key():
    signer = Signer()
    public_key = signer.get_public_key()
    assert isinstance(public_key, str)
    # Verify it's valid base64
    try:
        base64.b64decode(public_key)
    except Exception:
        pytest.fail("Public key is not valid base64")

def test_sign_block():
    signer = Signer()
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": 1234567890
    }
    
    signed_block = signer.sign_block(block)
    
    assert "signature" in signed_block
    assert "public_key" in signed_block
    assert signed_block["public_key"] == signer.get_public_key()
    
    # Verify the signature is valid base64
    try:
        base64.b64decode(signed_block["signature"])
    except Exception:
        pytest.fail("Signature is not valid base64")

def test_verify_block():
    signer = Signer()
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": 1234567890
    }
    
    signed_block = signer.sign_block(block)
    assert signer.verify_block(signed_block) is True

def test_verify_block_invalid():
    signer = Signer()
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": 1234567890
    }
    
    signed_block = signer.sign_block(block)
    # Modify the block after signing
    signed_block["content"] = "modified content"
    assert signer.verify_block(signed_block) is False

def test_verify_block_missing_fields():
    signer = Signer()
    block = {
        "version": "1.0",
        "content": "test content",
        "timestamp": 1234567890
    }
    
    assert signer.verify_block(block) is False  # Missing signature and public_key
    block["signature"] = "invalid"
    assert signer.verify_block(block) is False  # Missing public_key
    block["public_key"] = "invalid"
    assert signer.verify_block(block) is False  # Invalid signature and public_key 