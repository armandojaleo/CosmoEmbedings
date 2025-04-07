import argparse
import json
import os
import sys
from typing import Dict, List, Optional
from .block_builder import BlockBuilder
from .signer import Signer
from .validator import CosmicValidator

def create_block(args):
    """Create a new block with embeddings."""
    builder = BlockBuilder(model_name=args.model)
    
    # Read content from file or use direct input
    if args.input_file:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    else:
        content = args.content
        
    # Create metadata
    metadata = {}
    if args.metadata:
        for item in args.metadata:
            key, value = item.split('=', 1)
            metadata[key] = value
            
    # Create block
    block = builder.create_block(content, metadata)
    
    # Sign block if requested
    if args.sign:
        signer = Signer()
        block = signer.sign_block(block)
        
    # Validate block with cosmic signature if requested
    if args.validate:
        validator = CosmicValidator(args.latitude, args.longitude, args.elevation)
        is_valid, reason = validator.validate_block(block)
        if not is_valid:
            print(f"Validation failed: {reason}")
            sys.exit(1)
            
    # Save block to file
    if args.output_file:
        builder.save_block(block, args.output_file)
        print(f"Block saved to {args.output_file}")
    else:
        print(json.dumps(block, indent=2))
        
def verify_block(args):
    """Verify a block's signature and cosmic validation."""
    # Load block from file
    with open(args.block_file, 'r', encoding='utf-8') as f:
        block = json.load(f)
        
    # Verify Ed25519 signature if present
    if "signature" in block and "public_key" in block:
        signer = Signer()
        if signer.verify_block(block):
            print("Ed25519 signature: VALID")
        else:
            print("Ed25519 signature: INVALID")
    else:
        print("Ed25519 signature: NOT FOUND")
        
    # Verify cosmic signature if present
    if "cosmic_signature" in block and "cosmic_hash" in block:
        validator = CosmicValidator(args.latitude, args.longitude, args.elevation)
        is_valid, reason = validator.verify_cosmic_signature(block)
        print(f"Cosmic signature: {'VALID' if is_valid else 'INVALID'}")
        if not is_valid:
            print(f"Reason: {reason}")
    else:
        print("Cosmic signature: NOT FOUND")
        
def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="CosmicEmbeddings CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create block command
    create_parser = subparsers.add_parser("create", help="Create a new block")
    create_parser.add_argument("--model", default="all-MiniLM-L6-v2", help="Model to use for embeddings")
    create_parser.add_argument("--content", help="Content to create embeddings for")
    create_parser.add_argument("--input-file", help="File containing content to create embeddings for")
    create_parser.add_argument("--output-file", help="File to save the block to")
    create_parser.add_argument("--metadata", nargs="+", help="Metadata in key=value format")
    create_parser.add_argument("--sign", action="store_true", help="Sign the block with Ed25519")
    create_parser.add_argument("--validate", action="store_true", help="Validate the block with cosmic signature")
    create_parser.add_argument("--latitude", type=float, default=0.0, help="Latitude for cosmic validation")
    create_parser.add_argument("--longitude", type=float, default=0.0, help="Longitude for cosmic validation")
    create_parser.add_argument("--elevation", type=float, default=0.0, help="Elevation for cosmic validation")
    create_parser.set_defaults(func=create_block)
    
    # Verify block command
    verify_parser = subparsers.add_parser("verify", help="Verify a block")
    verify_parser.add_argument("block_file", help="File containing the block to verify")
    verify_parser.add_argument("--latitude", type=float, default=0.0, help="Latitude for cosmic validation")
    verify_parser.add_argument("--longitude", type=float, default=0.0, help="Longitude for cosmic validation")
    verify_parser.add_argument("--elevation", type=float, default=0.0, help="Elevation for cosmic validation")
    verify_parser.set_defaults(func=verify_block)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
        
    args.func(args)
    
if __name__ == "__main__":
    main()
