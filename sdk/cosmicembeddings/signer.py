# Handles block signing

import ed25519
import json
from typing import Dict, Tuple
import base64

class Signer:
    """Class for handling Ed25519 block signatures."""
    
    def __init__(self):
        """Initialize the Signer by generating a new key pair."""
        self.signing_key = ed25519.SigningKey(ed25519.create_seed())
        self.verifying_key = self.signing_key.get_verifying_key()
        
    @classmethod
    def from_seed(cls, seed: bytes) -> 'Signer':
        """
        Create a Signer from a seed.
        
        Args:
            seed: Seed to generate keys from
            
        Returns:
            Signer: Signer instance
        """
        instance = cls()
        instance.signing_key = ed25519.SigningKey(seed)
        instance.verifying_key = instance.signing_key.get_verifying_key()
        return instance
    
    def get_public_key(self) -> str:
        """
        Get the public key in base64 format.
        
        Returns:
            str: Base64 encoded public key
        """
        return base64.b64encode(self.verifying_key.to_bytes()).decode('utf-8')
    
    def sign_block(self, block: Dict) -> Dict:
        """
        Sign a block using Ed25519.
        
        Args:
            block: Block to sign
            
        Returns:
            Dict: Block with signature added
        """
        # Create a copy of the block without signature if it exists
        block_to_sign = block.copy()
        if "signature" in block_to_sign:
            del block_to_sign["signature"]
            
        # Convert block to ordered JSON string
        block_str = json.dumps(block_to_sign, sort_keys=True)
        
        # Sign the block
        signature = self.signing_key.sign(block_str.encode('utf-8'))
        
        # Add signature and public key to block
        block["signature"] = base64.b64encode(signature).decode('utf-8')
        block["public_key"] = self.get_public_key()
        
        return block
    
    def verify_block(self, block: Dict) -> bool:
        """
        Verify a block's signature.
        
        Args:
            block: Block to verify
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if "signature" not in block or "public_key" not in block:
            return False
            
        # Create a copy of the block without signature
        block_to_verify = block.copy()
        signature = base64.b64decode(block_to_verify.pop("signature"))
        public_key = base64.b64decode(block_to_verify.pop("public_key"))
        
        # Convert block to ordered JSON string
        block_str = json.dumps(block_to_verify, sort_keys=True)
        
        try:
            # Verify the signature
            verifying_key = ed25519.VerifyingKey(public_key)
            verifying_key.verify(signature, block_str.encode('utf-8'))
            return True
        except ed25519.BadSignatureError:
            return False
