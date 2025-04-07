# Handles communication with peers

import requests
import json
import base64
from typing import Dict, List, Optional, Union
import uuid
from .config import Config

class SyncClient:
    """Client for interacting with other nodes in the CosmicEmbeddings network."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the sync client.
        
        Args:
            config: Configuration object (optional)
        """
        self.config = config or Config()
        self.api_endpoint = self.config.get_api_endpoint()
        self.node_id = self.config.get_node_id()
        self.session = requests.Session()
        
    def push_block(self, block: Dict) -> Dict:
        """
        Push a block to the network.
        
        Args:
            block: Block to push
            
        Returns:
            Dict: Response from the server
        """
        # Ensure block has an ID
        if "id" not in block:
            block["id"] = f"block-{uuid.uuid4().hex[:8]}"
            
        # Ensure block has a creator
        if "created_by" not in block:
            block["created_by"] = self.node_id
            
        # Send block to server
        response = self.session.post(
            f"{self.api_endpoint}/blocks",
            json=block,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to push block: {response.text}")
            
        return response.json()
        
    def get_block(self, block_id: str) -> Dict:
        """
        Get a block from the network.
        
        Args:
            block_id: ID of the block to get
            
        Returns:
            Dict: The requested block
        """
        response = self.session.get(
            f"{self.api_endpoint}/blocks/{block_id}",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get block: {response.text}")
            
        return response.json()
        
    def search_blocks(self, 
                     query: Optional[str] = None, 
                     tags: Optional[List[str]] = None,
                     created_by: Optional[str] = None,
                     limit: int = 10) -> List[Dict]:
        """
        Search for blocks in the network.
        
        Args:
            query: Text query to search for
            tags: Tags to filter by
            created_by: Creator to filter by
            limit: Maximum number of results to return
            
        Returns:
            List[Dict]: List of matching blocks
        """
        params = {}
        if query:
            params["q"] = query
        if tags:
            params["tags"] = ",".join(tags)
        if created_by:
            params["created_by"] = created_by
        if limit:
            params["limit"] = limit
            
        response = self.session.get(
            f"{self.api_endpoint}/blocks/search",
            params=params,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to search blocks: {response.text}")
            
        return response.json().get("blocks", [])
        
    def get_related_blocks(self, block_id: str, limit: int = 5) -> List[Dict]:
        """
        Get blocks related to a specific block.
        
        Args:
            block_id: ID of the block to find related blocks for
            limit: Maximum number of results to return
            
        Returns:
            List[Dict]: List of related blocks
        """
        response = self.session.get(
            f"{self.api_endpoint}/blocks/{block_id}/related",
            params={"limit": limit},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get related blocks: {response.text}")
            
        return response.json().get("blocks", [])
        
    def get_node_info(self) -> Dict:
        """
        Get information about the current node.
        
        Returns:
            Dict: Node information
        """
        response = self.session.get(
            f"{self.api_endpoint}/nodes/{self.node_id}",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get node info: {response.text}")
            
        return response.json()
        
    def register_node(self, 
                     name: Optional[str] = None, 
                     description: Optional[str] = None,
                     location: Optional[tuple] = None) -> Dict:
        """
        Register the current node with the network.
        
        Args:
            name: Node name (optional)
            description: Node description (optional)
            location: Node location as (latitude, longitude, elevation) (optional)
            
        Returns:
            Dict: Registration response
        """
        # Use provided values or defaults from config
        name = name or self.node_id
        location = location or self.config.get_location()
        
        node_data = {
            "id": self.node_id,
            "name": name,
            "location": {
                "latitude": location[0],
                "longitude": location[1],
                "elevation": location[2]
            }
        }
        
        if description:
            node_data["description"] = description
            
        # Get keys if available
        private_key, public_key = self.config.get_keys()
        if public_key:
            node_data["public_key"] = public_key
            
        response = self.session.post(
            f"{self.api_endpoint}/nodes",
            json=node_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to register node: {response.text}")
            
        return response.json()
        
    def get_peers(self) -> List[Dict]:
        """
        Get list of peer nodes in the network.
        
        Returns:
            List[Dict]: List of peer nodes
        """
        response = self.session.get(
            f"{self.api_endpoint}/nodes",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get peers: {response.text}")
            
        return response.json().get("nodes", [])
        
    def validate_block(self, block_id: str) -> Dict:
        """
        Request validation of a block by the network.
        
        Args:
            block_id: ID of the block to validate
            
        Returns:
            Dict: Validation results
        """
        response = self.session.post(
            f"{self.api_endpoint}/blocks/{block_id}/validate",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to validate block: {response.text}")
            
        return response.json()
