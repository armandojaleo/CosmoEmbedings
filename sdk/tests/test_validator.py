# test_validator.py
from cosmicembeddings.validator import validate_block

def test_dummy_validation():
    block = {"signature": "signed_with_private_key"}
    assert validate_block(block, "demo_public_key") == True
