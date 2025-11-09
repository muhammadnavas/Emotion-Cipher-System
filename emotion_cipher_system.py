"""
Emotion Cipher System
A secure emotion-aware text processing system that combines RSA encryption with AI emotion analysis
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

from rsa_encryption import RSAEncryption
from openai_integration import OpenAIClient


class EmotionCipherSystem:
    """
    Emotion Cipher System - Secure emotion-aware text processing
    
    Combines RSA encryption with AI emotion analysis to create a system where:
    - Text messages are securely encrypted using RSA algorithm
    - Emotions in messages are analyzed and preserved
    - Complete decryption recovers both original text and emotional context
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Emotion Cipher System
        
        Args:
            openai_api_key (str, optional): OpenAI API key for emotion processing
        """
        # Initialize RSA encryption
        self.rsa = RSAEncryption()
        self.keys_generated = False
        
        # Initialize OpenAI integration if API key provided
        self.openai_client = None
        self.openai_available = False
        
        if openai_api_key:
            try:
                self.openai_client = OpenAIClient(openai_api_key)
                self.openai_available = True
            except Exception as e:
                print(f"Warning: OpenAI integration failed - {e}")
        else:
            # Try to load from environment (.env file)
            try:
                self.openai_client = OpenAIClient()  # Will auto-load from .env
                self.openai_available = True
            except Exception:
                print("Note: No OpenAI API key provided. Emotion analysis will not be available.")
        
        # Cipher history for analysis
        self.cipher_history = []
    
    def setup_encryption_keys(self, key_dir: str = "keys") -> bool:
        """
        Set up RSA encryption keys (generate new or load existing)
        
        Args:
            key_dir (str): Directory to store/load keys
            
        Returns:
            bool: True if keys are ready
        """
        os.makedirs(key_dir, exist_ok=True)
        
        private_key_path = os.path.join(key_dir, "private_key.pem")
        public_key_path = os.path.join(key_dir, "public_key.pem")
        
        # Try to load existing keys
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            try:
                with open(private_key_path, 'rb') as f:
                    private_pem = f.read()
                with open(public_key_path, 'rb') as f:
                    public_pem = f.read()
                
                self.rsa.load_private_key(private_pem)
                self.rsa.load_public_key(public_pem)
                
                print(f"Loaded existing RSA keys from {key_dir}/")
                self.keys_generated = True
                return True
                
            except Exception as e:
                print(f"Failed to load existing keys: {e}")
        
        # Generate new keys
        try:
            private_pem, public_pem = self.rsa.generate_key_pair()
            
            # Save keys to files
            with open(private_key_path, 'wb') as f:
                f.write(private_pem)
            with open(public_key_path, 'wb') as f:
                f.write(public_pem)
            
            print(f"Generated new RSA keys and saved to {key_dir}/")
            self.keys_generated = True
            return True
            
        except Exception as e:
            print(f"Failed to generate keys: {e}")
            return False
    
    def process_message(self, message: str, analyze_emotion: bool = True) -> Dict:
        """
        Process a message with encryption and optional emotion analysis
        
        Args:
            message (str): Text message to process
            analyze_emotion (bool): Whether to analyze emotions
            
        Returns:
            dict: Processing results
        """
        if not self.keys_generated:
            self.setup_encryption_keys()
        
        result = {
            "original_message": message,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            # Analyze emotion if available and requested
            if analyze_emotion and self.openai_available:
                emotion_analysis = self.openai_client.analyze_emotion(message)
                result["emotion_analysis"] = emotion_analysis
            
            # Encrypt the message
            encrypted_message = self.rsa.encrypt(message)
            result["encrypted_message"] = encrypted_message
            
            # Record operation
            self.cipher_history.append({
                "timestamp": result["timestamp"],
                "message_length": len(message),
                "encrypted_length": len(encrypted_message),
                "has_emotion_analysis": analyze_emotion and self.openai_available,
                "success": True
            })
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def decrypt_message(self, encrypted_message: str, analyze_emotion: bool = True) -> Dict:
        """
        Decrypt a message and optionally analyze its emotions
        
        Args:
            encrypted_message (str): Encrypted message to decrypt
            analyze_emotion (bool): Whether to analyze emotions in decrypted text
            
        Returns:
            dict: Decryption results
        """
        result = {
            "encrypted_message": encrypted_message,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            # Decrypt the message
            decrypted_message = self.rsa.decrypt(encrypted_message)
            result["decrypted_message"] = decrypted_message
            
            # Analyze emotion if available and requested
            if analyze_emotion and self.openai_available:
                emotion_analysis = self.openai_client.analyze_emotion(decrypted_message)
                result["emotion_analysis"] = emotion_analysis
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def batch_process_messages(self, messages: List[str], analyze_emotions: bool = True) -> List[Dict]:
        """
        Process multiple messages in batch
        
        Args:
            messages (List[str]): List of messages to process
            analyze_emotions (bool): Whether to analyze emotions
            
        Returns:
            List[dict]: Results for each message
        """
        results = []
        
        for i, message in enumerate(messages):
            print(f"Processing message {i+1}/{len(messages)}...")
            result = self.process_message(message, analyze_emotions)
            results.append(result)
        
        return results
    
    def get_system_status(self) -> Dict:
        """
        Get current system status and capabilities
        
        Returns:
            dict: System status information
        """
        return {
            "encryption": {
                "keys_ready": self.keys_generated,
                "algorithm": "RSA-2048"
            },
            "emotion_analysis": {
                "available": self.openai_available,
                "provider": "OpenAI GPT-3.5-turbo" if self.openai_available else None
            },
            "statistics": {
                "total_operations": len(self.cipher_history),
                "successful_operations": len([c for c in self.cipher_history if c.get("success")])
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def export_data(self, filename: str = "emotion_cipher_data.json") -> bool:
        """
        Export system data and history to JSON file
        
        Args:
            filename (str): Output filename
            
        Returns:
            bool: True if export successful
        """
        try:
            export_data = {
                "export_info": {
                    "timestamp": datetime.now().isoformat(),
                    "system_version": "1.0.0"
                },
                "system_status": self.get_system_status(),
                "cipher_history": self.cipher_history
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"Data exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Export failed: {e}")
            return False


# Simple demonstration function
def demo():
    """Simple demonstration of the Emotion Cipher System"""
    print("=== Emotion Cipher System Demo ===")
    print()
    
    # Initialize system
    system = EmotionCipherSystem()
    
    # Check system status
    status = system.get_system_status()
    print("System Status:")
    print(f"  Encryption: {'✓' if status['encryption']['keys_ready'] else '✗'} {status['encryption']['algorithm']}")
    print(f"  Emotion Analysis: {'✓' if status['emotion_analysis']['available'] else '✗'} {status['emotion_analysis']['provider'] or 'Not available'}")
    print()
    
    # Demo messages
    demo_messages = [
        "I'm really excited about this new project!",
        "I'm feeling a bit worried about the upcoming deadline.",
        "This is just a normal message without strong emotions."
    ]
    
    print("Processing demo messages...")
    print("=" * 50)
    
    for i, message in enumerate(demo_messages, 1):
        print(f"\nMessage {i}: \"{message}\"")
        
        # Process message
        result = system.process_message(message)
        
        if result['success']:
            print(f"✓ Encrypted successfully")
            
            # Show emotion analysis if available
            if 'emotion_analysis' in result:
                emotion = result['emotion_analysis']
                print(f"  Detected emotion: {emotion.get('primary_emotion', 'unknown')}")
                print(f"  Sentiment: {emotion.get('sentiment', 'unknown')}")
            
            # Decrypt to verify
            decrypt_result = system.decrypt_message(result['encrypted_message'])
            if decrypt_result['success']:
                print(f"✓ Decrypted: \"{decrypt_result['decrypted_message']}\"")
            else:
                print(f"✗ Decryption failed: {decrypt_result.get('error')}")
        else:
            print(f"✗ Processing failed: {result.get('error')}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    
    # Export data
    system.export_data("demo_results.json")


if __name__ == "__main__":
    demo()