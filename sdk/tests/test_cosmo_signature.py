import unittest
import time
from cosmoembeddings import CosmoSignatureGenerator

class TestCosmoSignatureGenerator(unittest.TestCase):
    """Test cases for the CosmoSignatureGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = CosmoSignatureGenerator()
        
    def test_get_star_positions(self):
        """Test getting star positions."""
        stars = self.generator.get_star_positions(40.7128, -74.0060)
        self.assertIsInstance(stars, list)
        self.assertTrue(len(stars) > 0)
        
        # Check star structure
        star = stars[0]
        self.assertIn("name", star)
        self.assertIn("magnitude", star)
        self.assertIn("ra", star)
        self.assertIn("dec", star)
        self.assertIn("distance", star)
        
    def test_generate_signature(self):
        """Test generating a cosmo signature."""
        signature = self.generator.generate_signature(40.7128, -74.0060)
        self.assertIsInstance(signature, str)
        self.assertTrue("-" in signature)
        
        # Check signature format
        parts = signature.split("-")
        self.assertEqual(len(parts), 2)
        self.assertTrue(parts[0].isalpha())  # Constellation name
        self.assertTrue(parts[1].replace(".", "").isdigit())  # Magnitude
        
    def test_verify_signature(self):
        """Test verifying a cosmo signature."""
        # Generate a signature
        signature = self.generator.generate_signature(40.7128, -74.0060)
        
        # Verify the signature
        is_valid = self.generator.verify_signature(
            signature=signature,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.assertTrue(is_valid)
        
    def test_verify_invalid_signature(self):
        """Test verifying an invalid cosmo signature."""
        # Create an invalid signature
        invalid_signature = "Invalid-0.0"
        
        # Verify the signature
        is_valid = self.generator.verify_signature(
            signature=invalid_signature,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.assertFalse(is_valid)
        
    def test_timestamp_consistency(self):
        """Test that signatures are consistent for the same timestamp."""
        # Use a fixed timestamp
        timestamp = time.time()
        
        # Generate two signatures with the same parameters
        signature1 = self.generator.generate_signature(
            latitude=40.7128,
            longitude=-74.0060,
            timestamp=timestamp
        )
        
        signature2 = self.generator.generate_signature(
            latitude=40.7128,
            longitude=-74.0060,
            timestamp=timestamp
        )
        
        # Signatures should be the same
        self.assertEqual(signature1, signature2)
        
    def test_location_sensitivity(self):
        """Test that signatures are different for different locations."""
        # Use a fixed timestamp
        timestamp = time.time()
        
        # Generate signatures for different locations
        signature1 = self.generator.generate_signature(
            latitude=40.7128,
            longitude=-74.0060,
            timestamp=timestamp
        )
        
        signature2 = self.generator.generate_signature(
            latitude=34.0522,
            longitude=-118.2437,
            timestamp=timestamp
        )
        
        # Signatures should be different
        self.assertNotEqual(signature1, signature2)
        
    def test_fallback_stars(self):
        """Test that fallback stars are used when API is unavailable."""
        # Create a generator with an invalid API key
        generator = CosmoSignatureGenerator(api_key="invalid_key")
        
        # Get star positions
        stars = generator.get_star_positions(40.7128, -74.0060)
        
        # Should still return stars (fallback)
        self.assertIsInstance(stars, list)
        self.assertTrue(len(stars) > 0)
        
if __name__ == "__main__":
    unittest.main() 