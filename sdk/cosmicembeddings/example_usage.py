#!/usr/bin/env python3
"""
Example usage of the CosmoEmbeddings SDK.
This script demonstrates how to create, sign, validate, and verify blocks.
"""

import json
import os
import tempfile
from block_builder import BlockBuilder
from signer import Signer
from validator import CosmoValidator
from cosmic_signature import CosmoSignatureGenerator

def main():
    # Create a temporary directory for our example
    with tempfile.TemporaryDirectory() as temp_dir:
        print("=== CosmoEmbeddings SDK Example ===")
        
        # Initialize components
        print("\n1. Initializing components...")
        builder = BlockBuilder()
        signer = Signer()
        validator = CosmoValidator(40.7128, -74.0060)  # New York coordinates
        
        # Create a block
        print("\n2. Creating a block...")
        content = "This is an example of a cosmic embedding block."
        metadata = {"source": "example", "author": "demo"}
        block = builder.create_block(content, metadata)
        print(f"Block created with {len(block['embeddings'])} embeddings")
        
        # Save the block
        block_path = os.path.join(temp_dir, "block.json")
        builder.save_block(block, block_path)
        print(f"Block saved to {block_path}")
        
        # Sign the block
        print("\n3. Signing the block...")
        signed_block = signer.sign_block(block)
        print("Block signed with Ed25519")
        
        # Save the signed block
        signed_block_path = os.path.join(temp_dir, "signed_block.json")
        builder.save_block(signed_block, signed_block_path)
        print(f"Signed block saved to {signed_block_path}")
        
        # Validate the block with cosmic signature
        print("\n4. Validating the block with cosmic signature...")
        is_valid, reason = validator.validate_block(signed_block)
        print(f"Validation result: {reason}")
        
        # Save the validated block
        validated_block_path = os.path.join(temp_dir, "validated_block.json")
        builder.save_block(signed_block, validated_block_path)
        print(f"Validated block saved to {validated_block_path}")
        
        # Verify the block
        print("\n5. Verifying the block...")
        # Verify Ed25519 signature
        if signer.verify_block(signed_block):
            print("Ed25519 signature: VALID")
        else:
            print("Ed25519 signature: INVALID")
            
        # Verify cosmic signature
        is_valid, reason = validator.verify_cosmic_signature(signed_block)
        print(f"Cosmo signature: {'VALID' if is_valid else 'INVALID'}")
        if not is_valid:
            print(f"Reason: {reason}")
            
        # Demonstrate tampering detection
        print("\n6. Demonstrating tampering detection...")
        tampered_block = signed_block.copy()
        tampered_block["content"] = "This content has been tampered with!"
        
        # Verify the tampered block
        if signer.verify_block(tampered_block):
            print("Ed25519 signature: VALID (unexpected!)")
        else:
            print("Ed25519 signature: INVALID (expected)")
            
        is_valid, reason = validator.verify_cosmic_signature(tampered_block)
        print(f"Cosmo signature: {'VALID' if is_valid else 'INVALID'}")
        if not is_valid:
            print(f"Reason: {reason}")
            
        # Demonstrate direct use of CosmoSignatureGenerator
        print("\n7. Demonstrating direct use of CosmoSignatureGenerator...")
        generator = CosmoSignatureGenerator()
        
        # Generate a cosmic signature
        signature = generator.generate_signature(40.7128, -74.0060)
        print(f"Generated cosmic signature: {signature}")
        
        # Verify the signature
        is_valid = generator.verify_signature(
            signature=signature,
            latitude=40.7128,
            longitude=-74.0060
        )
        print(f"Signature verification: {'VALID' if is_valid else 'INVALID'}")
        
        # Demonstrate location sensitivity
        print("\n8. Demonstrating location sensitivity...")
        # Generate signatures for different locations
        ny_signature = generator.generate_signature(40.7128, -74.0060)  # New York
        la_signature = generator.generate_signature(34.0522, -118.2437)  # Los Angeles
        
        print(f"New York signature: {ny_signature}")
        print(f"Los Angeles signature: {la_signature}")
        print(f"Signatures are different: {ny_signature != la_signature}")
        
        print("\n=== Example Complete ===")
        print(f"All files were saved in the temporary directory: {temp_dir}")
        print("This directory will be automatically deleted when the script exits.")

if __name__ == "__main__":
    main()
