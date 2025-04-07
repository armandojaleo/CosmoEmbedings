# Handles block signing

import nacl.signing
import nacl.encoding
import json
import base64
from typing import Dict, Any, Optional

class Signer:
    """Class for handling Ed25519 block signatures using pynacl."""
    
    def __init__(self):
        """Initialize a new signer with a random key pair."""
        self.signing_key = nacl.signing.SigningKey.generate()
        self.verify_key = self.signing_key.verify_key
    
    @classmethod
    def from_seed(cls, seed: bytes) -> 'Signer':
        """Create a signer from a seed."""
        instance = cls()
        instance.signing_key = nacl.signing.SigningKey(seed)
        instance.verify_key = instance.signing_key.verify_key
        return instance
    
    def get_public_key(self) -> str:
        """Get the public key in base64 format."""
        return base64.b64encode(bytes(self.verify_key)).decode('utf-8')
    
    def get_private_key(self) -> str:
        """Get the private key in base64 format."""
        return base64.b64encode(bytes(self.signing_key)).decode('utf-8')
    
    def sign_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign a block using Ed25519.
        
        Args:
            block: The block to sign
            
        Returns:
            The block with added signature
        """
        # Create a copy of the block without the signature
        block_to_sign = block.copy()
        if 'signature' in block_to_sign:
            del block_to_sign['signature']
            
        # Convert to JSON and encode
        message = json.dumps(block_to_sign, sort_keys=True).encode('utf-8')
        
        # Sign the message
        signature = self.signing_key.sign(message)
        
        # Add signature to block
        block['signature'] = base64.b64encode(signature.signature).decode('utf-8')
        block['public_key'] = self.get_public_key()
        
        return block
    
    @staticmethod
    def verify_block(block: Dict[str, Any]) -> bool:
        """
        Verify a block's signature.
        
        Args:
            block: The block to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        if 'signature' not in block or 'public_key' not in block:
            return False
            
        try:
            # Get the public key and signature
            public_key = base64.b64decode(block['public_key'])
            signature = base64.b64decode(block['signature'])
            
            # Create verifying key
            verify_key = nacl.signing.VerifyKey(public_key)
            
            # Create a copy of the block without the signature
            block_to_verify = block.copy()
            del block_to_verify['signature']
            del block_to_verify['public_key']
            
            # Convert to JSON and encode
            message = json.dumps(block_to_verify, sort_keys=True).encode('utf-8')
            
            # Verify the signature
            verify_key.verify(message, signature)
            return True
            
        except (nacl.exceptions.BadSignatureError, ValueError, KeyError):
            return False
