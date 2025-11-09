"""
RSA Encryption Module for Emotion Cipher System
Provides RSA key generation, encryption, and decryption functionality
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64
import os
from typing import Tuple, Optional


class RSAEncryption:
    """RSA encryption and decryption handler"""
    
    def __init__(self, key_size: int = 2048):
        """
        Initialize RSA encryption with specified key size
        
        Args:
            key_size (int): Size of RSA key in bits (default: 2048)
        """
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        
    def generate_key_pair(self) -> Tuple[bytes, bytes]:
        """
        Generate RSA key pair
        
        Returns:
            Tuple[bytes, bytes]: (private_key_pem, public_key_pem)
        """
        # Generate private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        
        # Get public key
        self.public_key = self.private_key.public_key()
        
        # Serialize keys to PEM format
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def load_private_key(self, private_key_pem: bytes, password: Optional[bytes] = None):
        """
        Load private key from PEM format
        
        Args:
            private_key_pem (bytes): Private key in PEM format
            password (Optional[bytes]): Password for encrypted key
        """
        self.private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=password,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def load_public_key(self, public_key_pem: bytes):
        """
        Load public key from PEM format
        
        Args:
            public_key_pem (bytes): Public key in PEM format
        """
        self.public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )
    
    def encrypt(self, message: str) -> str:
        """
        Encrypt message using RSA public key
        
        Args:
            message (str): Message to encrypt
            
        Returns:
            str: Base64 encoded encrypted message
            
        Raises:
            ValueError: If public key is not loaded
        """
        if not self.public_key:
            raise ValueError("Public key not loaded")
        
        # Convert message to bytes
        message_bytes = message.encode('utf-8')
        
        # Encrypt using OAEP padding
        encrypted = self.public_key.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Return base64 encoded result
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypt message using RSA private key
        
        Args:
            encrypted_message (str): Base64 encoded encrypted message
            
        Returns:
            str: Decrypted message
            
        Raises:
            ValueError: If private key is not loaded
        """
        if not self.private_key:
            raise ValueError("Private key not loaded")
        
        # Decode from base64
        encrypted_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
        
        # Decrypt using OAEP padding
        decrypted = self.private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Return decoded string
        return decrypted.decode('utf-8')
    
    def save_keys_to_files(self, private_key_file: str = "private_key.pem", 
                          public_key_file: str = "public_key.pem"):
        """
        Save generated keys to files
        
        Args:
            private_key_file (str): Filename for private key
            public_key_file (str): Filename for public key
        """
        if not self.private_key or not self.public_key:
            raise ValueError("Keys not generated yet")
        
        # Get key data
        private_pem, public_pem = self.generate_key_pair()
        
        # Write to files
        with open(private_key_file, 'wb') as f:
            f.write(private_pem)
        
        with open(public_key_file, 'wb') as f:
            f.write(public_pem)
        
        print(f"Keys saved to {private_key_file} and {public_key_file}")
    
    def load_keys_from_files(self, private_key_file: str = "private_key.pem",
                            public_key_file: Optional[str] = None):
        """
        Load keys from files
        
        Args:
            private_key_file (str): Path to private key file
            public_key_file (Optional[str]): Path to public key file (optional)
        """
        # Load private key
        if os.path.exists(private_key_file):
            with open(private_key_file, 'rb') as f:
                self.load_private_key(f.read())
        else:
            raise FileNotFoundError(f"Private key file not found: {private_key_file}")
        
        # Load public key if specified
        if public_key_file and os.path.exists(public_key_file):
            with open(public_key_file, 'rb') as f:
                self.load_public_key(f.read())


def demo_rsa_encryption():
    """Demonstrate RSA encryption functionality"""
    print("=== RSA Encryption Demo ===")
    
    # Create RSA instance
    rsa_enc = RSAEncryption()
    
    # Generate keys
    print("Generating RSA key pair...")
    private_pem, public_pem = rsa_enc.generate_key_pair()
    
    # Test message
    test_message = "Hello, this is a secret emotion: Joy! 😊"
    print(f"Original message: {test_message}")
    
    # Encrypt
    encrypted = rsa_enc.encrypt(test_message)
    print(f"Encrypted (Base64): {encrypted[:50]}...")
    
    # Decrypt
    decrypted = rsa_enc.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
    
    # Verify
    assert test_message == decrypted, "Encryption/Decryption failed!"
    print("✅ RSA Encryption/Decryption successful!")


if __name__ == "__main__":
    demo_rsa_encryption()