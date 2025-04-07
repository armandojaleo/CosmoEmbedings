# Handles configuration loading

import os
from typing import Dict, Optional, Tuple, Union
import json
from pathlib import Path

class Config:
    """Configuration manager for the CosmoEmbeddings SDK."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to a JSON configuration file (optional)
        """
        # Default configuration
        self.config = {
            "node_id": "default_node",
            "default_model": "all-MiniLM-L6-v2",
            "default_location": (0.0, 0.0, 0.0),  # (latitude, longitude, elevation)
            "api_endpoint": "http://localhost:8080",
            "private_key": None,
            "public_key": None,
            "cosmic_validation": {
                "enabled": True,
                "max_age_seconds": 300,  # 5 minutes
                "require_location": True
            }
        }
        
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file if provided
        if config_file:
            self._load_from_file(config_file)
            
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Node configuration
        if "COSMIC_NODE_ID" in os.environ:
            self.config["node_id"] = os.environ["COSMIC_NODE_ID"]
            
        if "COSMIC_DEFAULT_MODEL" in os.environ:
            self.config["default_model"] = os.environ["COSMIC_DEFAULT_MODEL"]
            
        if "COSMIC_API_ENDPOINT" in os.environ:
            self.config["api_endpoint"] = os.environ["COSMIC_API_ENDPOINT"]
            
        # Location configuration
        if all(k in os.environ for k in ["COSMIC_LATITUDE", "COSMIC_LONGITUDE"]):
            lat = float(os.environ["COSMIC_LATITUDE"])
            lon = float(os.environ["COSMIC_LONGITUDE"])
            elev = float(os.environ.get("COSMIC_ELEVATION", "0.0"))
            self.config["default_location"] = (lat, lon, elev)
            
        # Key configuration
        if "COSMIC_PRIVATE_KEY" in os.environ:
            self.config["private_key"] = os.environ["COSMIC_PRIVATE_KEY"]
            
        if "COSMIC_PUBLIC_KEY" in os.environ:
            self.config["public_key"] = os.environ["COSMIC_PUBLIC_KEY"]
            
        # Cosmo validation configuration
        if "COSMIC_VALIDATION_ENABLED" in os.environ:
            self.config["cosmic_validation"]["enabled"] = os.environ["COSMIC_VALIDATION_ENABLED"].lower() == "true"
            
        if "COSMIC_VALIDATION_MAX_AGE" in os.environ:
            self.config["cosmic_validation"]["max_age_seconds"] = int(os.environ["COSMIC_VALIDATION_MAX_AGE"])
            
        if "COSMIC_VALIDATION_REQUIRE_LOCATION" in os.environ:
            self.config["cosmic_validation"]["require_location"] = os.environ["COSMIC_VALIDATION_REQUIRE_LOCATION"].lower() == "true"
            
    def _load_from_file(self, config_file: str):
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                
            # Update configuration with file values
            for key, value in file_config.items():
                if key == "default_location" and isinstance(value, list) and len(value) >= 2:
                    # Convert list to tuple
                    lat, lon = value[0], value[1]
                    elev = value[2] if len(value) > 2 else 0.0
                    self.config[key] = (lat, lon, elev)
                else:
                    self.config[key] = value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load configuration file: {e}")
            
    def save_to_file(self, config_file: str):
        """
        Save the current configuration to a JSON file.
        
        Args:
            config_file: Path to save the configuration to
        """
        # Convert tuple to list for JSON serialization
        config_to_save = self.config.copy()
        if isinstance(config_to_save["default_location"], tuple):
            config_to_save["default_location"] = list(config_to_save["default_location"])
            
        with open(config_file, 'w') as f:
            json.dump(config_to_save, f, indent=2)
            
    def get(self, key: str, default=None):
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            The configuration value
        """
        return self.config.get(key, default)
        
    def set(self, key: str, value):
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        
    def get_location(self) -> Tuple[float, float, float]:
        """
        Get the default location as a tuple.
        
        Returns:
            Tuple of (latitude, longitude, elevation)
        """
        return self.config["default_location"]
        
    def set_location(self, latitude: float, longitude: float, elevation: float = 0.0):
        """
        Set the default location.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            elevation: Elevation in meters
        """
        self.config["default_location"] = (latitude, longitude, elevation)
        
    def get_node_id(self) -> str:
        """
        Get the node ID.
        
        Returns:
            The node ID
        """
        return self.config["node_id"]
        
    def set_node_id(self, node_id: str):
        """
        Set the node ID.
        
        Args:
            node_id: The node ID
        """
        self.config["node_id"] = node_id
        
    def get_default_model(self) -> str:
        """
        Get the default embedding model.
        
        Returns:
            The default model name
        """
        return self.config["default_model"]
        
    def set_default_model(self, model: str):
        """
        Set the default embedding model.
        
        Args:
            model: The model name
        """
        self.config["default_model"] = model
        
    def get_api_endpoint(self) -> str:
        """
        Get the API endpoint.
        
        Returns:
            The API endpoint URL
        """
        return self.config["api_endpoint"]
        
    def set_api_endpoint(self, endpoint: str):
        """
        Set the API endpoint.
        
        Args:
            endpoint: The API endpoint URL
        """
        self.config["api_endpoint"] = endpoint
        
    def get_keys(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the private and public keys.
        
        Returns:
            Tuple of (private_key, public_key)
        """
        return (self.config["private_key"], self.config["public_key"])
        
    def set_keys(self, private_key: Optional[str], public_key: Optional[str]):
        """
        Set the private and public keys.
        
        Args:
            private_key: The private key
            public_key: The public key
        """
        self.config["private_key"] = private_key
        self.config["public_key"] = public_key
        
    def is_cosmic_validation_enabled(self) -> bool:
        """
        Check if cosmic validation is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        return self.config["cosmic_validation"]["enabled"]
        
    def set_cosmic_validation_enabled(self, enabled: bool):
        """
        Enable or disable cosmic validation.
        
        Args:
            enabled: Whether to enable cosmic validation
        """
        self.config["cosmic_validation"]["enabled"] = enabled
        
    def get_cosmic_validation_max_age(self) -> int:
        """
        Get the maximum age for cosmic validation in seconds.
        
        Returns:
            Maximum age in seconds
        """
        return self.config["cosmic_validation"]["max_age_seconds"]
        
    def set_cosmic_validation_max_age(self, max_age_seconds: int):
        """
        Set the maximum age for cosmic validation.
        
        Args:
            max_age_seconds: Maximum age in seconds
        """
        self.config["cosmic_validation"]["max_age_seconds"] = max_age_seconds
        
    def is_location_required(self) -> bool:
        """
        Check if location is required for cosmic validation.
        
        Returns:
            True if required, False otherwise
        """
        return self.config["cosmic_validation"]["require_location"]
        
    def set_location_required(self, required: bool):
        """
        Set whether location is required for cosmic validation.
        
        Args:
            required: Whether location is required
        """
        self.config["cosmic_validation"]["require_location"] = required
