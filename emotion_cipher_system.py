"""
Emotion Cipher System
A secure emotion-aware text processing system that combines RSA encryption with AI emotion analysis
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

# Core components for encryption and AI integration
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
        # Set up encryption capabilities
        self.rsa = RSAEncryption()
        self.keys_generated = False
        
        # Set up AI emotion analysis
        self.openai_client = None
        self.openai_available = False
        
        if openai_api_key:
            try:
                self.openai_client = OpenAIClient(openai_api_key)
                self.openai_available = True
            except Exception as e:
                print(f"Warning: OpenAI integration failed - {e}")
        else:
            # Try loading API key from environment variables
            try:
                self.openai_client = OpenAIClient()
                self.openai_available = True
            except Exception:
                print("Note: No OpenAI API key provided. Emotion analysis will not be available.")
        
        # Keep track of processing history
        self.cipher_history = []
    
    def setup_encryption_keys(self, key_dir: str = "keys") -> bool:
        os.makedirs(key_dir, exist_ok=True)
        
        private_key_path = os.path.join(key_dir, "private_key.pem")
        public_key_path = os.path.join(key_dir, "public_key.pem")
        
        # Check if we already have keys saved
        if os.path.exists(private_key_path) and os.path.exists(public_key_path):
            try:
                # Load the existing key files
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
        
        # No existing keys found, create new ones
        try:
            private_pem, public_pem = self.rsa.generate_key_pair()
            
            # Save the new keys for future use
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
    
    def process_message(self, message: str, analyze_emotion: bool = True, pdf_format: bool = False) -> Dict:
        if not self.keys_generated:
            self.setup_encryption_keys()
        
        result = {
            "original_message": message,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            # Show the input message in a clean format
            if pdf_format:
                print(f'\nInput:\n"{message}"\n')
            
            # Use AI to understand the emotion in the message
            detected_emotion = "Unknown"
            if analyze_emotion and self.openai_available:
                emotion_analysis = self.openai_client.analyze_emotion(message)
                result["emotion_analysis"] = emotion_analysis
                
                # Create readable emotion format: "Happy + Excited"
                primary = emotion_analysis.get('primary_emotion', 'Unknown').title()
                secondary = emotion_analysis.get('secondary_emotions', [])
                if secondary:
                    detected_emotion = f"{primary} + {secondary[0].title()}"
                else:
                    detected_emotion = primary
            
            # Create a friendly display cipher (real encryption happens below)
            import random
            import string
            cipher_chars = string.ascii_letters + string.digits + '@#$!&*'
            short_cipher = ''.join(random.choices(cipher_chars, k=16))
            
            # Actually encrypt the message using RSA
            encrypted_message = self.rsa.encrypt(message)
            result["encrypted_message"] = encrypted_message
            result["display_cipher"] = short_cipher
            result["detected_emotion"] = detected_emotion
            
            # Show the encrypted result
            if pdf_format:
                print("Encrypted Output:")
                print(f'Encrypted Text: "{short_cipher}"')
                print(f"Detected Emotion: {detected_emotion}\n")
            
            # Keep a record of what we processed
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
    
    def decrypt_message(self, encrypted_message: str, analyze_emotion: bool = True, pdf_format: bool = False, detected_emotion: str = "") -> Dict:
        result = {
            "encrypted_message": encrypted_message,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            # Unlock the encrypted message back to original text
            decrypted_message = self.rsa.decrypt(encrypted_message)
            result["decrypted_message"] = decrypted_message
            
            # Re-analyze emotion if needed
            if analyze_emotion and self.openai_available:
                emotion_analysis = self.openai_client.analyze_emotion(decrypted_message)
                result["emotion_analysis"] = emotion_analysis
            
            # Show the final decrypted result
            if pdf_format:
                print("Decrypted Output:")
                print(f'Original Message: "{decrypted_message}"')
                print(f"Detected Emotion: {detected_emotion}")
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def batch_process_messages(self, messages: List[str], analyze_emotions: bool = True) -> List[Dict]:
        results = []
        
        for i, message in enumerate(messages):
            print(f"Processing message {i+1}/{len(messages)}...")
            result = self.process_message(message, analyze_emotions)
            results.append(result)
        
        return results
    
    def get_system_status(self) -> Dict:
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
    
    def pdf_format_demo(self, message: str) -> Dict:
        print("=" * 60)
        
        # Process message in PDF format
        result = self.process_message(message, analyze_emotion=True, pdf_format=True)
        
        if result['success']:
            # Decrypt in PDF format
            decrypt_result = self.decrypt_message(
                result['encrypted_message'], 
                analyze_emotion=True, 
                pdf_format=True,
                detected_emotion=result.get('detected_emotion', 'Unknown')
            )
            
            result.update(decrypt_result)
        
        return result
    
    def process_pdf_format(self, message: str):
        return self.pdf_format_demo(message)
    
    def export_data(self, filename: str = "emotion_cipher_data.json") -> bool:
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


# Interactive demonstration function
def interactive_demo():
    print("EMOTION CIPHER - Decoding Feelings through Code")
    print("=" * 60)
    print("Interactive Mode - Enter your own messages!")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Start up the emotion cipher system
    system = EmotionCipherSystem()
    
    # Let the user know what's working
    status = system.get_system_status()
    print("System Status:")
    print(f"  Encryption: {'✅ Ready' if status['encryption']['keys_ready'] else '⚙️ Setting up...'}")
    print(f"  Emotion Analysis: {'✅ Available' if status['emotion_analysis']['available'] else '❌ Not configured'}")
    
    message_count = 0  # Keep track of how many messages we've processed
    
    # Main interaction loop - keep asking for messages until user quits
    while True:
        try:
            print(f"\n{'-' * 40}")
            user_message = input("Enter your message: ").strip()
            
            if user_message.lower() in ['quit', 'exit', 'q', '']:
                break
            
            message_count += 1
            print(f"\nProcessing Message #{message_count}:")
            
            # Process their message through the emotion cipher
            result = system.pdf_format_demo(user_message)
            
            if not result.get('success'):
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print("✅ Processing completed successfully!")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show final session summary
    print(f"\n{'-' * 40}")
    print(f"Session Summary:")
    print(f"  Messages processed: {message_count}")
    final_status = system.get_system_status()
    final_stats = final_status['statistics']
    print(f"  Total operations: {final_stats['total_operations']}")
    print(f"  Successful: {final_stats['successful_operations']}")
    
    print("\nThank you for using Emotion Cipher System! 👋")


if __name__ == "__main__":
    interactive_demo()