# Handles block validation

import requests
from typing import Dict, Optional, Tuple
from datetime import datetime
import json
import hashlib
from skyfield.api import load, wgs84
from skyfield.data import hipparcos
from .cosmo_signature import CosmoSignatureGenerator

class CosmoValidator:
    """Class for validating blocks using cosmo signatures."""
    
    def __init__(self, latitude: float, longitude: float, elevation: float = 0.0, api_key: Optional[str] = None):
        """
        Initialize the CosmoValidator with location data.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            elevation: Elevation in meters (default: 0.0)
            api_key: API key for astronomical data services (optional)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.location = wgs84.latlon(latitude, longitude, elevation_m=elevation)
        self.signature_generator = CosmoSignatureGenerator(api_key=api_key)
        
    def get_celestial_signature(self, timestamp: Optional[float] = None) -> Dict:
        """
        Get the celestial signature for a given timestamp.
        
        Args:
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            Dict: Celestial signature data
        """
        if timestamp is None:
            timestamp = datetime.utcnow().timestamp()
            
        # Load ephemeris data
        planets = load('de421.bsp')
        
        # Create time object
        ts = load.timescale()
        t = ts.from_datetime(datetime.fromtimestamp(timestamp))
        
        # Get positions of major celestial bodies
        sun = planets['sun'].at(t)
        moon = planets['moon'].at(t)
        earth = planets['earth'].at(t)
        
        # Calculate positions relative to observer
        sun_pos = sun.observe(self.location)
        moon_pos = moon.observe(self.location)
        
        # Get apparent positions
        sun_apparent = sun_pos.apparent()
        moon_apparent = moon_pos.apparent()
        
        # Get cosmo signature from stars
        cosmo_signature = self.signature_generator.generate_signature(
            latitude=self.latitude,
            longitude=self.longitude,
            elevation=self.elevation,
            timestamp=timestamp
        )
        
        # Create signature
        signature = {
            "timestamp": timestamp,
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "elevation": self.elevation
            },
            "celestial_bodies": {
                "sun": {
                    "altitude": float(sun_apparent.altitude.degrees),
                    "azimuth": float(sun_apparent.azimuth.degrees),
                    "distance_au": float(sun_pos.distance().au)
                },
                "moon": {
                    "altitude": float(moon_apparent.altitude.degrees),
                    "azimuth": float(moon_apparent.azimuth.degrees),
                    "distance_au": float(moon_pos.distance().au),
                    "phase": float(moon_pos.phase_angle().degrees)
                }
            },
            "cosmo_signature": cosmo_signature
        }
        
        return signature
    
    def validate_block(self, block: Dict) -> Tuple[bool, str]:
        """
        Validate a block using cosmo signature.
        
        Args:
            block: Block to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, reason)
        """
        # Check if block has required fields
        if "timestamp" not in block:
            return False, "Block missing timestamp"
            
        # Get cosmo signature for block's timestamp
        signature = self.get_celestial_signature(block["timestamp"])
        
        # Add cosmo signature to block
        block["cosmo_signature"] = signature
        
        # Calculate hash of cosmo signature
        signature_str = json.dumps(signature, sort_keys=True)
        signature_hash = hashlib.sha256(signature_str.encode()).hexdigest()
        
        # Add hash to block
        block["cosmo_hash"] = signature_hash
        
        return True, "Block validated with cosmo signature"
    
    def verify_cosmo_signature(self, block: Dict) -> Tuple[bool, str]:
        """
        Verify the cosmo signature of a block.
        
        Args:
            block: Block to verify
            
        Returns:
            Tuple[bool, str]: (is_valid, reason)
        """
        if "cosmo_signature" not in block or "cosmo_hash" not in block:
            return False, "Block missing cosmo signature or hash"
            
        # Get stored signature and hash
        stored_signature = block["cosmo_signature"]
        stored_hash = block["cosmo_hash"]
        
        # Calculate hash of stored signature
        signature_str = json.dumps(stored_signature, sort_keys=True)
        calculated_hash = hashlib.sha256(signature_str.encode()).hexdigest()
        
        # Verify hash matches
        if calculated_hash != stored_hash:
            return False, "Cosmo signature hash mismatch"
            
        # Verify timestamp is within reasonable range (e.g., 5 minutes)
        current_time = datetime.utcnow().timestamp()
        time_diff = abs(current_time - stored_signature["timestamp"])
        if time_diff > 300:  # 5 minutes in seconds
            return False, "Cosmo signature timestamp too old"
            
        # Verify the cosmo signature string
        if "cosmo_signature" in stored_signature:
            cosmo_signature = stored_signature["cosmo_signature"]
            is_valid = self.signature_generator.verify_signature(
                signature=cosmo_signature,
                latitude=self.latitude,
                longitude=self.longitude,
                elevation=self.elevation,
                timestamp=stored_signature["timestamp"]
            )
            if not is_valid:
                return False, "Cosmo signature verification failed"
                
        return True, "Cosmo signature verified"
